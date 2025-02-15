from link import Link
from node import Node

# Router class (node)
class Router(Node):
    def __init__(self, propScale, occupied, bufferSize):
        super().__init__(propScale, occupied)
        self.links = [] # Connected links
        self.routingTable = {} # Host, Link
        self.bufferSize = bufferSize
        self.queues = {} # Link, List

        self.averageQueueLength = 0

    def generateRoute(self, host):
        
        pass

    def __str__(self):
        return super().__str__()