from node import Node

# Link class
class Link:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.length = node1.distanceTo(node2) # prop delay
        self.currentDirection = 2 # 1 = from 2 to 1, 2 = from 1 to 2
        self.packet = None

    def injectPacket(self, node, packet):
        if self.packet != None:
            return False
        self.packet = packet
        self.currentDirection = 1 if node == self.node2 else 2
        return True

    def getOther(self, node):
        return self.node2 if self.node1 == node else self.node1 if self.node2 == node else None