from link import Link

# Packet class
class Packet:
    def __init__(self, type, source, destination, sendTime, sequenceNum = 0, ackNum = 0, ackBit=0):
        self.type = type # "udp" or "tcp"
        self.source = source
        self.destination = destination
        self.sendTime = sendTime

        if self.type == "tcp":
            self.sequneceNum = sequenceNum
            self.ackNum = ackNum
            self.ackBit = ackBit
        else:
            self.sequenceNum = None
            self.ackNum = None
            self.ackBit = None
