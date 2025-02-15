from link import Link
from node import Node
import numpy as np

# Host class (node)
class Host(Node):
    def __init__(self, sim, propScale, occupied, aON, aOFF, routers):
        super().__init__(sim, propScale, occupied)
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

        self.findClosestRouter(routers).linkTo(self)
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
        if t <= 0:
            self.sendState = not self.sendState
            t = (np.random.pareto(self.aON if self.sendState else self.aOFF) + 1) * self.xMin
            if self.sendState:
                destinationHost = self.sim.getRandomHost(self) # TODO(Owen) sending packets
        else:
            t -= 1 # 1? idk time
        # tcp stuff

        # udp stuff
        pass

    def __str__(self):
        return super().__str__()