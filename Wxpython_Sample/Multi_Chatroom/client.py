import wx
import asyncio
from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
from time import sleep


class LoginFrame(wx.Frame):
    """
    登录窗口
    """
    def __init__(self, parent, id, title, size):
        '''初始化，添加控件并绑定事件'''
        wx.Frame.__init__(self, parent, id, title)
        self.loop = asyncio.get_event_loop()
        self.reader, self.writer = asyncio.open_connection('127.0.0.1', 6666, loop=self.loop)
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
            serverAddress = self.serverAddress.GetLineText(0).split(':')
            response = con.read_some()
            if response != 'Connect Success':
                self.showDialog('Error', 'Connect Fail!', (95, 20))
                return
            con.write('login ' + str(self.userName.GetLineText(0)) + '\n')
            response = con.read_some()
            if response == 'UserName Empty':
                self.showDialog('Error', 'UserName Empty!', (135, 20))
            elif response == 'UserName Exist':
                self.showDialog('Error', 'UserName Exist!', (135, 20))
            else:
                self.Close()
                ChatFrame(None, -2, title = 'Chat Client', size = (500, 350))
        except Exception:
            self.showDialog('Error', 'Connect Fail!', (95, 20), (reader, writer))

    def showDialog(self, title, content, size):
        '''显示错误信息对话框'''
        dialog = wx.Dialog(self, title = title, size = size)
        dialog.Center()
        wx.StaticText(dialog, label = content)
        dialog.ShowModal()


class ChatFrame(wx.Frame):
    """
    聊天窗口
    """
    def __init__(self, parent, id, title, size, con_tuple: tuple = None):
        '''初始化，添加控件并绑定事件'''
        wx.Frame.__init__(self, parent, id, title)
        self.reader, self.writer = con_tuple if con_tuple else None, None
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
        con.write('logout\n')
        con.close()
        self.Close()

    async def receive(self):
        '''接受服务器的消息'''
        while True:
            sleep(0.6)
            result = con.read_very_eager()
            if result != '':
                self.chatFrame.AppendText(result)


if __name__ == '__main__':
    app = WxAsyncApp()

    LoginFrame(None, -1, title = "Login", size = (280, 200))
    app.MainLoop()

    # frame = TestFrame()
    # frame.Show()
    # app.SetTopWindow(frame)
    loop = get_event_loop()
    loop.run_until_complete(app.MainLoop())