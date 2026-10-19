from util.node import Node

class Loop():
    def __init__(self) -> None:
        self.nodepath = []

    def add(self, node: Node):
        self.nodepath.append(node)

    def remove(self, node: Node):
        self.nodepath.remove(node)