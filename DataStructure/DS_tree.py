'''
Tree data structure implementation
simpel tree, only have left, right, key three property
'''


class BTree:
    def __init__(self, value, parent=None):
        self.value = value
        self.leftChild = None
        self.rightChild = None
        self.parent = parent

    def insertLeft(self, newNode):
        if self.leftChild is None:
            self.leftChild = BTree(newNode, parent=self)
            return self.leftChild
        else:
            t = BTree(newNode)
            self.leftChild.parent = t
            t.leftChild = self.leftChild
            t.parent = self
            return t
    
    def insertRight(self, newNode):
        if self.rightChild is None:
            self.rightChild = BTree(newNode, parent=self)
            return self.rightChild
        else:
            t = BTree(newNode)
            self.rightChild.parent = t
            t.rightChild = self.rightChild
            t.parent = self
            return t

    def getParent(self):
        return self.parent

    def getRightchild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    def setVal(self, obj):
        self.value = obj
    
    def getVal(self):
        return self.value

    @property
    def path(self):
        node = self
        paths = []
        while True:
            paths.insert(0, node.value)
            if node.parent is None:
                break
            node = node.parent
        return paths


if __name__ == "__main__":
    root = BTree("root")
    l1 = root.insertLeft("l1")
    r1 = root.insertRight("r1")
    l2l = l1.insertLeft("l2l")
    l2r = l1.insertRight("l2r")
    l = root.insertLeft("l")
    r = root.insertRight("r")
    print(l2l.path) # ['root', 'l', 'l1', 'l2l']