'''
for list data structure implementation
python official lib: heapq is the min heap
min heap:
    S[0] is the minimum
max heap:
    S[0] is the maximum
'''
from typing import Any, List 

# max heap

class UNDERFLOW(Exception):pass
class OVERFLOW(Exception):pass
class BADVALUE(Exception): pass


class Heap:
    def __init__(self, A: List):
        self.S = A[:]
        self.size = self.heap_size = len(A)
        self._BUILD_MAX_HEAP()
    
    PARENT = lambda self, i: i/2 # get the i's parent node index
    LETF = lambda self, i: 2*i # get the i's left sub tree root index
    RIGHT = lambda self, i: 2*i + 1 # get the i's right sub tree root index
    
    def MAX_HEAPIFY(self, i):
        left, right = self.LEFT(i), self.RIGHT(i)
        largest = left if left < self.heap_size and self.S[left] > self.S[i] else i
        largest = right if right < self.heap_size and self.S[right] > self.S[largest] else largest
        if largest != i:
            self.S[i], self.S[largest] = self.S[largest], self.S[i]
            self.MAX_HEAPIFY(largest)
    
    def _BUILD_MAX_HEAP(self): # build max heap
        for i in range(self.PARENT(self.size-1),-1,-1):
            self.MAX_HEAPIFY(i)
    
    # max priority queue
    def INSERT(self, key): # insert key to heap
        if self.heap_size >= self.size: raise OVERFLOW("the heap is full")
        self.heap_size += 1
        self.S[self.heap_size-1] = float('-INF')
        self.INCREASE_KEY(self.heap_size-1, key)

    def MAXIMUM(self): # return the maximum value
        return self.S[0]

    def EXTRACT_MAX(self): # del and return the maximum value
        if self.heap_size < 1: raise UNDERFLOW("the heap is empty")
        max = self.S[0]
        self.S[0] = self.S[self.heap_size-1]
        self.heap_size -= 1
        self.MAX_HEAPIFY(0)
        return max
        
    def INCREASE_KEY(self, i, key): # 将下标为i的值增加到key值，维护最大堆
        if self.S[i] > key: raise BADVALUE("new key is smaller than current key")
        self.S[i] = key
        while i> 0 and self.S[i] > self.S[self.PARENT(i)]:
            self.S[i], self.S[self.PARENT(i)] = self.S[self.PARENT(i)], self.S[i]
            i = self.PARENT(i)