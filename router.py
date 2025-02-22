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

        self.averageQueueLength = 0 # idk if this is over time or just at the end of sim, rn its at end
        self.droppedPackets = 0
        self.avgQueue = {}  # RED average for each outgoing link
        self.markCounter = {} # packets arrived since last marked, for each link
        
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
    
    def tick(self, collectData):
        # Process incoming packets
        for link in self.links:
            packet = link.getPacket(self)
            if packet:
                self.processPacket(packet, collectData)
        
        # Forward packets
        for link, queue in self.queues.items():
            if not link.active and len(queue) > 0:
                if link.injectPacket(self, queue[0]):
                    queue.pop(0)

    def processPacket(self, packet, collectData):
        if packet.destination not in self.routingTable:
            return
        outlink = self.routingTable[packet.destination]
        if outlink not in self.queues:
            self.queues[outlink] = []
        queue = self.queues[outlink]
        # Update running average for the queue on this outgoing link
        old_avg = self.avgQueue.get(outlink, 0)
        new_avg = (1 - self.sim.wq) * old_avg + self.sim.wq * len(queue)
        self.avgQueue[outlink] = new_avg
        dropProb = self.redDropProbability(new_avg)
        if (len(queue) >= self.bufferSize):
            if collectData: self.droppedPackets += 1
            # print(f"{self} dropped: {packet}")
            return
        
        # IF red enabled
        if self.sim.maxP:
            mark = False
            if (self.sim.redDistribution == "geometric"):
                if random.random() < dropProb:
                    mark = True
                    # print(f"{self} dropped: {packet} due to RED geometric")
            elif (self.sim.redDistribution == "uniform"):
                if random.random() < dropProb / (1 - (self.markCounter.get(outlink, 0)*dropProb)):
                    mark = True
                    self.markCounter[outlink] = 0
                    # print(f"{self} dropped: {packet} due to RED uniform")
                else:
                    self.markCounter[outlink] = self.markCounter.get(outlink, 0) + 1

            if mark:
                if collectData: self.droppedPackets += 1
                return

        queue.append(packet)

    def redDropProbability(self, avgQueueLength):
        # If maxP is 0, RED is disabled
        if self.sim.maxP == 0:
            return 0

        if avgQueueLength < self.sim.minTh:
            return 0
        elif avgQueueLength > self.sim.maxTh:
            return 1
        else:
            # RED drop probability calculation
            return self.sim.maxP * (avgQueueLength - self.sim.minTh) / (self.sim.maxTh - self.sim.minTh)
    
    def __str__(self):
        return super().__str__()
