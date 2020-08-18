'''
for queue data structure implementation
python official lib: collections.deque
Tips:
    FIFO: first in, first out
    the real amount of queue is size - 1
    Exception: underflow, overflow
'''
class UNDERFLOW(Exception):
    pass


class OVERFLOW(Exception):
    pass


class Queue:
    def __init__(self, size):
        self.head = self.tail = 0
        self.S = [0 for _ in range(0, size)]
        self.size = size

    QUEUE_EMPTY = lambda self: self.head == self.tail
    QUEUE_FULL = lambda self: self.head == (self.tail + 1) % self.size

    # insert into queue
    def ENQUEUE(self, value):
        if self.QUEUE_FULL(): raise OVERFLOW("the queue is full")
        self.S[self.tail] = value
        self.tail = (self.tail+1) % self.size
    # delete from queue
    def DEQUEUE(self):
        if self.QUEUE_EMPTY(): raise UNDERFLOW("the queue is empty")
        del_value = self.S[self.head]
        self.head = (self.head+1) % self.size
        return del_value


if __name__ == "__main__":
    q = Queue(5)
    # PUSH 4 items
    for i in range(4):
        q.ENQUEUE(i)
    #                                            valid
    #                                              ⬇
    # now there are 4 items in Stack: [0, 1, 2, 3, 0]
    try:
        q.ENQUEUE(5)
    except OVERFLOW:
        print("queue is full!")
    
    # pop 5 items from Stack
    for _ in range(4):
        q.DEQUEUE()
    # not the Stack is empty
    try:
        q.DEQUEUE()
    except UNDERFLOW:
        print("queue is empty")