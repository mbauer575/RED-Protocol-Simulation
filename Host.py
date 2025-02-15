from link import Link
from node import Node
from packet import Packet
import numpy as np
import random

# Host class (node)
class Host(Node):
    def __init__(self, sim, propScale, occupied, aON, aOFF, routers):
        super().__init__(sim, propScale, occupied)
        self.sendState = False
        self.udpQueue = []
        self.hostDestination = None

        self.aON = aON
        self.aOFF = aOFF
        self.xMin = 1
        self.t = 0

        self.tcpQueue = {} # Host, []
        self.ackQueue = {} # Host, []
        self.cwnd = {} # Host, int (default: 1)
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
        if self.t <= 0:
            self.sendState = not self.sendState
            self.t = (np.random.pareto(self.aON if self.sendState else self.aOFF) + 1) * self.xMin
            if self.sendState:
                self.hostDestination = self.sim.getRandomHost(self)
                # self.sendType = random.choice(["udp", "tcp"])
                self.sendType = "udp" # temp
        else:
            self.t -= 1 # 1? idk time

        if self.sendState:
            if self.sendType == "udp":
                self.udpQueue.append(Packet("udp", self, self.hostDestination, self.sim.tick))
            elif self.sendType == "tcp":
                pass

        if not self.links[0].active:
            avaliableQueues = []
            # for each host check tcp in cwnd

            #check udp queue
            if len(self.udpQueue) > 0:
                avaliableQueues.append(self.udpQueue)

            #get random queue
            queue = random.choice(avaliableQueues)
            if len(queue) > 0:
                if (queue[0].type == "udp"):
                    self.links[0].injectPacket(self, queue.pop(0))
                elif (queue[0].type == "tcp"):
                    pass

    
    def __str__(self):
        return super().__str__()