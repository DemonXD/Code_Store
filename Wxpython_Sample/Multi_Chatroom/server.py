import asyncio
import json
from struct import pack


# 消息頭長度 int or uint
_MESSAGE_PREFIX_LENGTH = 4
# 字節序
_BYTE_ORDER = 'big'


class Session(object):

    def __init__(self):

        self.clients = {}

    def get(self, client):
        # Get transport associated by client if exists.
        if client not in self.clients:
            return None
        return self.clients[client]

    def __contains__(self, client):
        # Decide if client is online
        return client in self.clients

    def __repr__(self):
        return "{}".format(self.clients)

    __str__ = __repr__

    def register(self, client, transport):
        """Register client on session"""
        if self.clients.get(client):
            return False
        self.clients[client] = transport
        return True

    def unregister(self, client):
        """Unregister client on session"""
        if client in self.clients:
            del self.clients[client]


class MetaHandler(type):
    """Metaclass for MessageHandler"""
    def __init__(cls, name, bases, _dict):
        try:
            cls._msg_handlers[cls.__msgtype__] = cls
        except AttributeError:
            cls._msg_handlers = {}


class MessageHandler(metaclass=MetaHandler):

    _session = Session()

    def handle(self, msg, transport):
        try:
            _handler = self._msg_handlers[msg['type']]
        except KeyError:
            return ErrorHandler().handler(msg)

        # Handling messages in a asyncio-Task
        # Don’t directly create Task instances: use the async() function
        # or the BaseEventLoop.create_task() method.

        #return _handler().handle(msg, transport)
        return asyncio.create_task(_handler().handle(msg, transport))


class ErrorHandler(MessageHandler):
    """
    Unknown message type
    """
    __msgtype__ = 'unknown'

    def handle(self, msg):
        print("Unknown message type: {}".format(msg))


class Register(MessageHandler):
    """
    Registry handler for handling clients registry.

    Message body should like this:

        {'type': 'register', 'uid': 'unique-user-id'}

    """
    __msgtype__ = 'register'

    def __init__(self):
        self.current_uid = None
        self.transport = None

    async def handle(self, msg, transport):

        self.current_uid = msg['uid']
        self.transport = transport

        print("registe uid: {}".format(self.current_uid))
        # Register user in global session
        if self._session.register(self.current_uid, self.transport):
            msg_pack = "CONNECT"
            self.transport.write(bytes(msg_pack, encoding='utf-8'))
        else:
            msg_pack = "EXIST"
            self.transport.write(bytes(msg_pack, encoding='utf-8'))


class COMMAND(MessageHandler):
    """
    accept client command
    Message body should like this:

        {'type': 'cmd', 'request': 'command'}
    """
    __msgtype__ = "cmd"

    async def handle(self, msg, transport):
        CMD = msg['request']
        if "USER" == CMD:
            msg = {
                "status": "success",
                "users": [user for user in self._session.clients.keys()]
            }
            transport.write(bytes(json.dumps(msg), encoding="utf-8"))


class SendTextMsg(MessageHandler):
    """
    Send message to others.

    Message body should like this:

        {'type': 'text', 'sender': 'Jack', 'receiver': 'Rose', 'content': 'I love you forever'}

    """
    __msgtype__ = 'text'  # Text message

    async def handle(self, msg, _):
        """
        Send message to receiver if receiver is online, and
        save message to mongodb. Otherwise save
        message to mongodb as offline message.
        :param msg:
        :return: None
        """
        print("send data...{}".format(msg))
        riv = msg['receiver']
        if 'all' == riv:
            for each_client, each_sess in self._session.clients.items():
                if each_client != msg['sender']:
                    each_sess.write(bytes(json.dumps(msg), encoding='utf-8'))
            else:
                msg['back_status'] = 'success'
                self._session.get(msg['sender']).write(bytes(json.dumps(msg), encoding="utf-8"))
        else:
            transport = self._session.get(riv)
            msg_pack = json.dumps(msg)
            msg_len = len(msg_pack)
            if transport:
                # Pack message as length-prifixed and send to receiver.
                transport.write(pack("!I%ds" % msg_len, msg_len, bytes(msg_pack, encoding='utf-8')))


class Unregister(MessageHandler):
    """
    Unregister user from global session

    Message body should like this:

        {'type': 'unregister', 'uid': 'unique-user-id'}

    """
    __msgtype__ = 'unregister'

    async def handle(self, msg, _):
        """Unregister user record from global session"""
        self._session.unregister(msg['uid'])


class myImProtocol(asyncio.Protocol):

    _buffer = b''     # 數據緩衝Buffer
    _msg_len = None   # 消息長度

    def data_received(self, data):

        while data:
            data = self.process_data(data)

    def process_data(self, data):
        """
        Called when some data is received.

        This method must be implemented by subclasses

        The argument is a bytes object.
        """
        self._buffer += data

        # For store the rest data out-of a full message
        _buffer = None

        if self._msg_len is None:
            # If buffer length < _MESSAGE_PREFIX_LENGTH return for more data
            if len(self._buffer) < _MESSAGE_PREFIX_LENGTH:
                return

            # If buffer length >= _MESSAGE_PREFIX_LENGTH
            self._msg_len = int.from_bytes(self._buffer[:_MESSAGE_PREFIX_LENGTH], byteorder=_BYTE_ORDER)

            # The left bytes will be the message body
            self._buffer = self._buffer[_MESSAGE_PREFIX_LENGTH:]

        # Received full message
        if len(self._buffer) >= self._msg_len:
            # Call message_received to handler message
            self.message_received(self._buffer[:self._msg_len])

            # Left the rest of the buffer for next message
            _buffer = self._buffer[self._msg_len:]

            # Clean data buffer for next message
            self._buffer = b''

            # Set message length to None for next message
            self._msg_len = None

        return _buffer

    def message_received(self, msg):
        """
        Must override in subclass

        :param msg: the full message
        :return: None
        """
        raise NotImplementedError()


class myIm(myImProtocol):

    def __init__(self):

        self.handler = MessageHandler()

        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def message_received(self, msg):
        """
        The real message handler
        :param msg: a full message without prefix length
        :return: None
        """
        # Convert bytes msg to python dictionary
        msg = json.loads(msg.decode("utf-8"))

        print("receive msg...{}".format(msg))
        # Handler msg
        return self.handler.handle(msg, self.transport)
    
    def connection_lost(self, exc):
        """
        show disconnect msg,
        unregister current connection session
        """
        for each_client, each_trans in self.handler._session.clients.items():
            if self.transport == each_trans:
                print(f"{each_client} disconnected!")
                msg = {'type': 'unregister', 'uid': each_client}
                self.handler.handle(msg, self.transport)


class myImServer(object):
    def __init__(self, protocol_factory, host, port):

        self.host = host
        self.port = port
        self.protocol_factory = protocol_factory

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(loop.create_server(self.protocol_factory, self.host, self.port))
        loop.run_forever()


if __name__ == '__main__':
    try:
        server = myImServer(myIm, '0.0.0.0', 6666)
        server.start()
    except KeyboardInterrupt:
        pass