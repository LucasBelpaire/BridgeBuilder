class Point:

    def __init__(self, coordinate, is_anchored_x=False, is_anchored_y=False, load=0):
        self.coordinate = coordinate
        self.is_anchored_x = is_anchored_x
        self.is_anchored_y = is_anchored_y
        self.neighbours = []
        self.load = load
        self.member_weight = 0

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)

    def add_neighbours(self, neighbours):
        self.neighbours.extend(neighbours)

    def __str__(self):
        return '(' + str(round(self.coordinate[0], 2)) + ', ' + str(round(self.coordinate[1], 2)) + ')'
