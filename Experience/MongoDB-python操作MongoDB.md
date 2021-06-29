*   基于pymongo

对于为创建的db，python操作的时候，只有在插入一条数据后才真正的创建db；

```python
#!/usr/bin/python3
 
import pymongo
 
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
 
dblist = myclient.list_database_names()
if "runoobdb" in dblist:
  print("数据库已存在！")

# 创建db
mydb = myclient["testdb"]
# 列出所有集合
collist = mydb.list_collection_names()

# 创建集合collection
mycol = mydb["sites"]
```

**增删改查：**

```python
import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
# 获取db
db = client['testdb']
# 获取集合
coll = db['test']

# 插入一条
val1 = coll.insert_one({"x": 1})
# 打印插入数据的id
print(val1.inserted_id)

# 插入多条
vals = coll.insert_many(
  { "name": "Taobao", "alexa": "100", "url": "https://www.taobao.com" },
  { "name": "QQ", "alexa": "101", "url": "https://www.qq.com" },
  { "name": "Facebook", "alexa": "10", "url": "https://www.facebook.com" },
  { "name": "知乎", "alexa": "103", "url": "https://www.zhihu.com" },
  { "name": "Github", "alexa": "109", "url": "https://www.github.com" }
)
# 打印所有插入数据的id
print(vals.inserted_ids)

# 也可以指定_id 插入数据
```

```python
import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
mycol = client["testdb"]{"test"]

# 改单条数据
myquery = { "alexa": "10000" }
newvalues = { "$set": { "alexa": "12345" } }
 
mycol.update_one(myquery, newvalues)
 
# 输出修改后的  "sites"  集合
for x in mycol.find():
  print(x)
                         
# 改多条数据
myquery = { "name": { "$regex": "^F" } }
newvalues = { "$set": { "alexa": "123" } }
 
x = mycol.update_many(myquery, newvalues)
```

```python
#!/usr/bin/python3
 
import pymongo
 
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["runoobdb"]
mycol = mydb["sites"]
 
# 数据排序
mydoc = mycol.find().sort("alexa")
for x in mydoc:
  print(x)
```

```python
import pymongo
 
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["runoobdb"]
mycol = mydb["sites"]
 
myquery = { "name": "Taobao" }
 
mycol.delete_one(myquery)
 
# 删除后输出
for x in mycol.find():
  print(x)
  
# 删除多条
myquery = { "name": {"$regex": "^F"} }
 
x = mycol.delete_many(myquery)
 
print(x.deleted_count, "个文档已删除")

# 删除集合中所有
x = mycol.delete_many({})
 
print(x.deleted_count, "个文档已删除")

# 删除集合
mycol.drop()
```

**封装类：**

```python
"""
mongodb_operation 静态方法 用来和mongodb 操作交互 
"""


class BaseHandle(object):
    @staticmethod
    def insert_one(collection, data):
        """直接使用insert() 可以插入一条和插入多条 不推荐 明确区分比较好"""
        res = collection.insert_one(data)
        return res.inserted_id

    @staticmethod
    def insert_many(collection, data_list):
        res = collection.insert_many(data_list)
        return res.inserted_ids

    @staticmethod
    def find_one(collection, data, data_field={}):
        if len(data_field):
            res = collection.find_one(data, data_field)
        else:
            res = collection.find_one(data)
        return res

    @staticmethod
    def find_many(collection, data, data_field={}):
        """ data_field 是指输出 操作者需要的字段"""
        if len(data_field):
            res = collection.find(data, data_field)
        else:
            res = collection.find(data)
        return res

    @staticmethod
    def update_one(collection, data_condition, data_set):
        """修改一条数据"""
        res = collection.update_one(data_condition, data_set)
        return res

    @staticmethod
    def update_many(collection, data_condition, data_set):
        """ 修改多条数据 """
        res = collection.update_many(data_condition, data_set)
        return res

    @staticmethod
    def replace_one(collection, data_condition, data_set):
        """ 完全替换掉 这一条数据， 只是 _id 不变"""
        res = collection.replace_one(data_condition, data_set)
        return res

    @staticmethod
    def delete_many(collection, data):
        res = collection.delete_many(data)
        return res

    @staticmethod
    def delete_one(collection, data):
        res = collection.delete_one(data)
        return res

    @staticmethod
    def find_count(collection, data):
        res = collection.find(data).count()
        return res


'''
mongodb_base 和mongo 连接的信息 
'''


class DBBase(object):
    """ 各种query 中的数据 data 和 mongodb 文档中的一样"""

    def __init__(self, collection):
        self.mg = MG()
        self.collection = self.mg.db[collection]

    def insert_one(self, data):
        res = BaseHandle.insert_one(self.collection, data)
        return res

    def insert_many(self, data_list):
        res = BaseHandle.insert_many(self.collection, data_list)
        return res

    def find_count(self, data={}):
        res = BaseHandle.find_count(self.collection, data)
        return res

    #  ========================= Query Documents Start =========

    def find_one(self, data, data_field={}):
        res = BaseHandle.find_one(self.collection, data, data_field)
        return res

    def find_many(self, data, data_field={}):
        """ 有多个键值的话就是 AND 的关系"""
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_all(self, data={}, data_field={}):
        """select * from table"""
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_in(self, field, item_list, data_field={}):
        """SELECT * FROM inventory WHERE status in ("A", "D")"""
        data = dict()
        data[field] = {"$in": item_list}
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_or(self, data_list, data_field={}):
        """db.inventory.find(
    {"$or": [{"status": "A"}, {"qty": {"$lt": 30}}]})

        SELECT * FROM inventory WHERE status = "A" OR qty < 30
        """
        data = dict()
        data["$or"] = data_list
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_between(self, field, value1, value2, data_field={}):
        """获取俩个值中间的数据"""
        data = dict()
        data[field] = {"$gt": value1, "$lt": value2}
        # data[field] = {"$gte": value1, "$lte": value2} # <>   <= >=
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_more(self, field, value, data_field={}):
        data = dict()
        data[field] = {"$gt": value}
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_less(self, field, value, data_field={}):
        data = dict()
        data[field] = {"$lt": value}
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_like(self, field, value, data_field={}):
        """ where key like "%audio% """
        data = dict()
        data[field] = {'$regex': '.*' + value + '.*'}
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def query_limit(self, query, num):
        """db.collection.find(<query>).limit(<number>) 获取指定数据"""
        res = query.limit(num)
        return res

    def query_count(self, query):
        res = query.count()
        return res

    def query_skip(self, query, num):
        res = query.skip(num)
        return res

    def query_sort(self, query, data):
        """db.orders.find().sort( { amount: -1 } ) 根据amount 降序排列"""
        res = query.sort(data)
        return res

    def delete_one(self, data):
        """ 删除单行数据 如果有多个 则删除第一个"""
        res = BaseHandle.delete_one(self.collection, data)
        return res

    def delete_many(self, data):
        """ 删除查到的多个数据 data 是一个字典 """
        res = BaseHandle.delete_many(self.collection, data)
        return res
```