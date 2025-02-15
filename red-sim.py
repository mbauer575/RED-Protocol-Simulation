from host import Host
from link import Link
from node import Node
from router import Router
from packet import Packet

# Red Protocol Simulation

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

def simulation(numRouters, numHosts, aON, aOFF, bufferSize, wq, minTh, maxTh, maxP, propScale):
    occupied = [None]*(numRouters+numHosts)
    
    # create routers
    routers = [None]*numRouters
    for i in range(numRouters):
        routers[i] = Router(propScale, occupied, bufferSize)
    
    # connect routers (MST)
    mst = prims(routers)
    print(mst) # TODO(Owen) make links


    # create hosts
    hosts = [None]*numHosts
    for i in range(numHosts):
        hosts[i] = Host(propScale, occupied, aON, aOFF, routers)

simulation(6, 4, 2, 1, 5, 0, 0, 0, 0, 10)