class Node:
    # Intialise the Node
    def __init__(self,data, heuristic=None):
        self.value = data
        self.heuristic = heuristic
        self.left = None
        self.right = None
        self.up = None
        self.down = None


class Tree:
    # Create a node for the tree
    def createNode(self, data):
        return Node(data)

    # Insert a node in the tree
    def insertNode(self, node, data, path):
        if node == None or path == '':
            return self.createNode(data)
        p = list(path)
        char = p[0]
        if char == 'L':
            node.left = self.insertNode(node.left, data, path[1:])
        elif char == 'R':
            node.right = self.insertNode(node.right, data, path[1:])
        elif char == 'U':
            node.up = self.insertNode(node.up, data, path[1:])
        elif char == 'D':
            node.down =  self.insertNode(node.down, data, path[1:])
        return node

    def searchTree(self, node, path):
        if node is None or path == '':
            return node
        p = list(path)
        char = p[0]
        if char == 'L':
            return self.searchTree(node.left,path[1:])
        elif char == 'R':
            return self.searchTree(node.right,path[1:])
        elif char == 'U':
            return self.searchTree(node.up,path[1:])
        elif char == 'D':
            return self.searchTree(node.down,path[1:])

    def traverseInorder(self, root):
        """
        traverse function will print all the node in the tree.
        """
        if root is not None:
            self.traverseInorder(root.left)
            self.traverseInorder(root.right)
            print root.value
            self.traverseInorder(root.up)
            self.traverseInorder(root.down)

    def traversePreorder(self, root):
        """
        traverse function will print all the node in the tree.
        """
        if root is not None:
            print root.value
            self.traversePreorder(root.left)
            self.traversePreorder(root.right)
            self.traversePreorder(root.up)
            self.traversePreorder(root.down)

    def traversePostorder(self, root):
        """
        traverse function will print all the node in the tree.
        """
        if root is not None:
            self.traversePostorder(root.left)
            self.traversePostorder(root.right)
            self.traversePostorder(root.up)
            self.traversePostorder(root.down)
            print root.value


def main():
    root = None
    tree = Tree()
    root = tree.insertNode(root,1,'')
    tree.insertNode(root, 2, 'L')
    tree.insertNode(root, 3, 'R')
    tree.insertNode(root, 4, 'U')
    tree.insertNode(root, 5, 'D')
    tree.insertNode(root, 6, 'RL')
    tree.insertNode(root, 7, 'RR')

    print "Traverse Inorder"
    tree.traverseInorder(root)

    print "Traverse Preorder"
    tree.traversePreorder(root)

    print "Traverse Postorder"
    tree.traversePostorder(root)



if __name__ == "__main__":
    main()
