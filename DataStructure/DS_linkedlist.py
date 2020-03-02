'''
linked list implementation
Tips:
    sigle direction linked list
'''

class ExistNode(Exception): pass
class DoesNotExistNode(ExistNode): pass
class NotSetData(Exception):pass

class Node:
    def __init__(self, data=None):
        # initial the linked-list's head node
        self.data = data
        self.next_node = None

    def set_next(self, node):
        if self.next_node is not None:
            raise ExistNode("Exist node!")
        self.next_node = node
    
    def get_next(self):
        if self.next_node:
            return self.next_node
        raise DoesNotExistNode("node does not exist!")

    def get_data(self):
        if self.data:
            return self.data
        raise NotSetData("current node not set data!")
    
    def equal(self, node):
        return self.get_data() == node.data

    def has_nextnode(self):
        return self.next_node != None

    def echo(self):
        node = self
        while True:
            print(node, node.data)
            if node.has_nextnode():
                node = node.next_node
            else:
                break


if __name__ == "__main__":
    head = Node()
    n1 = Node(data="n1")
    n2 = Node(data="n2")
    n3 = Node()

    head.set_next(n1)
    try:
        head.set_next(n2)
    except ExistNode as e:
        print(e)
    
    n1.set_next(n2)
    try:
        n2.get_next()
    except DoesNotExistNode as e:
        print(e)

    n2.set_next(n3)
    try:
        n3.get_data()
    except NotSetData as e:
        print(e)

    head.echo()
    print("-----")
    n1.echo()