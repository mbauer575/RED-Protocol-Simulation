from link import Link
from node import Node
from packet import Packet
import random

# Router class (node)
class Router(Node):
    def __init__(self, sim, propScale, occupied, bufferSize):
        super().__init__(sim, propScale, occupied)
        self.links = [] # Connected links
        self.routingTable = {} # Host, Link
        self.bufferSize = bufferSize
        self.queues = {} # Link, List

        self.averageQueueLength = 0
        self.droppedPackets = 0
        
    def generateRoute(self, host, mst, hostRouter):
        if self == hostRouter:
            self.routingTable[host] = self.getLinkTo(host)
            return
        adj = {router: [] for router in self.sim.routers}
        for edge in mst:
            r1, r2, _ = edge
            adj[r1].append(r2)
            adj[r2].append(r1)
        queue = [self]
        prev = {self: None}
        while queue:
            current = queue.pop(0)
            if current == hostRouter:
                break
            for neighbor in adj[current]:
                if neighbor not in prev:
                    prev[neighbor] = current
                    queue.append(neighbor)

        if hostRouter not in prev:
            print("Error generating route from " + self + " to " + host)
        
        nextHop = hostRouter
        while prev[nextHop] != self:
            nextHop = prev[nextHop]
        for link in self.links:
            if nextHop in (link.node1, link.node2):
                self.routingTable[host] = link
    
    def tick(self):
        # Process incoming packets
        for link in self.links:
            packet = link.getPacket(self)
            if packet:
                self.processPacket(packet)
        
        # Send outgoing packets
        for link, queue in self.queues.items():
            if not link.active and len(queue) > 0:
                if link.injectPacket(self, queue[0]):
                    queue.pop(0)

    def processPacket(self,packet):
        if packet.destination not in self.routingTable:
            return
        outlink = self.routingTable[packet.destination]
        if outlink not in self.queues:
            self.queues[outlink] = []
        queue = self.queues[outlink]
        dropProb = self.redDropProbability(len(queue))
        if len(queue) >= self.buffersize or (random.random() < dropProb):
            self.droppedPackets += 1
            return

        queue.append(packet)
        if packet.type == "tcp":
            if packet.ackBit == 0:
                self.forwardPacket(packet)
            else:
                self.forwardAck(packet)

    def forwardPacket(self, packet):
        outlink = self.routingTable[packet.destination]
        if outlink:
            if not outlink.active and len(self.queues[outlink]) > 0:
                outlink.injectPacket(self, packet)

    def forwardAck(self, packet):
        outlink = self.routingTable[packet.source]
        if outlink:
            if not outlink.active and len(self.queues[outlink]) > 0:
                outlink.injectPacket(self, packet)

    def redDropProbability(self, queueLength):
        return 0
    
    def __str__(self):
        return super().__str__()
