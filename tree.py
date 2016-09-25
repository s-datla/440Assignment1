class Node:
    # Intialise the Node
    def __init__(self,data):
        self.value = data
        self.left = None
        self.right = None
        self.up = None
        self.down = None

class Tree:
    # Create a node for the tree
    def createNode(self, data):
        return Node(data)

    # Insert a node in the tree
    def insertNode(self, node, data, option):
        if node == None:
            return self.createNode(data)
        if option == 'left':
            node.left = data
        if option == 'right':
            node.right = data
        if option == 'up':
            node.up = data
        if option == 'down':
            node.down = data
        return node

    def searchTree(self, node, path):
        if node is None or path is None:
            return node
        path = list(path)
        for char in path:
            if char == 'L':
                
            if char == 'R':

            if char == 'U':

            if char == 'D':
