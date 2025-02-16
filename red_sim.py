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
    
    while edges:
        edges.sort(key=lambda x: x[0])
        distance, source, dest = edges.pop(0)
        if dest not in visited:
            visited.add(dest)
            mst.append((source, dest, distance))
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
    def __init__(self, numRouters, numHosts, aON, aOFF, bufferSize, wq, minTh, maxTh, maxP, propScale):
        self.tick = 0
        self.propScale = propScale
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

        for i in range(numRouters):
            print(self.routers[i])
        for i in range(numHosts):
            print(self.hosts[i])
        # drawNodes(self)
        # drawRoute(self, random.choice(self.routers), random.choice(self.hosts))

    def getRandomHost(self, exclude):
        h = random.choice(self.hosts)
        while (h != exclude):
            h = random.choice(self.hosts)
        return h

    def run(self, runTicks):
        # run simulation
        while (self.tick < runTicks):
            for host in self.hosts:
                host.tick()
            for router in self.routers:
                router.tick()
            self.tick += 1
        pass
    
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
        elif stat == "recievedPackets":
            recieved = 0
            for host in self.hosts:
                recieved += host.packetsRecieved
            return recieved

currentSim = Simulation(3, 4, 100, 1, 1, 0, 0, 0, 0, 10)
currentSim.run(10000)
print(f"Sent {currentSim.getStat('sentPackets')} packets")
print(f"Recieved {currentSim.getStat('recievedPackets')} packets")
print(f"Dropped {currentSim.getStat('droppedPackets')} packets")