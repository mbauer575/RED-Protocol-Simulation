from host import Host
from link import Link
from node import Node
from router import Router
from packet import Packet
import random

import matplotlib.pyplot as plt

# Red Protocol Simulation

# Prim's algorithm
def prims(routers):
    mst = []
    visited = set()
    start = routers[0]
    visited.add(start)

    edges = []
    for router in routers:
        if router != start:
            distance = start.distanceTo(router)
            edges.append((distance, start, router))

    while len(visited) < len(routers):
        min_edge = None
        for edge in edges:
            distance, source, dest = edge
            if source in visited and dest not in visited:
                if min_edge is None or distance < min_edge[0]:
                    min_edge = edge

        if min_edge:
            distance, source, dest = min_edge
            mst.append((source, dest, distance))
            visited.add(dest)
            for router in routers:
                if router not in visited:
                    distance = dest.distanceTo(router)
                    edges.append((distance, dest, router))

    return mst


def generateNodePlot(sim):
    routerCoordsX = []
    routerCoordsY = []
    for router in sim.routers:
        routerCoordsX.append(router.x)
        routerCoordsY.append(router.y)
        for link in router.links:
            plt.plot([link.node1.x, link.node2.x], [link.node1.y, link.node2.y], color='blue', zorder=1)
    hostCoordsX = []
    hostCoordsY = []
    for host in sim.hosts:
        hostCoordsX.append(host.x)
        hostCoordsY.append(host.y)
    plt.scatter(routerCoordsX, routerCoordsY, color='red', label='Routers', zorder=2)
    plt.scatter(hostCoordsX, hostCoordsY, color='green', label='Hosts', zorder=2)
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    plt.title("Nodes")
    plt.xticks(range(0,sim.propScale + 1))
    plt.yticks(range(0,sim.propScale + 1))
    plt.legend()

# Debug draw nodes
# Makes a graph of all node positions and links
def drawNodes(sim):
    generateNodePlot(sim)
    plt.show()

# Debug draw route
# Makes a graph of all node positions and links
def drawRoute(sim, source, dest):
    generateNodePlot(sim)
    plt.scatter(source.x, source.y, color="orange", label="Source", zorder=4)
    plt.scatter(dest.x, dest.y, color="purple", label="Destination", zorder=4)
    link = source.routingTable[dest]
    plt.plot([link.node1.x, link.node2.x], [link.node1.y, link.node2.y], color='yellow', zorder=1)
    plt.legend()
    plt.show()

class Simulation():
    def __init__(self, numRouters, numHosts, aON, aOFF, bufferSize, wq, minTh, maxTh, maxP, propScale, redDistribution):
        self.tick = 0
        self.propScale = propScale
        self.bufferSize = bufferSize
        self.redDistribution = redDistribution
        self.wq = wq         # RED: weight for average queue calculation
        self.minTh = minTh   # RED: minimum threshold
        self.maxTh = maxTh   # RED: maximum threshold
        self.maxP = maxP     # RED: maximum drop probability
        occupied = [None]*(numRouters+numHosts)
    
        # create routers
        self.routers = [None]*numRouters
        for i in range(numRouters):
            self.routers[i] = Router(self, self.propScale, occupied, bufferSize)
        
        # connect routers (MST)
        mst = prims(self.routers)
        for edge in mst:
            edge[0].linkTo(edge[1])

        # create hosts
        self.hosts = [None]*numHosts
        for i in range(numHosts):
            self.hosts[i] = Host(self, self.propScale, occupied, aON, aOFF, self.routers, mst)

        # for i in range(numRouters):
        #     print(self.routers[i].longStr())
        # for i in range(numHosts):
        #     print(self.hosts[i].longStr())
        # drawNodes(self)
        # drawRoute(self, random.choice(self.routers), random.choice(self.hosts))

    def getRandomHost(self, exclude):
        h = random.choice(self.hosts)
        while (h == exclude):
            h = random.choice(self.hosts)
        return h

    def run(self, runTicks, collectData):
        endTick = runTicks + self.tick
        # run simulation
        while (self.tick < endTick):
            for host in self.hosts:
                host.tick(collectData)
            for router in self.routers:
                router.tick(collectData)
            self.tick += 1
        print(f"Ran simulation for {runTicks} ticks, now at {self.tick} total ticks")

    def getStat(self, stat):
        if stat == "droppedPackets":
            dropped = 0
            for router in self.routers:
                dropped += router.droppedPackets
            return dropped
        elif stat == "sentPackets":
            sent = 0
            for host in self.hosts:
                sent += host.packetsSent
            return sent
        elif stat == "receivedPackets":
            received = 0
            for host in self.hosts:
                received += host.packetsReceived
            return received
        elif stat == "hostUDPQueue":
            hostQueue = 0
            for host in self.hosts:
                hostQueue += len(host.udpQueue)
            return hostQueue
        elif stat == "routerQueueLength":
            lengths = 0
            queues = 0
            for router in self.routers:
                for queue in router.queues.values():
                    queues += 1
                    lengths += len(queue)
            return lengths / queues
        elif stat == "routerQueueCongestion":
            full = 0
            queues = 0
            for router in self.routers:
                for queue in router.queues.values():
                    queues += 1
                    if len(queue) >= self.bufferSize:
                        full += 1
            return full / queues

print("Low Router:Host, Low Buffer, Low Prop Scale, No RED")
currentSim = Simulation(10, 30, 3, 3, 50, 0.01, 10, 30, 0, 100, "geometric")
currentSim.run(10000, False)
currentSim.run(10000, True)
print(f"Packets waiting in host udp queue: {currentSim.getStat('hostUDPQueue')}")
print(f"Sent packets: {currentSim.getStat('sentPackets')}")
print(f"Received packets: {currentSim.getStat('receivedPackets')}")
print(f"Dropped packets: {currentSim.getStat('droppedPackets')}")
print(f"Average router queue length: {currentSim.getStat('routerQueueLength'):.2f}")
print(f"Proportion of congested queues: {currentSim.getStat('routerQueueCongestion'):.2f}")

print("\nLow Router:Host, Low Buffer, Low Prop Scale, RED")
currentSim = Simulation(10, 30, 3, 3, 50, 0.01, 10, 30, 0.3, 100, "geometric")
currentSim.run(10000, False)
currentSim.run(10000, True)
print(f"Packets waiting in host udp queue: {currentSim.getStat('hostUDPQueue')}")
print(f"Sent packets: {currentSim.getStat('sentPackets')}")
print(f"Received packets: {currentSim.getStat('receivedPackets')}")
print(f"Dropped packets: {currentSim.getStat('droppedPackets')}")
print(f"Average router queue length: {currentSim.getStat('routerQueueLength'):.2f}")
print(f"Proportion of congested queues: {currentSim.getStat('routerQueueCongestion'):.2f}")

# High prop

print("\nLow Router:Host, Low Buffer, High Prop Scale, No RED")
currentSim = Simulation(10, 30, 3, 3, 50, 0.01, 10, 30, 0, 200, "geometric")
currentSim.run(10000, False)
currentSim.run(10000, True)
print(f"Packets waiting in host udp queue: {currentSim.getStat('hostUDPQueue')}")
print(f"Sent packets: {currentSim.getStat('sentPackets')}")
print(f"Received packets: {currentSim.getStat('receivedPackets')}")
print(f"Dropped packets: {currentSim.getStat('droppedPackets')}")
print(f"Average router queue length: {currentSim.getStat('routerQueueLength'):.2f}")
print(f"Proportion of congested queues: {currentSim.getStat('routerQueueCongestion'):.2f}")

print("\nLow Router:Host, Low Buffer, High Prop Scale, RED")
currentSim = Simulation(10, 30, 3, 3, 50, 0.01, 10, 30, 0.3, 200, "geometric")
currentSim.run(10000, False)
currentSim.run(10000, True)
print(f"Packets waiting in host udp queue: {currentSim.getStat('hostUDPQueue')}")
print(f"Sent packets: {currentSim.getStat('sentPackets')}")
print(f"Received packets: {currentSim.getStat('receivedPackets')}")
print(f"Dropped packets: {currentSim.getStat('droppedPackets')}")
print(f"Average router queue length: {currentSim.getStat('routerQueueLength'):.2f}")
print(f"Proportion of congested queues: {currentSim.getStat('routerQueueCongestion'):.2f}")

# Large buffer

print("\nLow Router:Host, High Buffer, Low Prop Scale, No RED")
currentSim = Simulation(10, 30, 3, 3, 100, 0.01, 20, 60, 0, 100, "geometric")
currentSim.run(10000, False)
currentSim.run(10000, True)
print(f"Packets waiting in host udp queue: {currentSim.getStat('hostUDPQueue')}")
print(f"Sent packets: {currentSim.getStat('sentPackets')}")
print(f"Received packets: {currentSim.getStat('receivedPackets')}")
print(f"Dropped packets: {currentSim.getStat('droppedPackets')}")
print(f"Average router queue length: {currentSim.getStat('routerQueueLength'):.2f}")
print(f"Proportion of congested queues: {currentSim.getStat('routerQueueCongestion'):.2f}")

print("\nLow Router:Host, High Buffer, Low Prop Scale, RED")
currentSim = Simulation(10, 30, 3, 3, 100, 0.01, 20, 60, 0.3, 100, "geometric")
currentSim.run(10000, False)
currentSim.run(10000, True)
print(f"Packets waiting in host udp queue: {currentSim.getStat('hostUDPQueue')}")
print(f"Sent packets: {currentSim.getStat('sentPackets')}")
print(f"Received packets: {currentSim.getStat('receivedPackets')}")
print(f"Dropped packets: {currentSim.getStat('droppedPackets')}")
print(f"Average router queue length: {currentSim.getStat('routerQueueLength'):.2f}")
print(f"Proportion of congested queues: {currentSim.getStat('routerQueueCongestion'):.2f}")

# Large buffer, High prop

print("\nLow Router:Host, High Buffer, High Prop Scale, No RED")
currentSim = Simulation(10, 30, 3, 3, 100, 0.01, 20, 60, 0, 200, "geometric")
currentSim.run(10000, False)
currentSim.run(10000, True)
print(f"Packets waiting in host udp queue: {currentSim.getStat('hostUDPQueue')}")
print(f"Sent packets: {currentSim.getStat('sentPackets')}")
print(f"Received packets: {currentSim.getStat('receivedPackets')}")
print(f"Dropped packets: {currentSim.getStat('droppedPackets')}")
print(f"Average router queue length: {currentSim.getStat('routerQueueLength'):.2f}")
print(f"Proportion of congested queues: {currentSim.getStat('routerQueueCongestion'):.2f}")

print("\nLow Router:Host, High Buffer, High Prop Scale, RED")
currentSim = Simulation(10, 30, 3, 3, 100, 0.01, 20, 60, 0.3, 200, "geometric")
currentSim.run(10000, False)
currentSim.run(10000, True)
print(f"Packets waiting in host udp queue: {currentSim.getStat('hostUDPQueue')}")
print(f"Sent packets: {currentSim.getStat('sentPackets')}")
print(f"Received packets: {currentSim.getStat('receivedPackets')}")
print(f"Dropped packets: {currentSim.getStat('droppedPackets')}")
print(f"Average router queue length: {currentSim.getStat('routerQueueLength'):.2f}")
print(f"Proportion of congested queues: {currentSim.getStat('routerQueueCongestion'):.2f}")

# High Router:Host

print("\nHigh Router:Host, Low Buffer, Low Prop Scale, No RED")
currentSim = Simulation(10, 10, 3, 3, 50, 0.01, 10, 30, 0, 100, "geometric")
currentSim.run(10000, False)
currentSim.run(10000, True)
print(f"Packets waiting in host udp queue: {currentSim.getStat('hostUDPQueue')}")
print(f"Sent packets: {currentSim.getStat('sentPackets')}")
print(f"Received packets: {currentSim.getStat('receivedPackets')}")
print(f"Dropped packets: {currentSim.getStat('droppedPackets')}")
print(f"Average router queue length: {currentSim.getStat('routerQueueLength'):.2f}")
print(f"Proportion of congested queues: {currentSim.getStat('routerQueueCongestion'):.2f}")

print("\nHigh Router:Host, Low Buffer, Low Prop Scale, RED")
currentSim = Simulation(10, 10, 3, 3, 50, 0.01, 10, 30, 0.3, 100, "geometric")
currentSim.run(10000, False)
currentSim.run(10000, True)
print(f"Packets waiting in host udp queue: {currentSim.getStat('hostUDPQueue')}")
print(f"Sent packets: {currentSim.getStat('sentPackets')}")
print(f"Received packets: {currentSim.getStat('receivedPackets')}")
print(f"Dropped packets: {currentSim.getStat('droppedPackets')}")
print(f"Average router queue length: {currentSim.getStat('routerQueueLength'):.2f}")
print(f"Proportion of congested queues: {currentSim.getStat('routerQueueCongestion'):.2f}")

# High Router:Host, High prop

print("\nHigh Router:Host, Low Buffer, High Prop Scale, No RED")
currentSim = Simulation(10, 10, 3, 3, 50, 0.01, 10, 30, 0, 200, "geometric")
currentSim.run(10000, False)
currentSim.run(10000, True)
print(f"Packets waiting in host udp queue: {currentSim.getStat('hostUDPQueue')}")
print(f"Sent packets: {currentSim.getStat('sentPackets')}")
print(f"Received packets: {currentSim.getStat('receivedPackets')}")
print(f"Dropped packets: {currentSim.getStat('droppedPackets')}")
print(f"Average router queue length: {currentSim.getStat('routerQueueLength'):.2f}")
print(f"Proportion of congested queues: {currentSim.getStat('routerQueueCongestion'):.2f}")

print("\nHigh Router:Host, Low Buffer, High Prop Scale, RED")
currentSim = Simulation(10, 10, 3, 3, 50, 0.01, 10, 30, 0.3, 200, "geometric")
currentSim.run(10000, False)
currentSim.run(10000, True)
print(f"Packets waiting in host udp queue: {currentSim.getStat('hostUDPQueue')}")
print(f"Sent packets: {currentSim.getStat('sentPackets')}")
print(f"Received packets: {currentSim.getStat('receivedPackets')}")
print(f"Dropped packets: {currentSim.getStat('droppedPackets')}")
print(f"Average router queue length: {currentSim.getStat('routerQueueLength'):.2f}")
print(f"Proportion of congested queues: {currentSim.getStat('routerQueueCongestion'):.2f}")

# High Router:Host, High buffer

print("\nHigh Router:Host, High Buffer, Low Prop Scale, No RED")
currentSim = Simulation(10, 10, 3, 3, 100, 0.01, 20, 60, 0, 100, "geometric")
currentSim.run(10000, False)
currentSim.run(10000, True)
print(f"Packets waiting in host udp queue: {currentSim.getStat('hostUDPQueue')}")
print(f"Sent packets: {currentSim.getStat('sentPackets')}")
print(f"Received packets: {currentSim.getStat('receivedPackets')}")
print(f"Dropped packets: {currentSim.getStat('droppedPackets')}")
print(f"Average router queue length: {currentSim.getStat('routerQueueLength'):.2f}")
print(f"Proportion of congested queues: {currentSim.getStat('routerQueueCongestion'):.2f}")

print("\nHigh Router:Host, High Buffer, Low Prop Scale, RED")
currentSim = Simulation(10, 10, 3, 3, 100, 0.01, 20, 60, 0.3, 100, "geometric")
currentSim.run(10000, False)
currentSim.run(10000, True)
print(f"Packets waiting in host udp queue: {currentSim.getStat('hostUDPQueue')}")
print(f"Sent packets: {currentSim.getStat('sentPackets')}")
print(f"Received packets: {currentSim.getStat('receivedPackets')}")
print(f"Dropped packets: {currentSim.getStat('droppedPackets')}")
print(f"Average router queue length: {currentSim.getStat('routerQueueLength'):.2f}")
print(f"Proportion of congested queues: {currentSim.getStat('routerQueueCongestion'):.2f}")

# High Router:Host, High buffer, High prop

print("\nHigh Router:Host, High Buffer, High Prop Scale, No RED")
currentSim = Simulation(10, 10, 3, 3, 100, 0.01, 20, 60, 0, 200, "geometric")
currentSim.run(10000, False)
currentSim.run(10000, True)
print(f"Packets waiting in host udp queue: {currentSim.getStat('hostUDPQueue')}")
print(f"Sent packets: {currentSim.getStat('sentPackets')}")
print(f"Received packets: {currentSim.getStat('receivedPackets')}")
print(f"Dropped packets: {currentSim.getStat('droppedPackets')}")
print(f"Average router queue length: {currentSim.getStat('routerQueueLength'):.2f}")
print(f"Proportion of congested queues: {currentSim.getStat('routerQueueCongestion'):.2f}")

print("\nHigh Router:Host, High Buffer, High Prop Scale, RED")
currentSim = Simulation(10, 10, 3, 3, 100, 0.01, 20, 60, 0.3, 200, "geometric")
currentSim.run(10000, False)
currentSim.run(10000, True)
print(f"Packets waiting in host udp queue: {currentSim.getStat('hostUDPQueue')}")
print(f"Sent packets: {currentSim.getStat('sentPackets')}")
print(f"Received packets: {currentSim.getStat('receivedPackets')}")
print(f"Dropped packets: {currentSim.getStat('droppedPackets')}")
print(f"Average router queue length: {currentSim.getStat('routerQueueLength'):.2f}")
print(f"Proportion of congested queues: {currentSim.getStat('routerQueueCongestion'):.2f}")