from point import Point
from scipy.spatial import distance
from scipy.sparse.linalg import spsolve
from scipy.sparse import csr_matrix
import numpy as np


class Bridge:

    def __init__(self, points, forces=None):
        """
        :param points: list of point objects.
        :param forces: extra forces which affect the bridge.
        """
        self.points = points
        # generate all edges/forces
        # two points will correspond with one edge, the edge is represented by an int (index)
        self.edges = {}
        edge_index = 0
        for point in self.points:
            for neighbour in point.neighbours:
                key = frozenset([point, neighbour])
                if key not in self.edges:
                    self.edges[key] = edge_index
                    edge_index += 1
        self.sparse_matrix = [[]]

    def convert_points_into_matrix(self):
        """
        :return: resulting linear system of equations of all forces, in matrix form.
        >>> p0 = Point((0, 0), is_anchored_x=True, is_anchored_y=True)
        >>> p1 = Point((1, 0))
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
        array([[-1.   ,  0.   , -0.447,  0.447,  1.   ,  0.   ,  0.   ],
               [ 0.   ,  0.   ,  0.894,  0.894,  0.   ,  0.   ,  0.   ],
               [ 0.   ,  0.   ,  0.   ,  0.   , -1.   , -0.447,  0.   ],
               [ 0.   , -0.447,  0.447,  0.   ,  0.   ,  0.   ,  1.   ],
               [ 0.   , -0.894, -0.894,  0.   ,  0.   ,  0.   ,  0.   ],
               [ 0.   ,  0.   ,  0.   , -0.447,  0.   ,  0.447, -1.   ],
               [ 0.   ,  0.   ,  0.   , -0.894,  0.   , -0.894,  0.   ]])
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
                    matrix[row_index][column_index] = round(value, 3)
                row_index += 1
            # y-direction
            if not point.is_anchored_y:
                for neighbour in point.neighbours:
                    edge_key = frozenset([point, neighbour])
                    column_index = self.edges[edge_key]
                    value = (neighbour.coordinate[1] - point.coordinate[1]) / distance.euclidean(point.coordinate, neighbour.coordinate)
                    matrix[row_index][column_index] = round(value, 3)
                row_index += 1
        return matrix


# p0 = Point((0, 0), is_anchored_x=True, is_anchored_y=True)
# p1 = Point((1, 0))
# p2 = Point((2, 0), is_anchored_y=True)
# p3 = Point((0.5, 1))
# p4 = Point((1.5, 1))
# p0.add_neighbours([p1, p3])
# p1.add_neighbours([p0, p3, p4, p2])
# p2.add_neighbours([p1, p4])
# p3.add_neighbours([p0, p1, p4])
# p4.add_neighbours([p3, p1, p2])
# b = Bridge([p0, p1, p2, p3, p4])
#
# for k, v in b.edges.items():
#     k1 = list(k)[0].coordinate
#     k2 = list(k)[1].coordinate
#     print(k1, k2, v)

if __name__ == "__main__":
    import doctest

    doctest.testmod()
