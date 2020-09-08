import asyncpg
from asyncpg.pool import Pool
from config.PubManager import PublicManager


class DBHelper:
    _pool: Pool = None

    def __init__(self, db_config: dict) -> None:
        self.db_config = db_config

    async def connect(self):
        if self._pool is not None:
            pass
        else:
            PublicManager.logger.info(f"Connected to server({self.db_config['host']}/{self.db_config['database']}) successfully")
            self._pool = await asyncpg.create_pool(**self.db_config)

    def disconnect(self):
        if self._pool is not None:
            self._pool = None

    async def fetch(self, query):
        await self.connect()
        # Acquire a connection
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                try:
                    result = await connection.fetch(query)
                except Exception as e:
                    PublicManager.logger.info(f"fetch ERROR:{e}")
                else:
                    return result

    # 使用fetch 获取数据样例
    #    sqls = """
    #    select * from devices_device where devicetype = 'agv';
    #    """
    #    devices = await PublicManager.dbpool.fetch(sqls)
    #    results = [{key: val for key, val in each_device.items()} for each_device in devices ]

    async def execute(self, sql, data):
        await self.connect()
        # Acquire a connection
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                try:
                    exc_status = await connection.execute(sql, data)
                    PublicManager.logger.info(f"sql execute return: {exc_status}")
                except Exception as e:
                    PublicManager.logger.info(f"Store ERROR sql:{e}")

    def __del__(self):
        self.disconnect()
        assert self._pool is None