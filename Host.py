import Node, Link

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