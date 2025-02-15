import random

# Node class
class Node:
    def __init__(self, sim, propScale, occupied):
        self.sim = sim
        self.x = random.uniform(0, propScale)
        self.y = random.uniform(0, propScale)
        while ((self.x, self.y) in occupied):
            self.x = random.uniform(0, propScale)
            self.y = random.uniform(0, propScale)
        self.links = []
    
    def distanceTo(self, x, y):
        return (self.x - x) ** 2 + (self.y - y) ** 2
    
    def distanceTo(self, node):
        return (self.x - node.x) ** 2 + (self.y - node.y) ** 2
    
    def linkTo(self, node):
        from link import Link
        link = Link(self.sim, self, node)
        self.links.append(link)
        node.links.append(link)

    def __str__(self):
        data = f"{type(self).__name__} at {self.x:.2f}, {self.y:.2f}: Links: "
        for link in self.links:
            other = link.getOther(self)
            data += f"{type(other).__name__}({other.x:.2f}, {other.y:.2f}) "
        return data