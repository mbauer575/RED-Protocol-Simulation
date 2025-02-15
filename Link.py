from node import Node

# Link class
class Link:
    def __init__(self, sim, node1, node2):
        self.active = False
        self.node1 = node1
        self.node2 = node2
        self.length = node1.distanceTo(node2) # prop delay
        self.currentDirection = 2 # 1 = from 2 to 1, 2 = from 1 to 2
        self.packet = None
        self.arriveTime = 0
        self.sim = sim

    def injectPacket(self, node, packet):
        if self.packet != None:
            return False
        self.packet = packet
        self.currentDirection = 3 - self.getNodeNum(node) # to other node
        self.active = True
        self.arriveTime = self.sim.tick + self.length + 1
        return True
    
    def getNodeNum(self, node):
        return 2 if node == self.node2 else 1 if node == self.node1 else None
    
    def getPacket(self, node):
        if not self.active:
            return None
        if self.currentDirection == self.getNodeNum(node):
            if self.sim.tick >= self.arriveTime:
                packet = self.packet
                self.packet = None
                self.active = False
                return packet
        return None

    def getOther(self, node):
        return self.node2 if self.node1 == node else self.node1 if self.node2 == node else None