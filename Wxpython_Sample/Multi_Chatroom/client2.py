import asyncio
import socket
import json
import random
from struct import pack


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


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        print("send data......")
        msg = json.dumps(_MESSAGE_REG)
        msg_len = len(msg)
        packed_msg = pack("!i%ds" % msg_len, msg_len, bytes(msg, encoding='utf-8'))
        transport.write(packed_msg)

        msg2 = json.dumps(_MESSAGE_TEXT)
        msg_len2 = len(msg2)
        packed_msg2 = pack("!i%ds" % msg_len2, msg_len2, bytes(msg2, encoding='utf-8'))
        transport.write(packed_msg2)

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

try:
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: EchoClientProtocol(loop),
                                '127.0.0.1', 6666)
    loop.run_until_complete(coro)
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.close()
