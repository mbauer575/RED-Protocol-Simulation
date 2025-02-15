import random

# Node class
class Node:
    def __init__(self, propScale, occupied):
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