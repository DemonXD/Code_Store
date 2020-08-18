import re
import wx
import asyncio
import json
from collections import Counter
from struct import pack
from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
from time import sleep

"""
types:['text', 'register', 'unregister', 'cmd', 'unknown]
"""

# 返回消息状态
_MESSAGE_TEXT = {
    'type': 'text',
    'sender': '',
    'receiver': 'all',
    'content': 'love',
    'back_status': 'None'
}

# 不返回消息
_MESSAGE_REG = {
    'type': 'register',
    'uid': '',
}

# 返回命令执行状态
_MESSAGE_CMD = {
    'type': 'cmd',
    'sender': '',
    'request': "",
    'data': [],
    'status': 'None'
}

_CUR_USERS = [None]


class LoginFrame(wx.Frame):
    """
    登录窗口
    """
    def __init__(self, parent, id, title, size):
        '''初始化，添加控件并绑定事件'''
        wx.Frame.__init__(self, parent, id, title)
        self.loop = asyncio.get_event_loop()
        self.reader, self.writer = None, None
        self.SetSize(size)
        self.Center()
        self.serverAddressLabel = wx.StaticText(self, label = "Server Address", pos = (10, 50), size = (120, 25))
        self.userNameLabel = wx.StaticText(self, label = "UserName", pos = (40, 100), size = (120, 25))
        self.serverAddress = wx.TextCtrl(self, pos = (120, 47), size = (150, 25))
        self.userName = wx.TextCtrl(self, pos = (120, 97), size = (150, 25))
        self.loginButton = wx.Button(self, label = 'Login', pos = (80, 145), size = (130, 30))
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
                _MESSAGE_TEXT['sender'] = name
                _MESSAGE_CMD['sender'] = name

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
                    ChatFrame(None, -2, title='Chat Client', size=(610, 380), 
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
        self.chatFrame = wx.TextCtrl(self, pos = (5, 5), size = (445, 320),
                        style = wx.TE_MULTILINE | wx.TE_READONLY)
        self.message = wx.TextCtrl(self, pos = (5, 330), size = (300, 25),
                        style = wx.TE_PROCESS_ENTER)
        self.sendButton = wx.Button(self, label = "发送", pos = (310, 330),
                        size = (65, 25))

        self.closeButton = wx.Button(self, label = "注销", pos = (380, 330),
                        size = (65, 25))

        self.userlist = wx.TextCtrl(self, pos = (455, 5), size = (150, 350),
                        style = wx.TE_MULTILINE | wx.TE_READONLY)

        AsyncBind(wx.EVT_BUTTON, self.send, self.sendButton)
        AsyncBind(wx.EVT_TEXT_ENTER, self.send, self.message)
        AsyncBind(wx.EVT_BUTTON, self.close, self.closeButton)
        StartCoroutine(self.receive, self)
        StartCoroutine(self.lookUsers, self)
        self.Show()

    async def send(self, event):
        '''发送消息
        default: 发送给所有人
        @person: 单独可见
        '''
        message = str(self.message.GetLineText(0)).strip()
        if message != "":
            _MESSAGE_TEXT['content'] = message
            if message.startswith('@'):
                # 执行判断操作，是否是@某人私密发送
                for each_user in [user for user in _CUR_USERS if user != _MESSAGE_REG['uid']]:
                    if message.startswith((f'@{each_user},', f'@{each_user}，')):
                        cp_MESSAGE_TEXT = _MESSAGE_TEXT
                        cp_MESSAGE_TEXT['receiver'] = each_user
                        cp_MESSAGE_TEXT['content'] = re.sub(r"@%s(,|，)"%(each_user), "", message).strip()
                        msg = json.dumps(cp_MESSAGE_TEXT)
                        msg_len = len(msg)
                        packed_msg = pack("!i%ds" % msg_len, msg_len, bytes(msg, encoding='utf-8'))
                        self.writer.write(packed_msg)
                        await self.writer.drain()
                        return
            # 发送给所有人
            _MESSAGE_TEXT['receiver'] = 'all'
            msg = json.dumps(_MESSAGE_TEXT)
            msg_len = len(msg)
            packed_msg = pack("!i%ds" % msg_len, msg_len, bytes(msg, encoding='utf-8'))
            self.writer.write(packed_msg)
            await self.writer.drain()

    async def send_back(self, msg):
        self.chatFrame.WriteText(f"{_MESSAGE_REG['uid']}:\t{_MESSAGE_TEXT['content']}" + "\n")
        self.message.Clear()

    async def receive_msg(self, msg):
        """
        handle msg show in frame
        """
        self.chatFrame.WriteText(f"{msg['sender']}:\t{msg['content']}" + "\n")

    async def lookUsers(self):
        '''查看当前在线用户'''
        while True:
            await asyncio.sleep(3)
            try:
                _MESSAGE_CMD['request'] = 'LISTONLINEUSERS'
                msg = json.dumps(_MESSAGE_CMD)
                msg_len = len(msg)
                packed_msg = pack("!i%ds" % msg_len, msg_len, bytes(msg, encoding='utf-8'))
                self.writer.write(packed_msg)
                await self.writer.drain()
            except ConnectionResetError:
                pass

    async def updateUserList(self, users):
        global _CUR_USERS
        if Counter(_CUR_USERS) != Counter(users):
            _CUR_USERS = users
            self.userlist.Clear()
            [self.userlist.WriteText(user+'\n') for user in users if user != _MESSAGE_REG['uid']]

    async def handle_receive_data(self):
        """
        统一处理所有返回消息
        """
        try:
            datas = await self.reader.read(1024)
            if datas:
                datas = json.loads(datas.decode('utf-8'))
                if "text" == datas['type']:
                    if datas['back_status'] == "success":
                        await self.send_back(datas)
                    elif datas['back_status'] == 'None':
                        await self.receive_msg(datas)
                elif "cmd" == datas['type']:
                    if datas['request'] == 'LISTONLINEUSERS' and datas['status'] == "success":
                        await self.updateUserList(datas['data'])
        except ConnectionResetError:
            pass

    async def close(self, event):
        '''关闭窗口'''
        try:
            self.writer.close()
        except Exception:
            wx.MessageBox("Something Wrong!", "ERROR" ,wx.OK | wx.ICON_INFORMATION)
        else:
            self.Close()
            LoginFrame(None, -1, title = "Login", size = (280, 200))

    async def receive(self):
        '''接受服务器的消息'''
        while True:
            await asyncio.sleep(0.2)
            await self.handle_receive_data()


if __name__ == '__main__':
    try:
        app = WxAsyncApp()
        LoginFrame(None, -1, title = "Login", size = (280, 200))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(app.MainLoop())
    except KeyboardInterrupt:
        pass
