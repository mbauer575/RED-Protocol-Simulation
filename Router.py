from link import Link
from node import Node

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
        for link in self.links:
            packet = link.getPacket(self)
            if packet:
                if (self.routingTable[packet.destination] not in self.queues):
                    self.queues[self.routingTable[packet.destination]] = []
                queue = self.queues[self.routingTable[packet.destination]]
                if len(queue) < self.bufferSize:
                    queue.append(packet)
                else:
                    self.droppedPackets += 1
        
        for link, queue in self.queues.items():
            if not link.active and len(queue) > 0:
                if link.injectPacket(self, queue[0]):
                    queue.pop(0)

    def __str__(self):
        return super().__str__()