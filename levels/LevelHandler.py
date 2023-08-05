from levels import EASY_DEPTH

class LevelHandler:
    """
    Deals with the creation, deletion and loading of levels. Also interfaces with 
    the level solver in order to produce a viable solution for the generated level
    """

    current_level = []
    """
    A list of the various shapes that represent the current level being played.
    """


    def generate_level(difficulty):
        """
        Generates a level of the specified difficulty
        """
        
        match difficulty:
            case 0:
                # Easy difficulty with little amount of shapes
