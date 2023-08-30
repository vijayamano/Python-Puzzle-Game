import random
from levels import (
    EASY_DEPTH,
    DEFAULT_SURFACE_SIZE,
    EASY_FALL_OFF,
    HARD_FALL_OFF,
    HARD_DEPTH,
    MEDIUM_DEPTH,
    MEDIUM_FALL_OFF,
    SHAPES,
    COLORS,
)
from pygame import Surface, SRCALPHA, draw
from pygame.image import save
from levels.Shapes import Rhombus, Square, Triangle, Circle


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
            self.generate_easy_level()
        elif self.difficulty == 1:
            self.generate_medium_level()
        elif self.difficulty == 2:
            print("generating hard level")
            self.generate_hard_level()
        # generate the preview image
        self.generate_preview_image()

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
        except IndexError:
            return None

    def _generate_colors(self, decrease):
        """
        This is a helper function to be run after a level has been generated.
        The function will assign a color to each shape in the level.
        A color is assigned based on if the order shapes are generated. Each iteration
        has either a chance to be assigned a new color or to be assigned the same color.
        The probability of assigning a new color increases as the level gets deeper.
        """
        prob = 50
        for shape in self.current_level:
            # for the first shape we assign a random color\
            if self.current_level.index(shape) == 0:
                shape.color = random.choice(COLORS)
                continue
            # choose whether to assign a new color or not
            if random.randint(0, 100) < prob:
                # assign a new color
                shape.color = random.choice(COLORS)
            else:
                # assign the same color
                shape.color = self.current_level[
                    self.current_level.index(shape) - 1
                ].color
            # decrease the probability of assigning the same color
            prob += decrease

    def generate_easy_level(self):
        """
        Generates an easy level
        """
        for i in range(EASY_DEPTH):
            # select a random shape
            shape = random.choice(SHAPES)
            random_shape = self._choose_random_shape()
            if random_shape is None and i != 0:
                print("impossible to generate level")
                return
            match shape:
                case "square":
                    if len(self.current_level) == 0:
                        # this is the first shape so we just add it to the level
                        self.current_level.append(Square(0))
                        continue
                    # pick a random shape that has free vertices
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
                    new_shape = Rhombus(i)
                    # attach the new shape to the random shape
                    new_shape.attach(random_shape)
                    # add the new shape to the current level
                    self.current_level.append(new_shape)
        # assign colors to the shapes
        self._generate_colors(EASY_FALL_OFF)

    def generate_medium_level(self):
        """
        Generates a level of medium difrficulty
        """
        for i in range(MEDIUM_DEPTH):
            # select a random shape
            shape = random.choice(SHAPES)
            random_shape = self._choose_random_shape()
            if random_shape is None and i != 0:
                print("impossible to generate level")
                return
            match shape:
                case "square":
                    if len(self.current_level) == 0:
                        # this is the first shape so we just add it to the level
                        self.current_level.append(Square(0))
                        continue
                    # pick a random shape that has free vertices
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
                    new_shape = Rhombus(i)
                    # attach the new shape to the random shape
                    new_shape.attach(random_shape)
                    # add the new shape to the current level
                    self.current_level.append(new_shape)
        # assign colors to the shapes
        self._generate_colors(MEDIUM_FALL_OFF)

    def generate_hard_level(self):
        """
        Generates a level of hard difficulty
        """
        for i in range(HARD_DEPTH):
            # select a random shape
            shape = random.choice(SHAPES)
            random_shape = self._choose_random_shape()
            if random_shape is None and i != 0:
                print("impossible to generate level")
                return
            match shape:
                case "square":
                    if len(self.current_level) == 0:
                        # this is the first shape so we just add it to the level
                        self.current_level.append(Square(0))
                        continue
                    # pick a random shape that has free vertices
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
                    new_shape = Rhombus(i)
                    # attach the new shape to the random shape
                    new_shape.attach(random_shape)
                    # add the new shape to the current level
                    self.current_level.append(new_shape)
        # assign colors to the shapes
        self._generate_colors(HARD_FALL_OFF)

    def generate_preview_image(self):
        """
        Generates the preview image for this level and store it in the tmp folder
        """
        surface = Surface((700, 700), SRCALPHA, 32)
        surface.fill((255, 255, 255, 0))
        for shape in self.current_level:
            if shape.shape_type == "triangle":
                draw.polygon(
                    surface,
                    shape.color,
                    [shape.p1, shape.p2, shape.p3],
                    0,
                )
            elif shape.shape_type == "square":
                draw.polygon(
                    surface,
                    shape.color,
                    [shape.p1, shape.p2, shape.p3, shape.p4],
                    0,
                )
            elif shape.shape_type == "circle":
                draw.circle(
                    surface,
                    shape.color,
                    shape.center,
                    shape.radius,
                    0,
                )
            elif shape.shape_type == "rhombus":
                draw.polygon(
                    surface,
                    shape.color,
                    [shape.p1, shape.p2, shape.p3, shape.p4],
                    0,
                )
        save(surface, "assets/levels/generated/preview.png")
