from abc import abstractclassmethod
import base64
import zlib

data_store = []

class DataSource:
    @abstractclassmethod
    def writeData(self, data):
        pass

    @abstractclassmethod
    def readData(self):
        pass


class StreamDataSource(DataSource):
    def writeData(self, data):
        print("execute origin decorator!")
        data_store.append(data)

    def readData(self):
        return data_store.pop()

    
class DataSourceDecorator(DataSource):
    def __init__(self, source: DataSource):
        self.wrappee = source
    
    def writeData(self, data):
        self.wrappee.writeData(data)
    
    def readData(self):
        return self.wrappee.readData()


class EncryptionDecorator(DataSourceDecorator):
    def __init__(self, source: DataSource):
        super(EncryptionDecorator, self).__init__(source)
    
    def writeData(self, data):
        print("execute encryt decorator!")
        self.wrappee.writeData(base64.b64encode(data.encode()))
    
    def readData(self):
        return base64.b64decode(self.wrappee.readData()).decode()


class CompressDecorator(DataSourceDecorator):
    def __init__(self, source: DataSource):
        super(CompressDecorator, self).__init__(source)
    
    def writeData(self, data):
        print("execute compress decorator!")
        self.wrappee.writeData(zlib.compress(data))

    def readData(self):
        return zlib.decompress(self.wrappee.readData())

if __name__ == "__main__":
    # 按需求添加一个或者多个
    # 执行过程由外到内
    # 对操作对象进行层层处理
    source = StreamDataSource()
    source = CompressDecorator(source)
    source = EncryptionDecorator(source)
    source.writeData("i am data")
    print(data_store[0])
    readData = source.readData()
    print(readData)