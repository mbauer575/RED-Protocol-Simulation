import Link

# Packet class
class Packet:
    def __init__(self, type, source, destination):
        self.type = type # string, bool, or int?
        self.source = source
        self.destination = destination

        # tcp stuff