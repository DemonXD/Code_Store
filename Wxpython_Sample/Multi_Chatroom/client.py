import wx
import asyncio
import json
from struct import pack
from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
from time import sleep

"""
types:['text', 'register', 'unregister', 'cmd', 'unknown]
"""


_MESSAGE_TEXT = {
    'type': 'text',
    'sender': 'niuminguo',
    'receiver': 'niuminguo',
    'content': 'love',
}

_MESSAGE_REG = {
    'type': 'register',
    'uid': 'nobody',
}


class LoginFrame(wx.Frame):
    """
    登录窗口
    """
    def __init__(self, parent, id, title, size):
        '''初始化，添加控件并绑定事件'''
        wx.Frame.__init__(self, parent, id, title)
        self.loop = asyncio.get_event_loop()
        # self.reader, self.writer = asyncio.open_connection('127.0.0.1', 6666, loop=self.loop)
        self.reader, self.writer = None, None
        self.SetSize(size)
        self.Center()
        self.serverAddressLabel = wx.StaticText(self, label = "Server Address", pos = (10, 50), size = (120, 25))
        self.userNameLabel = wx.StaticText(self, label = "UserName", pos = (40, 100), size = (120, 25))
        self.serverAddress = wx.TextCtrl(self, pos = (120, 47), size = (150, 25))
        self.userName = wx.TextCtrl(self, pos = (120, 97), size = (150, 25))
        self.loginButton = wx.Button(self, label = 'Login', pos = (80, 145), size = (130, 30))
        # self.loginButton.Bind(wx.EVT_BUTTON, self.login)
        AsyncBind(wx.EVT_BUTTON, self.login, self.loginButton)
        self.Show()

    async def login(self, event):
        '''登录处理'''
        try:
            if not self.reader and not self.writer:
                serverAddress = self.serverAddress.GetLineText(0).split(':')
                try:
                    self.reader, self.writer = await asyncio.open_connection(
                        serverAddress[0], serverAddress[1], loop=self.loop)
                except Exception:
                    raise

                name = str(self.userName.GetLineText(0))
                _MESSAGE_REG['uid'] = name

                msg = json.dumps(_MESSAGE_REG)
                msg_len = len(msg)
                packed_msg = pack("!i%ds" % msg_len, msg_len, bytes(msg, encoding='utf-8'))
                self.writer.write(packed_msg)
                await self.writer.drain()
                response = await self.reader.read(1024)
                if response.decode() == 'EXIST':
                    wx.MessageBox("Account Exist!", "ERROR" ,wx.OK | wx.ICON_INFORMATION)
                    return
                else:
                    self.Close()
                    ChatFrame(None, -2, title='Chat Client', size=(500, 350), 
                        reader=self.reader, writer=self.writer)
        except Exception:
            wx.MessageBox("Something Wrong!", "ERROR" ,wx.OK | wx.ICON_INFORMATION)


class ChatFrame(wx.Frame):
    """
    聊天窗口
    """
    def __init__(self, parent, id, title, size, reader, writer):
        '''初始化，添加控件并绑定事件'''
        wx.Frame.__init__(self, parent, id, title)
        self.reader, self.writer = reader, writer
        self.SetSize(size)
        self.Center()
        self.chatFrame = wx.TextCtrl(self, pos = (5, 5), size = (490, 310), style = wx.TE_MULTILINE | wx.TE_READONLY)
        self.message = wx.TextCtrl(self, pos = (5, 320), size = (300, 25))
        self.sendButton = wx.Button(self, label = "Send", pos = (310, 320), size = (58, 25))
        self.usersButton = wx.Button(self, label = "Users", pos = (373, 320), size = (58, 25))
        self.closeButton = wx.Button(self, label = "Close", pos = (436, 320), size = (58, 25))
        # self.sendButton.Bind(wx.EVT_BUTTON, self.send)
        # self.usersButton.Bind(wx.EVT_BUTTON, self.lookUsers)
        # self.closeButton.Bind(wx.EVT_BUTTON, self.close)
        AsyncBind(wx.EVT_BUTTON, self.send, self.sendButton)
        AsyncBind(wx.EVT_BUTTON, self.lookUsers, self.usersButton)
        AsyncBind(wx.EVT_BUTTON, self.close, self.closeButton)
        StartCoroutine(self.receive, self)
        self.Show()

    async def send(self, event):
        '''发送消息'''
        message = str(self.message.GetLineText(0)).strip()
        if message != '':
          con.write('say ' + message + '\n')
          self.message.Clear()

    async def lookUsers(self, event):
        '''查看当前在线用户'''
        con.write('look\n')

    async def close(self, event):
        '''关闭窗口'''
        del self.reader, self.writer
        self.Close()

    async def receive(self):
        '''接受服务器的消息'''
        while True:
            sleep(0.6)
            result = await self.reader.read(1024)
            if result != '':
                self.chatFrame.AppendText(result)


if __name__ == '__main__':
    app = WxAsyncApp()
    LoginFrame(None, -1, title = "Login", size = (280, 200))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.MainLoop())
