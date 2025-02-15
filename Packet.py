from link import Link

# Packet class
class Packet:
    def __init__(self, type, source, destination, sendTime):
        self.type = type # "udp" or "tcp"
        self.source = source
        self.destination = destination
        self.sendTime = sendTime

        # tcp stuff
        self.sequenceNum = 0
        self.ackBit = 0