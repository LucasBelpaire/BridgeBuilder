from point import Point
from scipy.spatial import distance
from scipy.sparse.linalg import spsolve
from scipy.sparse import csr_matrix
from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt


class Bridge:

    def __init__(self, points, ground_level=0):
        """
        :param points: list of point objects.
        """
        self.points = points
        # generate all edges/forces
        # two points will correspond with one edge, the edge is represented by an int (index)
        self.edges = {}
        edge_index = 0
        number_of_forces = 0
        for point in self.points:
            if not point.is_anchored_x:
                number_of_forces += 1
            if not point.is_anchored_y:
                number_of_forces += 1
            for neighbour in point.neighbours:
                key = frozenset([point, neighbour])
                if key not in self.edges:
                    self.edges[key] = edge_index
                    edge_index += 1
        self.ground_level = ground_level
        assert number_of_forces == len(self.edges.keys()), "There is no unique solution. The number of equations and unkown forces aren't equal."

    def generate_visualisation(self, member_weight=False, k=1, show_member_weights=False, fname=None, show_coordinates=True):
        # general setup
        force_values = self.solve_matrix(self.convert_points_into_matrix(), member_weight=member_weight, k=k)
        plt.axis('equal')
        plt.axis('off')

        # draw all points
        for point in self.points:
            x = point.coordinate[0]
            y = point.coordinate[1]
            plt.scatter(x, y, c='black')
            if show_coordinates:
                plt.text(x, y, str(point))
            # draw load if there is one
            if point.load:
                plt.arrow(x,
                          y,
                          0,
                          -point.load/5,
                          length_includes_head=True,
                          head_width=0.05,
                          ec='blue',
                          fc='blue')
            if point.member_weight:
                if show_member_weights:
                    plt.text(x,
                             y-0.2,
                             str(round(point.member_weight, 3)))
                plt.arrow(x,
                          y,
                          0,
                          -point.member_weight/15,
                          length_includes_head=True,
                          head_width=0.05,
                          ec='grey',
                          fc='grey')

        # draw all resulting forces
        for key, value in self.edges.items():
            p1 = list(key)[0]
            p2 = list(key)[1]
            x1, y1 = p1.coordinate
            x2, y2 = p2.coordinate
            x_middle = (x1 + x2) / 2
            y_middle = (y1 + y2) / 2
            force = force_values[value]
            plt.text(x_middle, y_middle, s=str(abs(round(force, 2))))
            if force < 0:
                plt.arrow(x_middle,
                          y_middle,
                          (x1-x_middle),
                          (y1-y_middle),
                          length_includes_head=True,
                          head_width=0.05,
                          ec='red',
                          fc='red')
                plt.arrow(x_middle,
                          y_middle,
                          (x2 - x_middle),
                          (y2 - y_middle),
                          length_includes_head=True,
                          head_width=0.05,
                          ec='red',
                          fc='red')
            if force >= 0:
                plt.arrow(x1,
                          y1,
                          (x_middle - x1),
                          (y_middle - y1),
                          length_includes_head=True,
                          head_width=0.05,
                          ec='green',
                          fc='green')
                plt.arrow(x2,
                          y2,
                          (x_middle - x2),
                          (y_middle - y2),
                          length_includes_head=True,
                          head_width=0.05,
                          ec='green',
                          fc='green')

        if fname:
            plt.savefig(fname)
            plt.cla()
            plt.clf()
        else:
            plt.show()

    def solve_matrix(self, matrix, member_weight=False, k=1):
        """
        :param matrix: system of linear equations representing the bridge.
        :param member_weight: boolean, if True the result will account for the weight of members.
        :param k: int, distance^k
        :return: array containing all resulting forces.
        >>> p0 = Point((0, 0), is_anchored_x=True, is_anchored_y=True)
        >>> p1 = Point((1, 0), load=1)
        >>> p2 = Point((2, 0), is_anchored_y=True)
        >>> p3 = Point((0.5, 1))
        >>> p4 = Point((1.5, 1))
        >>> p0.add_neighbours([p1, p3])
        >>> p1.add_neighbours([p0, p3, p4, p2])
        >>> p2.add_neighbours([p1, p4])
        >>> p3.add_neighbours([p0, p1, p4])
        >>> p4.add_neighbours([p3, p1, p2])
        >>> b = Bridge([p0, p1, p2, p3, p4])
        >>> matrix = b.convert_points_into_matrix()
        >>> b.solve_matrix(matrix)
        array([ 0.25      , -0.55901699,  0.55901699,  0.55901699,  0.25      ,
               -0.55901699, -0.5       ])
        """
        assert k in [1, 2, 3], "The power used for calculating the member weight is not equal to 1, 2 or 3."
        if member_weight:
            self.set_member_weights(k=k)
        else:
            self.reset_member_weights()
        # initialize "known forces" array
        forces_array = []
        for point in self.points:
            if not point.is_anchored_x:
                forces_array.append(0)
            if not point.is_anchored_y:
                down_force = point.load + point.member_weight
                forces_array.append(down_force)
        return spsolve(csr_matrix(matrix), forces_array)

    def convert_points_into_matrix(self):
        """
        :return: resulting linear system of equations of all forces, in matrix form.
        >>> p0 = Point((0, 0), is_anchored_x=True, is_anchored_y=True)
        >>> p1 = Point((1, 0), load=1)
        >>> p2 = Point((2, 0), is_anchored_y=True)
        >>> p3 = Point((0.5, 1))
        >>> p4 = Point((1.5, 1))
        >>> p0.add_neighbours([p1, p3])
        >>> p1.add_neighbours([p0, p3, p4, p2])
        >>> p2.add_neighbours([p1, p4])
        >>> p3.add_neighbours([p0, p1, p4])
        >>> p4.add_neighbours([p3, p1, p2])
        >>> b = Bridge([p0, p1, p2, p3, p4])
        >>> b.convert_points_into_matrix()
        array([[-1.        ,  0.        , -0.4472136 ,  0.4472136 ,  1.        ,
                 0.        ,  0.        ],
               [ 0.        ,  0.        ,  0.89442719,  0.89442719,  0.        ,
                 0.        ,  0.        ],
               [ 0.        ,  0.        ,  0.        ,  0.        , -1.        ,
                -0.4472136 ,  0.        ],
               [ 0.        , -0.4472136 ,  0.4472136 ,  0.        ,  0.        ,
                 0.        ,  1.        ],
               [ 0.        , -0.89442719, -0.89442719,  0.        ,  0.        ,
                 0.        ,  0.        ],
               [ 0.        ,  0.        ,  0.        , -0.4472136 ,  0.        ,
                 0.4472136 , -1.        ],
               [ 0.        ,  0.        ,  0.        , -0.89442719,  0.        ,
                -0.89442719,  0.        ]])
        """
        # initialize a matrix filled with zeros
        n = len(self.edges)
        matrix = np.zeros(shape=(n, n))
        # go over points in order, p0 -> p1 -> ... -> pn
        # for every point, check x-direction then y-direction
        # if a direction is anchored, it gets skipped
        row_index = 0
        for point in self.points:
            # x-direction
            if not point.is_anchored_x:
                # take a look at all neighbours, and corresponding edges
                for neighbour in point.neighbours:
                    edge_key = frozenset([point, neighbour])
                    column_index = self.edges[edge_key]
                    value = (neighbour.coordinate[0] - point.coordinate[0]) / distance.euclidean(point.coordinate, neighbour.coordinate)
                    matrix[row_index][column_index] = value
                row_index += 1
            # y-direction
            if not point.is_anchored_y:
                for neighbour in point.neighbours:
                    edge_key = frozenset([point, neighbour])
                    column_index = self.edges[edge_key]
                    value = (neighbour.coordinate[1] - point.coordinate[1]) / distance.euclidean(point.coordinate, neighbour.coordinate)
                    matrix[row_index][column_index] = value
                row_index += 1
        return matrix

    def reset_member_weights(self):
        # reset all member weight to zero
        for point in self.points:
            point.member_weight = 0

    def set_member_weights(self, k=1):
        assert k in [1, 2, 3], "The power used for calculating the member weight is not equal to 1, 2 or 3."
        self.reset_member_weights()
        # calculate new weights
        for key in self.edges.keys():
            p1 = list(key)[0]
            p2 = list(key)[1]
            member_weight = distance.euclidean(p1.coordinate, p2.coordinate)**k
            p1.member_weight += member_weight
            p2.member_weight += member_weight

    def calculate_total_forces(self, new_coordinates, *args):
        k = args[0][0]
        new_co_index = 0
        for point in self.points:
            if point.coordinate[1] is not self.ground_level:
                point.coordinate = (new_coordinates[new_co_index], new_coordinates[new_co_index+1])
                new_co_index += 2
        self.set_member_weights()
        return sum(self.solve_matrix(self.convert_points_into_matrix(), member_weight=True, k=k)**2)

    def optimize(self, k=1, show_member_weights=False, fname=None, show_coordinates=True):
        variable_coordinates = []
        for point in self.points:
            if point.coordinate[1] is not self.ground_level:
                variable_coordinates.append(point.coordinate[0])
                variable_coordinates.append(point.coordinate[1])
        solution = minimize(self.calculate_total_forces, np.array(variable_coordinates), args=[k]).x
        sol_index = 0
        for point in self.points:
            if point.coordinate[1] is not self.ground_level:
                point.coordinate = (solution[sol_index], solution[sol_index+1])
                sol_index += 2
        self.generate_visualisation(member_weight=True, k=k, show_member_weights=show_member_weights, fname=fname, show_coordinates=show_coordinates)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
