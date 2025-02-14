import numpy as np
import random

# Red Protocol Simulation

# Node class
class Node:
    def __init__(self, propScale):
        self.pos = (random.uniform(0, propScale), random.uniform(0, propScale))
        self.links = []


# Host class (node)
class Host(Node):
    def __init__(self, propScale):
        super().__init__(self, propScale)
        self.sendState = False
        self.udpQueue = []

        self.tcpQueue = []
        self.ackQueue = []
        self.cwnd = 1
        self.estimatedRTT = 0
        self.devRTT = 0
        self.RTO = 0

        self.packetsSent = 0
        self.packetsRecieved = 0
        
    def tick(self):
        # tcp stuff

        # udp stuff
        pass


# Router class (node)
class Router(Node):
    def __init__(self, propScale, bufferSize):
        super().__init__(propScale)
        self.links = [] # Connected links
        self.routingTable = {} # Host, Link
        self.bufferSize = bufferSize
        self.queues = {} # Link, List

        self.averageQueueLength = 0

        self.buildRoutingTable()

    def buildRoutingTable(self):
        # prims
        pass


# Packet class
class Packet:
    def __init__(self, type, source, destination):
        self.type = type # string, bool, or int?
        self.source = source
        self.destination = destination

        # tcp stuff


# Link class
class Link:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.currentDirection = 2 # 1 = from 2 to 1, 2 = from 1 to 2


def simulation():
    pass

simulation()