class Level:
    """
    This class represents a level in the game
    """

    difficulty = None
    """
    The difficulty of the level
    """

    shapes = []
    """
    A list of all the shapes in the level
    """

    preview_path = None
    """
    The path to the preview image
    """

    difficulty_path = None
    """
    The path to the difficulty image
    """

    def __init__(self, difficulty, shapes, preview_path, difficulty_path):
        self.difficulty = difficulty
        self.shapes = shapes
        self.preview_path = preview_path
        self.difficulty_path = difficulty_path
