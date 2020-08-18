'''
for list data structure implementation
can inplement by python list: append, pop
Tips:
    LIFO: last in, first out
    Exception: underflow, overflow
'''
class UNDERFLOW(Exception):
    pass


class OVERFLOW(Exception):
    pass


class Stack:
    '''
    top is the curser to show the current value in stack
    :paras size: initial stack size
    '''
    def __init__(self, size):
        self.top = -1
        self.S = [0 for _ in range(0, size)]
        self.size = size
    STACK_EMPTY = lambda self: self.top == -1
    STACK_FULL = lambda self: self.top == self.size - 1

    def PUSH(self, value):
        if self.STACK_FULL():
            raise OVERFLOW("Stack is full!")
        self.top += 1
        self.S[self.top] = value
    
    def POP(self):
        if self.STACK_EMPTY():
            raise UNDERFLOW("Stack is empty!")
        pop_value = self.S[self.top]
        self.top -= 1
        return pop_value


if __name__ == "__main__":
    st = Stack(5)
    # PUSH 5 items
    for i in range(5):
        st.PUSH(i)
    # now there are 5 items in Stack: [0, 1, 2, 3, 4]
    try:
        st.PUSH(6)
    except OVERFLOW:
        print("stack is full!")
    
    # pop 5 items from Stack
    for _ in range(5):
        st.POP()
    # not the Stack is empty
    try:
        st.POP()
    except UNDERFLOW:
        print("stack is empty")