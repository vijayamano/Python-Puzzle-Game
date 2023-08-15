from calendar import c
import random
from tkinter import N
from levels import EASY_DEPTH, DEFAULT_SIZE, DEFAULT_SURFACE_SIZE
from pygame import Surface
from levels.Shapes import Rhombus, Square, Triangle, Circle

SHAPES = ["square", "rectangle"]


class LevelGenerator:
    """
    Generate a level based on difficulty using a brute force approach
    """

    difficulty = 0
    """
    Represents the difficulty with which this level generator was created with.
    """

    current_level = []
    """
    Represenst the current level that is being generated
    """

    default_surface = Surface(DEFAULT_SURFACE_SIZE)
    """
    The default surface to which the level will be drawn.
    Is used as  size reference in calculation 
    """

    def __init__(self, difficulty) -> None:
        self.difficulty = difficulty

    def clear_level(self):
        """
        Clears the current level
        """
        self.current_level = []

    def generate_level(self):
        """
        Generates a level of the specified difficulty
        """
        if self.difficulty == 0:
            return self.generate_easy_level()
        elif self.difficulty == 1:
            return self.generate_medium_level()
        elif self.difficulty == 2:
            return self.generate_hard_level()
        else:
            return self.generate_easy_level()

    def _choose_random_shape(self):
        """
        Chooses a random shape from the current level
        """
        possible = [
            shape
            for shape in self.current_level
            if shape.shape_type != "circle" and len(shape.free_edges) > 0
        ]
        for shape in possible:
            if shape.shape_type == "triangle" and shape.circles_attached == 1:
                possible.remove(shape)
        try:
            return random.choice(possible)
        except:
            return None

    def generate_easy_level(self):
        """
        Generates an easy level
        """
        for i in range(EASY_DEPTH):
            # select a random shape
            shape = random.choice(SHAPES)
            shape = random.choice(
                [
                    "rhombus",
                    "square",
                    "triangle",
                    "circle",
                ]
            )
            match shape:
                case "square":
                    if len(self.current_level) == 0:
                        # this is the first shape so we just add it to the level
                        self.current_level.append(Square(0))
                        continue
                    # pick a random shape that has free vertices
                    random_shape = self._choose_random_shape()
                    if random_shape is None:
                        print("impossible to generate level")
                        return
                    # generate a new random shape that will be attached to the existing random one
                    new_shape = Square(i)
                    # attach the new shape to the random shape
                    new_shape.attach(random_shape)
                    # add the new shape to the current level
                    self.current_level.append(new_shape)

                case "triangle":
                    if len(self.current_level) == 0:
                        # this is the first shape so we just add it to the level
                        self.current_level.append(Triangle(0))
                        continue
                    # pick a random shape in the current level
                    random_shape = self._choose_random_shape()
                    # generate a new random shape that will be attached to the existing random one
                    new_shape = Triangle(i)
                    # attach the new shape to the random shape
                    new_shape.attach(random_shape)
                    # add the new shape to the current level
                    self.current_level.append(new_shape)

                case "circle":
                    if len(self.current_level) == 0:
                        # since we cannot add a circle as the first shape we add a square instead
                        self.current_level.append(Square(0))
                        continue
                    # pick a random shape in the current level that is also not a circle
                    random_shape = self._choose_random_shape()
                    # generate a new random shape that will be attached to the existing random one
                    new_shape = Circle(i)
                    # attach the new shape to the random shape
                    new_shape.attach(random_shape)
                    # add the new shape to the current level
                    self.current_level.append(new_shape)

                case "rhombus":
                    if len(self.current_level) == 0:
                        # this is the first shape so we just add it to the level
                        self.current_level.append(Rhombus(0))
                        continue
                    # pick a random shape in the current level
                    random_shape = self._choose_random_shape()
                    # generate a new random shape that will be attached to the existing random one
                    new_shape = Rhombus(i)
                    # attach the new shape to the random shape
                    new_shape.attach(random_shape)
                    # add the new shape to the current level
                    self.current_level.append(new_shape)
