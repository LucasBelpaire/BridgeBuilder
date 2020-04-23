class Point:

    def __init__(self, coordinate, is_anchored=False, neighbours=None):
        self.coordinate = coordinate
        self.is_anchored = is_anchored
        if neighbours:
            self.neighbours = neighbours
        else:
            self.neighbours = []

    def add_neighbour(self, neighbor):
        self.neighbours.append(neighbor)

    def add_neighbours(self, neighbours):
        self.neighbours.extend(neighbours)
