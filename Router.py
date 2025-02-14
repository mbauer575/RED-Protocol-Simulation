import Node, Link

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