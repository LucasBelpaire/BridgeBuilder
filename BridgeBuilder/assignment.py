from point import Point
from bridge import Bridge


# Bridge A
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

# Visualize bridge
b.generate_visualisation(fname="plots/introduction_bridge.png")

# Bridge with weights
# distance^1
b.generate_visualisation(member_weight=True, k=1, show_member_weights=True, show_coordinates=False)
# distance^2
b.generate_visualisation(member_weight=True, k=2, show_member_weights=True, show_coordinates=False)
# distance^3
b.generate_visualisation(member_weight=True, k=3, show_member_weights=True, show_coordinates=False)

# Optimize bridge
b.optimize()

# Micheal T. Heath: Scientific Computing [6, Chapter 2]
p1 = Point((0, 0), is_anchored_x=True, is_anchored_y=True)
p2 = Point((1, 0))
p3 = Point((1, 1))
p4 = Point((2, 1))
p5 = Point((2, 0))
p6 = Point((3, 0))
p7 = Point((3, 1))
p8 = Point((4, 0), is_anchored_y=True)

p1.add_neighbours([p2, p3])
p2.add_neighbours([p1, p3, p5])
p3.add_neighbours([p1, p2, p4, p5])
p4.add_neighbours([p3, p5, p7])
p5.add_neighbours([p2, p3, p4, p7, p6])
p6.add_neighbours([p5, p7, p8])
p7.add_neighbours([p4, p5, p6, p8])
p8.add_neighbours([p6, p7])

b2 = Bridge([p1, p2, p3, p4, p5, p6, p7, p8])
b2.generate_visualisation(member_weight=True)
b2.optimize(fname="plots/optimized_heath_bridge_k3.png", k=3)

# Long unique bridge: https://www.canambridges.com/products/steel-bridges/steel-standard-truss-bridges/
points = []
# first part of the bridge
bridge_length = 11
p_bottom = Point((0, 0), is_anchored_x=True, is_anchored_y=True)
p_top = Point((0, 1.5))
p_bottom.add_neighbour(p_top)
p_top.add_neighbour(p_bottom)
points.append(p_bottom)
points.append(p_top)
for i in range(1, bridge_length):
    if i < bridge_length/2:
        p_bottom = Point((i, 0))
        p_top = Point((i, 1.5))
        p_bottom_previous = points[i*2-2]
        p_top_previous = points[i*2-1]
        # fix neighbours
        p_bottom.add_neighbours([p_bottom_previous, p_top_previous, p_top])
        p_top.add_neighbours([p_top_previous, p_bottom])
        p_bottom_previous.add_neighbour(p_bottom)
        p_top_previous.add_neighbours([p_top, p_bottom])
        points.append(p_bottom)
        points.append(p_top)
    else:
        p_bottom = Point((i, 0))
        p_top = Point((i, 1.5))
        p_bottom_previous = points[i*2-2]
        p_top_previous = points[i*2-1]
        # fix neighbours
        p_bottom.add_neighbours([p_bottom_previous, p_top])
        p_top.add_neighbours([p_top_previous, p_bottom, p_bottom_previous])
        p_bottom_previous.add_neighbours([p_bottom, p_top])
        p_top_previous.add_neighbour(p_top)
        points.append(p_bottom)
        points.append(p_top)

points[len(points)-2].is_anchored_y = True

long_bridge = Bridge(points)
long_bridge.generate_visualisation(member_weight=True, show_coordinates=False)


# crane
p1 = Point((3, 0), is_anchored_x=True, is_anchored_y=True)
p2 = Point((5, 0), is_anchored_y=True)
p3 = Point((2, 10), is_anchored_y=True)
p4 = Point((4, 10))
p5 = Point((4, 13))
p6 = Point((20, 10), load=30)

p1.add_neighbours([p2, p4])
p2.add_neighbours([p1, p4])
p3.add_neighbours([p4, p5])
p4.add_neighbours([p1, p2, p3, p5, p6])
p5.add_neighbours([p3, p4, p6])
p6.add_neighbours([p4, p5])

crane = Bridge([p1, p2, p3, p4, p5, p6])
crane.generate_visualisation(member_weight=True, fname="plots/crane_v2.png")
