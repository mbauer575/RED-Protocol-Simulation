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

# Debug draw nodes
# Makes a graph of all node positions and links
def drawNodes(sim):
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
    plt.show()

class Simulation():
    def __init__(self, numRouters, numHosts, aON, aOFF, bufferSize, wq, minTh, maxTh, maxP, propScale):
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
            self.hosts[i] = Host(self, self.propScale, occupied, aON, aOFF, self.routers)

        for i in range(numRouters):
            print(self.routers[i])
        for i in range(numHosts):
            print(self.hosts[i])
        drawNodes(self)

    def getRandomHost(self, exclude):
        h = random.choice(self.hosts)
        while (h != exclude):
            h = random.choice(self.hosts)
        return h

    def run(self, runTicks):
        # run simulation
        self.tick = 0
        while (self.tick < runTicks):

            self.tick += 1
        pass

currentSim = Simulation(6, 4, 2, 1, 5, 0, 0, 0, 0, 10)
currentSim.run(1000)