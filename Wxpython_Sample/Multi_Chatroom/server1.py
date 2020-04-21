import asyncio
import logging
# XXX: REMOVE THIS LINE IN PRODUCTION!
logging.basicConfig(format='%(asctime)s %(lineno)d %(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

users = {}

async def handle_login(data):
    if data:
        if not data.strip():
            return
        parts = data.split(' ', 1)
        cmd = parts[0]
        try:
            data = parts[1].strip()
        except IndexError:
            data = ''
        if 'login' == cmd.strip():
            if users.get(data.strip()):
                return "UserName Exist"
            elif data == '':
                return "UserName Empty"
            else:
                users[data.strip()] = True
                return True
        else:
            return data

async def handle_dispatch_room():
    pass


async def broadcast():
    pass


# Connected client records
clients = dict()


async def show_tasks():
    """FOR DEBUGGING"""
    while True:
        await asyncio.sleep(5)
        logger.debug(asyncio.Task.all_tasks())


def client_connected_cb(client_reader, client_writer):
    # Use peername as client ID
    client_id = client_writer.get_extra_info('peername')

    logger.info('Client connected: {}'.format(client_id))

    # Define the clean up function here
    def client_cleanup(fu):
        logger.info('Cleaning up client {}'.format(client_id))
        try:  # Retrievre the result and ignore whatever returned, since it's just cleaning
            fu.result()
        except Exception as e:
            pass
        # Remove the client from client records
        del clients[client_id]

    task = asyncio.create_task(client_task(client_reader, client_writer))
    task.add_done_callback(client_cleanup)
    # Add the client and the task to client records
    clients[client_id] = task


async def client_task(reader, writer):
    client_addr = writer.get_extra_info('peername')
    logger.info('Start echoing back to {}'.format(client_addr))

    while True:
        data = await reader.read(1024)
        if data == b'':
            logger.info('Received EOF. Client disconnected.')
            return
        else:
            writer.write(data)
            await writer.drain()


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 6666
    loop = asyncio.get_event_loop()
    server_coro = asyncio.start_server(client_connected_cb,
                                       host=HOST,
                                       port=PORT,
                                       loop=loop)
    server = loop.run_until_complete(server_coro)

    try:
        logger.info('Serving on {}:{}'.format(HOST, PORT))
        loop.run_forever()
    except KeyboardInterrupt as e:
        logger.info('Keyboard interrupted. Exit.')
    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()