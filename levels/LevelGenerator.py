from calendar import c
import random
from levels import EASY_DEPTH, DEFAULT_SIZE, DEFAULT_SURFACE_SIZE
from pygame import Surface
from levels.Shapes import Square, Triangle

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

    def generate_easy_level(self):
        """
        Generates an easy level
        """
        for i in range(EASY_DEPTH):
            # select a random shape
            shape = random.choice(SHAPES)
            shape = "triangle"  # TODO: remove this line
            match shape:
                case "square":
                    if len(self.current_level) == 0:
                        # this is the first shape so we just add it to the level
                        self.current_level.append(Square(0))
                        continue
                    # pick a random shape in the current level
                    random_shape = random.choice(self.current_level)
                    # generate a new random shape that will be attached to the existing random one
                    new_shape = Square(i)  # TODO: generate a random shape
                    # attach the new shape to the random shape
                    new_shape.attach(random_shape)
                    # add the new shape to the current level
                    self.current_level.append(new_shape)

                case "triangle":
                    if len(self.current_level) == 0:
                        # this is the first shape so we just add it to the level
                        print("generating first triangle")
                        self.current_level.append(Triangle(0))
                        continue
                    # pick a random shape in the current level
                    random_shape = random.choice(self.current_level)
                    # generate a new random shape that will be attached to the existing random one
                    print("generating triangle ", i)
                    new_shape = Triangle(i)  # TODO: generate a random shape
                    # attach the new shape to the random shape
                    new_shape.attach(random_shape)
                    # add the new shape to the current level
                    self.current_level.append(new_shape)
