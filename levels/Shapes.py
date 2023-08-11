import pygame
import random
import math
import copy


class Shape:
    """
    Base class for all shapes. Contains the basic methods and attributes

    """

    shape_type = None
    """
    Stores the type of the shape. Possible options are "square", "triangle", "circle", "rectangle", "star"
    """

    free_edges = None
    """
    A dictionary consisting of the free edges availble to attach to. The key is the index of the edge and the value is the edge itself
    """

    all_edges = None
    """
    A Dictionary consisting of all the edges of the shape. The key is the index of the edge and the value is the edge itself
    """

    index = None
    """
    A random index applied to the shape in order to make it easier to indentify
    """

    def __init__(self, index) -> None:
        self.index = index


class Square(Shape):
    """
    Square shape class

    """

    p1 = (300, 300)

    p2 = (400, 300)

    p3 = (400, 400)

    p4 = (300, 400)

    def __init__(self, index) -> None:
        super().__init__(index)
        self.shape_type = "square"
        self._setAllEdges()
        self.free_edges = copy.deepcopy(self.all_edges)

    def _setAllEdges(self):
        self.all_edges = {
            0: (  # top edge
                self.p1,
                self.p2,
            ),
            1: (  # right edge
                self.p2,
                self.p3,
            ),
            2: (  # bottom edge
                self.p3,
                self.p4,
            ),
            3: (  # left edge
                self.p4,
                self.p1,
            ),
        }

    def square_vertex(self, edge, distance, type=0):
        # Calculate the length of the edge
        edge_length = math.sqrt(
            (edge[0][0] - edge[1][0]) ** 2 + (edge[0][1] - edge[1][1]) ** 2
        )

        # Calculate the unit vector along the edge
        unit_vector = (
            (edge[1][0] - edge[0][0]) / edge_length,
            (edge[1][1] - edge[0][1]) / edge_length,
        )

        # Calculate the unit vector perpendicular to the edge
        perpendicular_unit_vector = (-unit_vector[1], unit_vector[0])

        # Calculate the coordinates of the new vertex
        if type:
            new_vertex = (
                edge[1][0] + distance * perpendicular_unit_vector[0],
                edge[1][1] + distance * perpendicular_unit_vector[1],
            )
        else:
            new_vertex = (
                edge[0][0] + distance * perpendicular_unit_vector[0],
                edge[0][1] + distance * perpendicular_unit_vector[1],
            )
        return new_vertex

    def _check_if_overlap(self, p1, p2, p3):
        """
        Checks if the edge formed by p1, p2 will form a fill square that overlaps  a triangle underneath it
        This is done by calculating the angle between edge formed by p1,p2 nad p2,p3. If the angle is less than
        90 degrees then the shape will overlap
        """
        print("Checking for overlap")
        print(p1, p2, p3)
        # calculate the angle between the two edges
        angle = math.atan2(p3[1] - p2[1], p3[0] - p2[0]) - math.atan2(
            p1[1] - p2[1], p1[0] - p2[0]
        )
        angle = math.degrees(angle)
        print(abs(angle))
        if abs(angle) < 90:
            return True
        else:
            return False

    def attach(self, shape: Shape):
        """
        Will reposisition the shape to the new shape on any random edge
        """

        this_edge = random.choice(list(self.free_edges.keys()))
        that_edge = random.choice(list(shape.free_edges.keys()))
        # remove the edge from the free edges of that shape
        del shape.free_edges[that_edge]
        # if the shapes are the same then we can only attach to the outer edges
        if self.shape_type == shape.shape_type:
            # we can only attach to the outer edges of the that_edge
            match that_edge:
                case 3:  # left edge
                    self.p2, self.p3 = shape.p1, shape.p4
                    self.p1 = self.square_vertex((self.p2, self.p3), 100)
                    self.p4 = self.square_vertex((self.p2, self.p3), 100, 1)
                    # update the all edges and free edges
                    self._setAllEdges()
                    self.free_edges = copy.deepcopy(self.all_edges)
                    del self.free_edges[1]
                case 1:  # right edge
                    self.p1, self.p4 = shape.p2, shape.p3
                    self.p2 = self.square_vertex((self.p1, self.p4), -100)
                    self.p3 = self.square_vertex((self.p1, self.p4), -100, 1)
                    # update the all edges and free edges
                    self._setAllEdges()
                    self.free_edges = copy.deepcopy(self.all_edges)
                    del self.free_edges[3]
                case 0:  # top edge
                    self.p4, self.p3 = shape.p1, shape.p2
                    self.p1 = self.square_vertex((self.p4, self.p3), -100)
                    self.p2 = self.square_vertex((self.p4, self.p3), -100, 1)
                    # update the all edges and free edges
                    self._setAllEdges()
                    self.free_edges = copy.deepcopy(self.all_edges)
                    del self.free_edges[2]
                case 2:  # bottom edge
                    self.p1, self.p2 = shape.p4, shape.p3
                    self.p3 = self.square_vertex((self.p1, self.p2), 100, 1)
                    self.p4 = self.square_vertex((self.p1, self.p2), 100)
                    # update the all edges and free edges
                    self._setAllEdges()
                    self.free_edges = copy.deepcopy(self.all_edges)
                    del self.free_edges[0]
        else:
            # we have a different kind of shape
            pass
            if shape.shape_type == "triangle":
                # we have a triangle
                match that_edge:
                    case 0:  # left edge
                        print("left edge")
                        self.p2, self.p3 = shape.p2, shape.p1
                        # check if the square will overlap with the triangle
                        if self._check_if_overlap(
                            shape.p3,
                            shape.p2,
                            self.square_vertex((self.p2, self.p3), 100),
                        ):
                            print("collision detetced left")
                            self.p1 = self.square_vertex((self.p2, self.p3), -100)
                            self.p4 = self.square_vertex((self.p2, self.p3), -100, 1)
                        else:
                            print("No collision detetced left")
                            self.p1 = self.square_vertex((self.p2, self.p3), 100)
                            self.p4 = self.square_vertex((self.p2, self.p3), 100, 1)
                        # update the all edges and free edges
                        self._setAllEdges()
                        self.free_edges = copy.deepcopy(self.all_edges)
                        del self.free_edges[1]
                    case 1:  # right edge
                        print("right edge")
                        self.p1, self.p4 = shape.p2, shape.p3
                        # check if the square will overlap with the triangle
                        if self._check_if_overlap(
                            shape.p1,
                            shape.p2,
                            self.square_vertex((self.p1, self.p4), -100),
                        ):
                            print("collision detetced right")
                            self.p2 = self.square_vertex((self.p1, self.p4), 100)
                            self.p3 = self.square_vertex((self.p1, self.p4), 100, 1)
                        else:
                            print("No collision detetced right")
                            self.p2 = self.square_vertex((self.p1, self.p4), -100)
                            self.p3 = self.square_vertex((self.p1, self.p4), -100, 1)
                        # update the all edges and free edges
                        self._setAllEdges()
                        self.free_edges = copy.deepcopy(self.all_edges)
                        del self.free_edges[3]
                    case 2:  # bottom edge
                        print("bottom edge")
                        self.p1, self.p2 = shape.p1, shape.p3
                        # check if the square will overlap with the triangle
                        if self._check_if_overlap(
                            shape.p2,
                            shape.p1,
                            self.square_vertex((self.p1, self.p2), -100),
                        ):
                            print("collision detetced bottom")
                            self.p3 = self.square_vertex((self.p1, self.p2), 100, 1)
                            self.p4 = self.square_vertex((self.p1, self.p2), 100)
                        else:
                            print("No collision detetced bottom")
                            self.p3 = self.square_vertex((self.p1, self.p2), -100, 1)
                            self.p4 = self.square_vertex((self.p1, self.p2), -100)
                        # update the all edges and free edges
                        self._setAllEdges()
                        self.free_edges = copy.deepcopy(self.all_edges)
                        del self.free_edges[0]


class Triangle(Shape):
    """
    A Triangle class shape
    """

    p1 = (300, 300)
    """
    The first point of the triangle
    """

    p2 = (350, 213)
    """
    The second point of the triangle
    """

    p3 = (400, 300)
    """
    The third point of the triangle
    """

    def __init__(self, index) -> None:
        super().__init__(index)
        self.shape_type = "triangle"
        self._setAllEdges()
        self.free_edges = copy.deepcopy(self.all_edges)

    def _setAllEdges(self):
        self.all_edges = {
            0: (  # left edge
                self.p1,
                self.p2,
            ),
            1: (  # right edge
                self.p2,
                self.p3,
            ),
            2: (  # bottom edge
                self.p3,
                self.p1,
            ),
        }

    def _check_if_close(self, p1, p2, p3, point):
        """
        Helper function that checks if point is close to any of the other points
        """
        flag = False
        if math.isclose(point[0], p1[0], abs_tol=5) and math.isclose(
            point[1], p1[1], abs_tol=1
        ):
            flag = True
        if math.isclose(point[0], p2[0], abs_tol=5) and math.isclose(
            point[1], p2[1], abs_tol=1
        ):
            flag = True
        if math.isclose(point[0], p3[0], abs_tol=5) and math.isclose(
            point[1], p3[1], abs_tol=1
        ):
            flag = True
        return flag

    def attach(self, shape: Shape):
        """
        Will reposisition the shape to the new shape on any random edge
        """
        this_edge = random.choice(list(self.free_edges.keys()))
        that_edge = random.choice(list(shape.free_edges.keys()))
        # if the shapes are the same then we can only attach to the outer edges
        if self.shape_type == shape.shape_type:
            # remove the edge from the free edges of that shape
            del shape.free_edges[that_edge]
            # we can only attach to the outer edges of the that_edge
            match that_edge:
                case 0:
                    # the left edge
                    self.p3 = shape.p1
                    self.p2 = shape.p2
                    temp = self._calculate_third_vertex(self.p3, self.p2)
                    if self._check_if_close(shape.p1, shape.p2, shape.p3, temp):
                        self.p1 = self._calculate_third_vertex(self.p3, self.p2, 1)
                    else:
                        self.p1 = temp
                    # update the all edges and free edges
                    self._setAllEdges()
                    self.free_edges = copy.deepcopy(self.all_edges)
                    del self.free_edges[1]

                case 1:
                    # the right edge
                    self.p1 = shape.p3
                    self.p2 = shape.p2
                    temp = self._calculate_third_vertex(self.p1, self.p2)
                    if self._check_if_close(shape.p1, shape.p2, shape.p3, temp):
                        self.p3 = self._calculate_third_vertex(self.p1, self.p2, 1)
                    else:
                        self.p3 = temp
                    # update the all edges and free edges
                    self._setAllEdges()
                    self.free_edges = copy.deepcopy(self.all_edges)
                    del self.free_edges[0]

                case 2:
                    # the bottom edge
                    self.p1 = shape.p3
                    self.p3 = shape.p1
                    temp = self._calculate_third_vertex(self.p1, self.p3)
                    if self._check_if_close(shape.p1, shape.p2, shape.p3, temp):
                        self.p2 = self._calculate_third_vertex(self.p1, self.p3, 1)
                    else:
                        self.p2 = temp
                    # update the all edges and free edges
                    self._setAllEdges()
                    self.free_edges = copy.deepcopy(self.all_edges)
                    del self.free_edges[2]
        else:
            # we have different kind of shapes
            if shape.shape_type == "square":
                # we have a square
                match this_edge:
                    case 0:
                        # the left edge
                        self.p1 = shape.free_edges[that_edge][0]
                        self.p2 = shape.free_edges[that_edge][1]
                        self.p3 = self._calculate_third_vertex(self.p1, self.p2)
                        # update the all edges and free edges
                        self._setAllEdges()
                        self.free_edges = copy.deepcopy(self.all_edges)
                        del self.free_edges[0]

                    case 1:
                        # the right edge
                        self.p2 = shape.free_edges[that_edge][0]
                        self.p3 = shape.free_edges[that_edge][1]
                        self.p1 = self._calculate_third_vertex(self.p2, self.p3)
                        # update the all edges and free edges
                        self._setAllEdges()
                        self.free_edges = copy.deepcopy(self.all_edges)
                        del self.free_edges[1]

                    case 2:
                        # the bottom edge
                        self.p1 = shape.free_edges[that_edge][0]
                        self.p3 = shape.free_edges[that_edge][1]
                        self.p2 = self._calculate_third_vertex(self.p1, self.p3)
                        # update the all edges and free edges
                        self._setAllEdges()
                        self.free_edges = copy.deepcopy(self.all_edges)
                        del self.free_edges[2]
                # remove the edge from the free edges of that shape
                del shape.free_edges[that_edge]

    def _calculate_third_vertex(self, point1, point2, type=0):
        x1, y1 = point1
        x2, y2 = point2

        # Calculate the distance between the two points
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # Calculate the angle between the line connecting the two points and the horizontal axis
        angle = math.atan2(y2 - y1, x2 - x1)

        # Calculate the angle to the third vertex (60 degrees or pi/3 radians)
        if type:
            angle_third_vertex = angle + math.radians(60)
        else:
            angle_third_vertex = angle - math.radians(60)

        # Calculate the coordinates of the third vertex
        x3 = x1 + distance * math.cos(angle_third_vertex)
        y3 = y1 + distance * math.sin(angle_third_vertex)

        return math.ceil(x3), math.ceil(y3)


class Circle(Shape):
    """
    A Circle Class Shape
    """

    center = (300, 300)

    radius = 50

    def __init__(self, index):
        super().__init__(index)
        self.shape_type = "circle"

    def _find_midpoint(self, p1, p2):
        """
        finds the midpoint of two points
        """
        x1, y1 = p1
        x2, y2 = p2
        return (x1 + x2) / 2, (y1 + y2) / 2

    def attach(self, shape: Shape):
        """
        Will reposisition the shape to the new shape on any random edge.
        The circle can only attach its center to the edge of any other shape.
        Based on difficulty it will be decidede whether the attached edge should be
        removed or not.
        """
        that_edge = random.choice(list(shape.free_edges.keys()))
        # find midpoint of that edge
        self.center = self._find_midpoint(
            shape.free_edges[that_edge][0], shape.free_edges[that_edge][1]
        )
        # remove the edge from the free edges of that shape
        del shape.free_edges[that_edge]
