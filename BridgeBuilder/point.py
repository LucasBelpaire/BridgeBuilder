class Point:

    def __init__(self, coordinate, is_anchored_x=False, is_anchored_y=False, neighbours=None, load=0, member_weight=0):
        self.coordinate = coordinate
        self.is_anchored_x = is_anchored_x
        self.is_anchored_y = is_anchored_y
        if neighbours:
            self.neighbours = neighbours
        else:
            self.neighbours = []
        self.load = load
        self.member_weight = member_weight

    def add_neighbour(self, neighbor):
        self.neighbours.append(neighbor)

    def add_neighbours(self, neighbours):
        self.neighbours.extend(neighbours)

    def __str__(self):
        return str(self.coordinate)
