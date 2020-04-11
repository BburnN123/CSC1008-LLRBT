__author__ = 'A88253'

import os
import subprocess
import sys
import time
from collections import deque
from random import random

import pygraphviz as pgv


class LLRBT:
    root=None

    def put(self, key, val):
        self.root = self.put2(self.root, key, val)
        self.root.color=Node.BLACK

    def put2(self, node, key, val):
        if node is None:
            return Node(key, val,Node.RED)
        if key < node.key:
            node.left = self.put2(node.left, key, val)
        elif key > node.key:
            node.right = self.put2(node.right, key, val)
        else:
            node.val = val

        if self.isRed(node.right) and not self.isRed(node.left):
            node=self.rotateLeft(node)
        if self.isRed(node.left) and self.isRed(node.left.left):
            node=self.rotateRight(node)
        if self.isRed(node.left) and self.isRed(node.right):
            self.flipColors(node)

        return node

    def isRed(self, n):
        if n is None:
            return False
        else:
            return n.color == Node.RED

    def rotateLeft(self, h):
        assert(self.isRed(h.right))
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = Node.RED
        return x

    def rotateRight(self,h):
        assert(self.isRed(h.left))
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = Node.RED
        return x

    def flipColors(self, h):
        assert(not self.isRed(h))
        assert(self.isRed(h.left))
        assert(self.isRed(h.right))
        h.color = Node.RED
        h.left.color = Node.BLACK
        h.right.color = Node.BLACK

    # draw the graph
    def drawTree(self, filename):
        # create an empty undirected graph
        G=pgv.AGraph('graph myGraph {}')

        # create queue for breadth first search
        q = deque([self.root])
        # breadth first search traversal of the tree
        while len(q) != 0:
            node = q.popleft()
            #G.add_node(node, label=node.key+":"+str(node.val))
            G.add_node(node, label="")
            if node.left is not None:
                # draw the left node and edge
                #G.add_node(node.left, label=node.left.key+":"+str(node.left.val))
                G.add_node(node.left, label="")
                G.add_edge(node, node.left)
                q.append(node.left)
            if node.right is not None:
                # draw the right node and edge
                # G.add_node(node.right, label=node.right.key+":"+str(node.right.val))
                G.add_node(node.right, label="")
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
        self.put("B",4)
        self.put("A",3)
        self.put("C",5)

    def sortArr(self, root_node, arr):
        if root_node is None:
            return
        # using the same method as inorder to sort the root
        if root_node:
            self.sortArr(root_node.left, arr)
            arr.append([root_node.key, root_node.val])
            self.sortArr(root_node.right, arr)
        return arr

    def balancedTree(self):
        # create an empty arr
        arr = []
        arr = self.sortArr(self.root, arr)
        self.root = self.createBalancedTree(arr)

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

    def size(self, val):
        return self.size2(self.root, val, False)

    def size2(self, node, key, found):
        if node is None:
            return 0
        #  if the node key hit the key, set it to true
        if node.key == key:
            found = True
        #  initialize the size to 0
        size = 0
        if found:
            size = 1

        size += self.size2(node.left, key, found)
        size += self.size2(node.right, key, found)
        return size

    def preOrder(self, root_node):
        # Root, Left , Right
        if root_node is None:
            return
        if root_node:
            # Print the Root
            # print(root_node.key, " ")
            # Moving to the left node
            self.preOrder(root_node.left)
            # Moving to the right node
            self.preOrder(root_node.right)  # Moving to the right node

    def inOrder(self, root_node):
        # Left Root Right
        if root_node is None:
            return
        if root_node:
            self.inOrder(root_node.left)
            # print(root_node.key, " ")
            self.inOrder(root_node.right)

    def postOrder(self, root_node):
        # Left Right Root
        if root_node is None:
            return
        if root_node:
            self.postOrder(root_node.left)
            self.postOrder(root_node.right)
            # print(root_node.key, " ")

    def height(self, key):
        h = self.height2(self.root, key, False) - 1

    def height2(self, root, key, found):
        if root is None:
            return 0

        height = 0
        if root.key == key:
            found = True

        if found:
            height = 1
        #  Add left node
        left_node = self.height2(root.left, key, height)
        #  Add right_node
        right_node = self.height2(root.right, key, height)
        return height + max(left_node, right_node)

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
    RED = True
    BLACK = False
    left = None
    right = None
    key = 0
    val = 0
    color = None

    def __init__(self, key, val, color):
        self.key = key
        self.val = val
        self.color = color

llrbt = LLRBT()
# llrbt.createTree()

testsize = 100
values = []
k = 0
while len(values) != testsize:
    # values.append(k)
    # k += 1
    k = int(random()*testsize)
    if k not in values:
        values.append(k)

start = time.clock()
for i in values:
    llrbt.put(i, i)
print(time.clock() - start)

# start = time.clock()
# for i in values:
#     llrbt.get(i)
# print(time.clock() - start)

# llrbt.get("B")
#llrbt.balancedTree()

# llrbt.size("D")
# llrbt.height("F")
# llrbt.depth("B")
#
# llrbt.inOrder(llrbt.root)
# llrbt.postOrder(llrbt.root)
# llrbt.preOrder(llrbt.root)

#llrbt.deletion("F")

llrbt.drawTree("demo-llrbt.png")


