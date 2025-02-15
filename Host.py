from link import Link
from node import Node

# Host class (node)
class Host(Node):
    def __init__(self, propScale, occupied, aON, aOFF, routers):
        super().__init__(propScale, occupied)
        self.sendState = False
        self.udpQueue = []

        self.aON = aON
        self.aOFF = aOFF
        self.xMin = 1
        self.t = 0

        self.tcpQueue = []
        self.ackQueue = []
        self.cwnd = 1
        self.estimatedRTT = 0
        self.devRTT = 0
        self.rto = 0

        self.packetsSent = 0
        self.packetsRecieved = 0

        self.links.append(Link(self, self.findClosestRouter(routers)))
        for router in routers:
            router.generateRoute(self)
    
    def findClosestRouter(self, routers):
        bestDist = None
        bestRouter = None
        for router in routers:
            dist = self.distanceTo(router)
            if (bestDist == None or dist < bestDist):
                bestDist = dist
                bestRouter = router
        return bestRouter

    def tick(self):
        # tcp stuff

        # udp stuff
        pass