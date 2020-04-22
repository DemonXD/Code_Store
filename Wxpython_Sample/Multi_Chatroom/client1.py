import wx
from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
import asyncio
from asyncio.events import get_event_loop
import time

_MESSAGE_TEXT = {
   'type': 'text',
    'sender': 'niuminguo',
    'receiver': 'niuminguo',
    'content': 'love',
}

_MESSAGE_REG = {
    'uid': 'niuminguo',
    'type': 'register',
}

_MESSAGE_LOGOUT = {
    'uid': 'somebody',
    'type': 'unregister',
}

class TestFrame(wx.Frame):
    def __init__(self, parent=None):
        super(TestFrame, self).__init__(parent)
        self.reader, self.writer = None, None
        self.loop = asyncio.get_event_loop()
        vbox = wx.BoxSizer(wx.VERTICAL)
        button1 =  wx.Button(self, label="Submit")
        self.edit =  wx.StaticText(self, style=wx.ALIGN_CENTRE_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        self.edit_timer =  wx.StaticText(self, style=wx.ALIGN_CENTRE_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        vbox.Add(button1, 2, wx.EXPAND|wx.ALL)
        vbox.AddStretchSpacer(1)
        vbox.Add(self.edit, 1, wx.EXPAND|wx.ALL)
        vbox.Add(self.edit_timer, 1, wx.EXPAND|wx.ALL)
        self.SetSizer(vbox)
        self.Layout()
        AsyncBind(wx.EVT_BUTTON, self.async_callback, button1)
        StartCoroutine(self.update_clock, self)

    async def async_callback(self, event):
        if not self.reader and not self.writer:
            self.reader, self.writer = await asyncio.open_connection('127.0.0.1', 6666, loop=self.loop)
        
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
        
        # self.writer.write("connected".encode())
        # await self.writer.drain()
        # data = await self.reader.read(100)
        # print(data.decode())
        # self.edit.SetLabel(f"{data.decode()}")
        # await asyncio.sleep(1)

    async def update_clock(self):
        while True:
            self.edit_timer.SetLabel(time.strftime('%H:%M:%S'))
            await asyncio.sleep(0.5)

            
app = WxAsyncApp()
frame = TestFrame()
frame.Show()
app.SetTopWindow(frame)
loop = get_event_loop()
loop.run_until_complete(app.MainLoop())