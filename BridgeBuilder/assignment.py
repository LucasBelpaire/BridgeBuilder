from point import Point
from bridge import Bridge


p0 = Point((0, 0), is_anchored_x=True, is_anchored_y=True)
p1 = Point((1, 0), load=1)
p2 = Point((2, 0), is_anchored_y=True)
p3 = Point((0.5, 1))
p4 = Point((1.5, 1))
p0.add_neighbours([p1, p3])
p1.add_neighbours([p0, p3, p4, p2])
p2.add_neighbours([p1, p4])
p3.add_neighbours([p0, p1, p4])
p4.add_neighbours([p3, p1, p2])
b = Bridge([p0, p1, p2, p3, p4])
b.generate_visualisation()
