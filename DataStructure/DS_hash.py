'''
hash table implementation
python official lib: dict
'''

# based on linked list
class Node:
    def __init__(self, data):
        self.next_node = None
        self.data = data
    
    def set_next(self, node):
        self.next_node = node
    
    def get_next(self):
        return self.next_node

    def get_data(self):
        return self.data

    def data_equals(self, data):
        return self.data == data


# store nums
class HashTable:
    def __init__(self, n: int):
        self.value = [None] * n
        self.n = n

    def insert(self, data):
        if self.search(data):
            return True

        i = data % self.n
        node = Node(data)
        if self.value[i] is None:
            self.value[i] = node
            return True
        else:
            head = self.value[i]
            while head.get_next() is not None:
                head = head.get_next()
            head.set_next(node)
            return True

    def search(self, data):
        i = data % self.n
        if self.value[i] is None:
            return False
        else:
            head = self.value[i]
            while head and not head.data_equals(data):
                head = head.get_next()
            if head:
                return head
            else:
                return False

    def delete(self, data):
        if self.search(data):
            i = data % self.n
            if self.value[i].data_equals(data):
                self.value[i] = self.value[i].get_next()
            else:
                head = self.value[i]
                while not head.get_next().data_equals(data):
                    head = head.get_next()
                head.set_next(head.get_next().get_next())
            return True
        else:
            return False

    def echo(self):
        i = 0
        for head in self.value:
            print(str(i) + ':\t'),
            if head is None:
                print(None)
            else:
                while head is not None:
                    print(str(head.get_data()) + ' ->')
                    head = head.get_next()
                print(None)
            print()
            i += 1
        print()

#-----------------------------------------
# based on rehash
class MyDictionary(object):
    # 字典类的初始化
    def __init__(self):
        self.table_size = 13 # 哈希表的大小
        self.key_list = [None]*self.table_size #用以存储key的列表
        self.value_list = [None]*self.table_size #用以存储value的列表
    
    # 散列函数，返回散列值
    # key为需要计算的key
    def hashfuction(self, key):
        count_char = 0
        key_string = str(key)
        for key_char in key_string: # 计算key所有字符的ASCII值的和
            count_char += ord(key_char) # ord()函数用于求ASCII值
        length = len(str(count_char))
        if length > 3 : # 当和的位数大于3时，使用平方取中法，保留中间3位
            mid_int = 100*int((str(count_char)[length//2-1])) \
                    + 10*int((str(count_char)[length//2])) \
                    + 1*int((str(count_char)[length//2+1]))
        else: # 当和的位数小于等于3时，全部保留
            mid_int = count_char
            
        return mid_int%self.table_size # 取余数作为散列值返回
        
    # 重新散列函数，返回新的散列值
    # hash_value为旧的散列值
    def rehash(self, hash_value):
        return (hash_value+3)%self.table_size #向前间隔为3的线性探测
        
    # 存放键值对
    def __setitem__(self, key, value):
        hash_value = self.hashfuction(key) #计算哈希值
        if None == self.key_list[hash_value]: #哈希值处为空位，则可以放置键值对
            pass
        elif key == self.key_list[hash_value]: #哈希值处不为空，旧键值对与新键值对的key值相同，则作为更新，可以放置键值对
            pass
        else: #哈希值处不为空，key值也不同，即发生了“冲突”，则利用重新散列函数继续探测，直到找到空位
            hash_value = self.rehash(hash_value) # 重新散列
            while (None != self.key_list[hash_value]) and (key != self.key_list[hash_value]): #依然不能插入键值对，重新散列
                hash_value = self.rehash(hash_value) # 重新散列
        #放置键值对      
        self.key_list[hash_value] = key
        self.value_list[hash_value] = value

    # 根据key取得value
    def __getitem__(self, key):
        hash_value = self.hashfuction(key) #计算哈希值
        first_hash = hash_value #记录最初的哈希值，作为重新散列探测的停止条件
        if None == self.key_list[hash_value]: #哈希值处为空位，则不存在该键值对
            return None
        elif key == self.key_list[hash_value]: #哈希值处不为空，key值与寻找中的key值相同，则返回相应的value值
            return self.value_list[hash_value]
        else: #哈希值处不为空，key值也不同，即发生了“冲突”，则利用重新散列函数继续探测，直到找到空位或相同的key值
            hash_value = self.rehash(hash_value) # 重新散列
            while (None != self.key_list[hash_value]) and (key != self.key_list[hash_value]): #依然没有找到，重新散列
                hash_value = self.rehash(hash_value) # 重新散列
                if hash_value == first_hash: #哈希值探测重回起点，判断为无法找到了
                    return None
            #结束了while循环，意味着找到了空位或相同的key值
            if None == self.key_list[hash_value]: #哈希值处为空位，则不存在该键值对
                return None
            else: #哈希值处不为空，key值与寻找中的key值相同，则返回相应的value值
                return self.value_list[hash_value]
    
    # 删除键值对
    def __delitem__(self, key):
        hash_value = self.hashfuction(key) #计算哈希值
        first_hash = hash_value #记录最初的哈希值，作为重新散列探测的停止条件
        if None == self.key_list[hash_value]: #哈希值处为空位，则不存在该键值对，无需删除
            return
        elif key == self.key_list[hash_value]: #哈希值处不为空，key值与寻找中的key值相同，则删除
            self.key_list[hash_value] = None
            self.value_list[hash_value] = None
            return
        else: #哈希值处不为空，key值也不同，即发生了“冲突”，则利用重新散列函数继续探测，直到找到空位或相同的key值
            hash_value = self.rehash(hash_value) # 重新散列
            while (None != self.key_list[hash_value]) and (key != self.key_list[hash_value]): #依然没有找到，重新散列
                hash_value = self.rehash(hash_value) # 重新散列
                if hash_value == first_hash: #哈希值探测重回起点，判断为无法找到了
                    return
            #结束了while循环，意味着找到了空位或相同的key值
            if None == self.key_list[hash_value]: #哈希值处为空位，则不存在该键值对
                return
            else: #哈希值处不为空，key值与寻找中的key值相同，则删除
                self.key_list[hash_value] = None
                self.value_list[hash_value] = None
                return
    
    # 返回字典的长度
    def __len__(self):
        count = 0
        for key in self.key_list:
            if key != None:
                count += 1
        return count


if __name__ == '__main__':
    # linked list
    # hashTable = HashTable(10)
    # hashTable.insert(10)
    # hashTable.insert(11)
    # hashTable.insert(1)
    # hashTable.echo()
    # hashTable.delete(1)
    # hashTable.echo()
    #-------------------------