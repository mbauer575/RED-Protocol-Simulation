import random, Link

# Node class
class Node:
    def __init__(self, propScale):
        self.pos = (random.uniform(0, propScale), random.uniform(0, propScale))
        self.links = []