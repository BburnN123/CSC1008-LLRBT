__author__ = 'A88253'

import os
import sys
import subprocess
import time
import pygraphviz as pgv
from collections import deque
from random import random

class BST:
    root=None

    def put(self, key, val):
        self.root = self.put2(self.root, key, val)

    def put2(self, node, key, val):
        if node is None:
            #key is not in tree, create node and return node to parent
            return Node(key, val)
        if key < node.key:
            # key is in left subtree
            node.left = self.put2(node.left, key, val)
        elif key > node.key:
            # key is in right subtree
            node.right = self.put2(node.right, key, val)
        else:
            node.val = val
        return node

    # draw the graph
    def drawTree(self, filename):
        # create an empty undirected graph
        G=pgv.AGraph('graph myGraph {}')

        # create queue for breadth first search
        q = deque([self.root])

        # breadth first search traversal of the tree
        while len(q) != 0:
            node = q.popleft()

            G.add_node(node, label=node.key+":"+str(node.val))
            #if node.left is not empty//
            if node.left is not None:
                # draw the left node and edge
                G.add_node(node.left, label=node.left.key+":"+str(node.left.val))
                G.add_edge(node, node.left)
                q.append(node.left)
            #if node.right is not empty//
            if node.right is not None:
                # draw the right node and edge
                G.add_node(node.right, label=node.right.key+":"+str(node.right.val))
                G.add_edge(node, node.right)
                q.append(node.right)

        # render graph into PNG file
        G.draw(filename,prog='dot')
        if sys.platform == "win32":
            os.startfile(filename)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])

    def createTree(self):
        self.put("F", 6)
        self.put("D", 4)
        self.put("C", 3)
        self.put("B", 2)
        self.put("A", 1)
        self.put("I", 9)
        self.put("E", 5)
        self.put("G", 7)
        self.put("J", 10)
        self.put("H", 8)

    def balancedTree(self):
        # create an empty arr
        arr = []
        arr = self.sortArr(self.root, arr)
        self.root = self.createBalancedTree(arr)

    def sortArr(self, root_node, arr):
        if root_node is None:
            return
        # using the same method as inorder to sort the root
        if root_node:
            self.sortArr(root_node.left, arr)
            arr.append([root_node.key, root_node.val])
            self.sortArr(root_node.right, arr)
        return arr

    def createBalancedTree(self, arr):
        if not arr:
            return None
        # get the middle val
        mid = int((len(arr)) / 2)

        # make the middle element the root
        root = Node(arr[mid][0], arr[mid][1])

        # left subtree of root has all
        # if values is less than arr[mid]
        root.left = self.createBalancedTree(arr[:mid])

        # right subtree of root has all
        # if values is more than arr[mid]
        root.right = self.createBalancedTree(arr[mid + 1:])
        return root

    def get(self, key):
        q = self.root
        while q is not None:
            #  if there is a key in the root, return the value
            if q.key == key:
                return q.val
            elif q.key > key:
                q = q.left
            else:
                q = q.right

    def size(self, key):
        q = self.root
        while q is not None:
            #  if there is a key in the root, return the value
            if q.key == key:
                return self.size2(q, key)
            elif q.key > key:
                q = q.left
            else:
                q = q.right


    def size2(self, node, key):
        if node is None:
            return 0
        #  initialize the size to 0
        size = 1

        size += self.size2(node.left, key)
        size += self.size2(node.right, key)
        return size

    def preOrder(self):
        if self.root is None:
            return
        arr = []
        arr = self.preOrder2(self.root, arr)
        string_arr = ""
        for index in arr:
            temp = index[0] + ":" + str(index[1])
            string_arr = string_arr + " " + temp

        return string_arr

    def preOrder2(self, root_node, arr):
        # Root, Left , Right
        if root_node is None:
            return
        if root_node:
            # Print the Root
            arr.append([root_node.key, root_node.val])
            # Moving to the left node
            self.preOrder2(root_node.left, arr)
            # Moving to the right node
            self.preOrder2(root_node.right, arr)
        return arr

    def inOrder(self):
        # Left Root Right
        if self.root is None:
            return

        arr = []
        arr = self.inOrder2(self.root, arr)
        string_arr = ""
        for index in arr:
            temp = index[0] + ":" + str(index[1])
            string_arr = string_arr + " " + temp
        return string_arr


    def inOrder2(self, root_node, arr):
        # Left Root Right
        if root_node is None:
            return

        if root_node:
            self.inOrder2(root_node.left, arr)
            arr.append([root_node.key, root_node.val])
            # print(root_node.key, " ")
            self.inOrder2(root_node.right, arr)

            return arr

    def postOrder(self):
        # Left Right Root
        if self.root is None:
            return

        arr = []
        arr = self.postOrder2(self.root, arr)
        string_arr = ""
        for index in arr:
            temp = index[0] + ":" + str(index[1])
            string_arr = string_arr + " " + temp
        return string_arr

    def postOrder2(self, root_node, arr):
        # Left Right Root
        if root_node is None:
            return
        if root_node:
            self.postOrder2(root_node.left, arr)
            self.postOrder2(root_node.right, arr)
            arr.append([root_node.key, root_node.val])
        return arr

    def height(self, key):
        q = self.root
        while q is not None:
            if q.key == key:
                return self.height2(q)
            elif key < q.key:
                q = q.left
            else:
                q = q.right
        return q

    def height2(self, root):
        if root is None:
            return -1
        #  Add left node
        left_node = self.height2(root.left)
        #  Add right_node
        right_node = self.height2(root.right)
        return 1 + max(left_node, right_node)

    def depth(self, key):
        q = self.root
        while q is not None:
            if q.key == key:
                return self.depth2(self.root)

            elif q.key > key:
                q = q.left
            else:
                q = q.right

    def depth2(self, root):
        #  if there is no root
        if root is None:
            return 0

        # If left and right root is empty
        if root.left is None and root.right is None:
            return 1

        # Recur the right subtree if the left subtree is None
        if root.left is None:
            return self.depth2(root.right) + 1

        # Recur the left subtree if the right sub tree is None
        if root.right is None:
            return self.depth2(root.left) + 1

        return min(self.depth2(root.left), self.depth2(root.right)) + 1

    def deletionMin(self):
        self.root = self.deletionMin2(self.root)

    def deletionMin2(self, node):
        #  If left node is empty, return right node
        if node.left is None:
            return node.right

        node.left = self.deletionMin2(node.left)
        return node

    def min(self, node):
        #  find the min
        if node.left is None:
            return node
        else:
            return self.min(node.left)

    def deletion(self, key):
        #  Making use of the get method to search for the key
        if self.get(key) is None:
            return 0
        else:
            self.root = self.deletion2(self.root, key)
            if self.get(key) is None:
                return 1

    def deletion2(self, root_node, key):
        if root_node is None:
            return 0
        #  If the key is less than the root key, recur the left node
        if key < root_node.key:
            root_node.left = self.deletion2(root_node.left, key)
        #  If the key is more than the root key, recur the right node
        elif key > root_node.key:
            root_node.right = self.deletion2(root_node.right, key)
        else:
            if root_node.right is None:
                return root_node.left
            if root_node.left is None:
                return root_node.right

            n = root_node
            root_node = self.min(n.right)
            root_node.right = self.deletionMin2(n.right)
            root_node.left = n.left

        return root_node

class Node:
    left = None
    right = None
    key = 0
    val = 0

    def __init__(self, key, val):
        self.key = key
        self.val = val



bst = BST()
bst.createTree()
#
# testsize = 100
# values = []
# k = 0
# while len(values) != testsize:
#     # values.append(k)
#     # k += 1
#     k = int(random()*testsize)
#     if k not in values:
#         values.append(k)
# start = time.clock()
# for i in values:
#     bst.put(i, i)
# print(time.clock() - start)

# start = time.clock()
# for i in values:
#     bst.get(i)
# print(time.clock() - start)


print("Get value of key for B is ", bst.get("B"))
bst.balancedTree()
print("Size for D is ", bst.size("D"))
print("Depth for B is ", bst.depth("B"))
print("Height for F is ", bst.height("F"))
print("Height for A is ", bst.height("A"))

print("PreOrder", bst.preOrder())
print("InOrder: ", bst.inOrder())
print("PostOrder: ", bst.postOrder())

print("Deletion: ", bst.deletion("B"))
bst.drawTree("demo.png")
