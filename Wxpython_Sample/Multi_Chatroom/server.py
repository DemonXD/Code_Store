import socket
import asyncio


class EndSession(Exception):
    """
    自定义会话结束时的异常
    """
    pass


class CommandHandler:
    """
    命令处理类
    """
    def unknown(self, session, cmd):
        '''响应未知命令'''
        session.push('Unknown command: %s\n' % cmd)

    def handle(self, session, line):
        '''命令处理'''
        if not line.strip():
            return
        parts = line.split(' ', 1)
        cmd = parts[0]
        try:
            line = parts[1].strip()
        except IndexError:
            line = ''
        meth = getattr(self, 'do_' + cmd, None)
        try:
            meth(session, line)
        except TypeError:
            self.unknown(session, cmd)


class Room(CommandHandler):
    """
    包含多个用户的环境，负责基本的命令处理和广播
    """
    def __init__(self, server):
        self.server = server
        self.sessions = []
    def add(self, session):
        '''一个用户进入房间'''
        self.sessions.append(session)
    def remove(self, session):
        '''一个用户离开房间'''
        self.sessions.remove(session)
    def broadcast(self, line):
        '''向所有的用户发送指定消息'''
        for session in self.sessions:
            session.push(line)
    def do_logout(self, session, line):
        '''退出房间'''
        raise EndSession("logout")


class LoginRoom(Room):
    """
    刚登录的用户的房间
    """
    def add(self, session):
        '''用户连接成功的回应'''
        Room.add(self, session)
        session.push('Connect Success')

    def do_login(self, session, line):
        '''登录命令处理'''
        name = line.strip()
        if not name:
            session.push('UserName Empty')
        elif name in self.server.users:
            session.push('UserName Exist')
        else:
            session.name = name
            session.enter(self.server.main_room)


class LogoutRoom(Room):
    """
    用户退出时的房间
    """
    def add(self, session):
        '''从服务器中移除'''
        try:
            del self.server.users[session.name]
        except KeyError:
            pass


class ChatRoom(Room):
    """
    聊天用的房间
    """
    def add(self, session):
        '''广播新用户进入'''
        session.push('Login Success')
        self.broadcast(session.name + ' has entered the room.\n')
        self.server.users[session.name] = session
        Room.add(self, session)
    def remove(self, session):
        '''广播用户离开'''
        Room.remove(self, session)
        self.broadcast(session.name + ' has left the room.\n')
    def do_say(self, session, line):
        '''客户端发送消息'''
        self.broadcast(session.name + ': ' + line + '\n')
    def do_look(self, session, line):
        '''查看在线用户'''
        session.push('Online Users:\n')
        for other in self.sessions:
            session.push(other.name + '\n')


class ChatSession():
    """
    负责数据的接受发送，维护用户会话
    """
    def __init__(self, ):
        self.server = server

        self.data = []
        self.name = None
        self.enter(LoginRoom(server))

    async def data_handle(self, reader, writer):
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))

        print("Send: %r" % message)
        writer.write(data)
        await writer.drain()

        # print("Close the client socket")
        # writer.close()

    def enter(self, room):
        '''退出当前房间进入指定房间'''
        pass


class ChatServer():
    """
    聊天服务器
    """
    def __init__(self, loop: asyncio.BaseEventLoop, host: str, port: str):
        self.loop = loop
        self.coro = asyncio.start_server()
        self.loop.create_connection(host=host, port=port)
        self.users = {}
        self.main_room = ChatRoom(self)

    def _run(self):
        

    def run_server(self):
        self._run()


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 6666
    s = ChatServer(PORT)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print()
