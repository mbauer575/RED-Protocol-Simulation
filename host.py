from link import Link
from node import Node
from packet import Packet
import numpy as np
import random

# Host class (node)
class Host(Node):
    def __init__(self, sim, propScale, occupied, aON, aOFF, routers, mst):
        super().__init__(sim, propScale, occupied)
        self.sendState = False
        self.hostDestination = None
        self.aON = aON
        self.aOFF = aOFF
        self.xMin = 1
        self.t = 0
        
        #QUEUES
        self.udpQueue = []
        self.tcpQueue = {} #Host: []
        self.ackQueue = {} #Host: []
        
        #CONGESTION CONTROL
        self.cwnd = {} # Host: int (default: 1)
        self.ssthresh = {}
        self.unackedPackets = {}
        self.duplicateAcks = {}
        self.estimatedRTT = 1
        self.devRTT = 0
        self.rto = 3
        self.timers = {}
        
        #PACKET TRACKING
        self.packetsSent = 0
        self.packetsRecieved = 0
        self.nextSeqNum = {}

        hostRouter = self.findClosestRouter(routers)
        hostRouter.linkTo(self)
        for router in routers:
            router.generateRoute(self, mst, hostRouter)
    
    def findClosestRouter(self, routers):
        bestDist = None
        bestRouter = None
        for router in routers:
            dist = self.distanceTo(router)
            if (bestDist == None or dist < bestDist):
                bestDist = dist
                bestRouter = router
        return bestRouter

    def tick(self, collectData):
        # check link for incoming
        incomingPacket = self.links[0].getPacket(self)
        if incomingPacket:
            # print(f"{self} received a packet: {incomingPacket}")
            if collectData: self.packetsRecieved += 1

        self.t -= 1
        if self.t <= 0:
            self.sendState = not self.sendState
            self.t = (np.random.pareto(self.aON if self.sendState else self.aOFF) + 1) * self.xMin
            # print(f"send: {self.sendState} t: {self.t}")
            if self.sendState:
                self.hostDestination = self.sim.getRandomHost(self)
                # self.hostDestination = self.sim.hosts[0] if not self == self.sim.hosts[0] else self.sim.getRandomHost(self)
                self.sendType = random.choice(["udp", "tcp"])
                # self.sendType = "udp" # temp
                # self.sendType = "tcp"

        if self.sendState:
            if self.sendType == "udp":
                self.udpQueue.append(Packet("udp", self, self.hostDestination, self.sim.tick))
            elif self.sendType == "tcp":
                self.sendTCPPacket(self.hostDestination)

        if not self.links[0].active:
            availableQueues = []
            # for each host check tcp in cwnd

            #check udp queue
            if len(self.udpQueue) > 0:
                availableQueues.append(self.udpQueue)

            #check tcp queues
            if self.hostDestination in self.tcpQueue and len(self.tcpQueue[self.hostDestination])>0:
                availableQueues.append(self.tcpQueue[self.hostDestination])
            #get random queue
            if availableQueues:
                queue = random.choice(availableQueues)
                if queue:
                    if self.links[0].injectPacket(self, queue[0]):
                        queue.pop(0)
                        if collectData: self.packetsSent += 1

    def sendTCPPacket(self, dest):
        if dest not in self.cwnd:
            self.cwnd[dest] = 1
            self.ssthresh[dest] = 16
            self.tcpQueue[dest] = []
            self.unackedPackets[dest] = {}
            self.nextSeqNum[dest] = 1
        if len(self.unackedPackets[dest]) < self.cwnd[dest]:
            seqNum = self.nextSeqNum[dest]
            packet = Packet("tcp",self, dest, self.sim.tick, sequenceNum = seqNum)
            self.tcpQueue[dest].append(packet)
            self.unackedPackets[dest][seqNum] = packet
            self.nextSeqNum[dest] += 1
            self.timers[dest] = self.rto

    def handleACK(self, ackPacket):
        dest = ackPacket.source
        if dest in self.unackedPackets:
            expectedSeq = ackPacket.ackNum
            for seq in self.unackedPackets[dest].keys():
                if seq < expectedSeq:
                    del self.unackedPackets[dest][seq]
            if len(self.unackedPackets[dest]) == 0:
                if self.cwnd[dest] < self.ssthresh[dest]: 
                    self.cwnd[dest] += 1
                else:
                    self.cwnd[dest] += 1 / self.cwnd[dest]
                self.duplicateAcks[dest] = 0
            else:
                self.duplicateAcks[dest] = self.duplicateAcks.get(dest,0) + 1
                if self.duplicateAcks[dest] > 3:
                    self.ssthresh[dest] = max(self.cwnd[dest] // 2, 1)
                    self.cwnd[dest] = self.ssthesh[dest]
                    self.retransmitPacket(dest, expectedSeq)

    def retransmistPacket(self,dest, seqNum):
        if dest in self.unackedPackets and seqNum in self.unackedPackets[dest]:
            packet = self.unackedPackets[dest][seqNum]
            self.tcpQueue[dest].append(packet)
            self.timers[dest] = self.rto

    def updateRTT(self, sampleRTT):
        alpha, beta = 0.125, 0.25
        self.estimatedRTT = (1-alpha) * self.estimatedRTT + alpha * sampleRTT
        self.devRTT = (1-beta) * self.devRTT + beta * abs(sampleRTT - self.estimatedRTT)
        self.rto = self.estimatedRTT + 4 * self.devRTT
        
    def __str__(self):
        return super().__str__()
