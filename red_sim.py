from host import Host
from link import Link
from node import Node
from router import Router
from packet import Packet

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
def drawNodes(routers, hosts, scale):
    routerCoordsX = []
    routerCoordsY = []
    for router in routers:
        routerCoordsX.append(router.x)
        routerCoordsY.append(router.y)
        for link in router.links:
            plt.plot([link.node1.x, link.node2.x], [link.node1.y, link.node2.y], color='blue', zorder=1)
    hostCoordsX = []
    hostCoordsY = []
    for host in hosts:
        hostCoordsX.append(host.x)
        hostCoordsY.append(host.y)
    plt.scatter(routerCoordsX, routerCoordsY, color='red', label='Routers', zorder=2)
    plt.scatter(hostCoordsX, hostCoordsY, color='green', label='Hosts', zorder=2)
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    plt.title("Nodes")
    plt.xticks(range(0,scale + 1))
    plt.yticks(range(0,scale + 1))
    plt.legend()
    plt.show()

def simulation(numRouters, numHosts, aON, aOFF, bufferSize, wq, minTh, maxTh, maxP, propScale):
    occupied = [None]*(numRouters+numHosts)
    
    # create routers
    routers = [None]*numRouters
    for i in range(numRouters):
        routers[i] = Router(propScale, occupied, bufferSize)
    
    # connect routers (MST)
    mst = prims(routers)
    for edge in mst:
        edge[0].linkTo(edge[1])

    # create hosts
    hosts = [None]*numHosts
    for i in range(numHosts):
        hosts[i] = Host(propScale, occupied, aON, aOFF, routers)

    for i in range(numRouters):
        print(routers[i])
    for i in range(numHosts):
        print(hosts[i])
    # drawNodes(routers, hosts, propScale)


simulation(6, 4, 2, 1, 5, 0, 0, 0, 0, 10)