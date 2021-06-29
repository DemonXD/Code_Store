**操作封装：**

```python
# -*- coding: UTF-8 -*-
import psycopg2

class PGHelper:
    def __init__(self, host, db, user, pwd, port):
        self.host = host
        self.db = db
        self.user = user
        self.pwd = pwd
        self.port = port
        self._conn = self._connect()
        self._cursor = self._conn.cursor()

    def try_except(self):
        def wrapper(*args, **kwargs):
            try:
                self(*args, **kwargs)
            except Exception as e:
                print("get error: %s" % e)
        return wrapper

    @try_except
    def _connect(self):
        return psycopg2.connect(
            database=self.db,
            user=self.user,
            password=self.pwd,
            host=self.host,
            port=self.port)

    @try_except
    def select(self, sqlCode):
        self.execute(sqlCode)
        return self.cursor.fetchall()

    def insert(self, sqlCode):
        self.common(sqlCode)

    def update(self, sqlCode):
        self.common(sqlCode)

    def delete(self, sqlCode):
        self.common(sqlCode)

    def close(self):
        self._cursor.close()
        self._conn.close()

    def insertAndGetField(self, sql_code, field):
        """
        插入数据，并返回当前 field
        :param sql_code:
        :param field:
        :return:
        """
        try:
            self.cursor.execute(sql_code + " RETURNING " + field)
        except Exception as e:
            print(e)
            self.conn.rollback()
            self.cursor.execute(sql_code + " RETURNING " + field)
        self.conn.commit()

        return self.cursor.fetchone()

    def common(self, sqlCode):
        try:
            self.cursor.execute(sqlCode)
        except Exception as e:
            print(e)
            self.conn.rollback()
            self.cursor.execute(sqlCode)
        self.conn.commit()

    def __del__(self):
        self.close()


if __name__ == '__main__':
    pghelper = PGHelper(host="***",db="***",user="***",pwd="***",port="***")
```