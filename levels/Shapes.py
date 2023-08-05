import pygame
import random
import math


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

    base_shape = None
    """
    The base pygame shape object that is used to draw the shape
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

    def __init__(self, index) -> None:
        super().__init__(index)
        self.shape_type = "square"
        self.all_edges = {0: None, 1: None, 2: None, 3: None}
        self.free_edges = self.all_edges
        self.base_shape = pygame.Rect(400, 400, 100, 100)

    def _setAllEdges(self):
        self.all_edges = {
            0: (  # top edge
                (self.base_shape.left, self.base_shape.top),
                (self.base_shape.right, self.base_shape.top),
            ),
            1: (  # right edge
                (self.base_shape.right, self.base_shape.top),
                (self.base_shape.right, self.base_shape.bottom),
            ),
            2: (  # bottom edge
                (self.base_shape.right, self.base_shape.bottom),
                (self.base_shape.left, self.base_shape.bottom),
            ),
            3: (  # left edge
                (self.base_shape.left, self.base_shape.bottom),
                (self.base_shape.left, self.base_shape.top),
            ),
        }

    def attach(self, shape: Shape):
        """
        Will reposisition the shape to the new shape on any random edge
        """
        this_edge = random.choice(self.free_edges)
        that_edge = random.choice(list(shape.free_edges.keys()))
        # remove the edge from the free edges of that shape
        del shape.free_edges[that_edge]
        # if the shapes are the same then we can only attach to the outer edges
        if self.shape_type == shape.shape_type:
            # we can only attach to the outer edges of the that_edge
            match that_edge:
                case 3:  # left edge
                    self.base_shape.right = shape.base_shape.left
                    self.base_shape.top = shape.base_shape.top
                    self.base_shape.bottom = shape.base_shape.bottom
                    # update the all edges and free edges
                    self._setAllEdges()
                    self.free_edges = self.all_edges
                    del self.free_edges[1]
                case 1:  # right edge
                    self.base_shape.left = shape.base_shape.right
                    self.base_shape.top = shape.base_shape.top
                    self.base_shape.bottom = shape.base_shape.bottom
                    # update the all edges and free edges
                    self._setAllEdges()
                    self.free_edges = self.all_edges
                    del self.free_edges[3]

                case 0:  # top edge
                    self.base_shape.left = shape.base_shape.left
                    self.base_shape.right = shape.base_shape.right
                    self.base_shape.bottom = shape.base_shape.top
                    # update the all edges and free edges
                    self._setAllEdges()
                    self.free_edges = self.all_edges
                    del self.free_edges[2]

                case 2:  # bottom edge
                    self.base_shape.left = shape.base_shape.left
                    self.base_shape.right = shape.base_shape.right
                    self.base_shape.top = shape.base_shape.bottom
                    # update the all edges and free edges
                    self._setAllEdges()
                    self.free_edges = self.all_edges
                    del self.free_edges[0]


class Triangle(Shape):
    """
    A Triangle class shape
    """

    p1 = (342, 300)
    """
    The first point of the triangle
    """

    p2 = (400, 200)
    """
    The second point of the triangle
    """

    p3 = (457, 300)
    """
    The third point of the triangle
    """

    def __init__(self, index) -> None:
        super().__init__(index)
        self.shape_type = "triangle"
        self.all_edges = {0: None, 1: None, 2: None}
        self.free_edges = self.all_edges

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
        this_edge = random.choice(self.free_edges)
        that_edge = random.choice(list(shape.free_edges.keys()))
        # remove the edge from the free edges of that shape
        del shape.free_edges[that_edge]
        # if the shapes are the same then we can only attach to the outer edges
        if self.shape_type == shape.shape_type:
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
                    self.free_edges = self.all_edges
                    del self.free_edges[1]

                case 1:
                    # the right edge
                    print("right")
                    self.p1 = shape.p3
                    self.p2 = shape.p2
                    temp = self._calculate_third_vertex(self.p1, self.p2)
                    if self._check_if_close(shape.p1, shape.p2, shape.p3, temp):
                        self.p3 = self._calculate_third_vertex(self.p1, self.p2, 1)
                    else:
                        self.p3 = temp
                    # update the all edges and free edges
                    self._setAllEdges()
                    self.free_edges = self.all_edges
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
                    self.free_edges = self.all_edges
                    del self.free_edges[2]

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
