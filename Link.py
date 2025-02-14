import Node

# Link class
class Link:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.currentDirection = 2 # 1 = from 2 to 1, 2 = from 1 to 2