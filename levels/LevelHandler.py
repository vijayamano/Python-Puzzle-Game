import json
from levels.level import Level


class LevelHandler:
    """
    Deals with the creation, deletion and loading of levels. Also interfaces with
    the level solver in order to produce a viable solution for the generated level
    """

    current_level = []
    """
    A list of the various shapes that represent the current level being played.
    """

    easy_levels = []
    """
    Contains all the pre-generated easy levels
    """

    medium_levels = []
    """
    Contains all the pre-generated medium levels
    """

    hard_levels = []
    """
    Contains all the pre-generated hard levels
    """

    def generate_level(difficulty):
        """
        Generates a level of the specified difficulty
        """

        match difficulty:
            case 0:
                # Easy difficulty with little amount of shapes
                pass

    def load_levels(self):
        """
        Returns a list of all pre generated levels in the game
        """
        # load the easy.json and convert to level classes
        easy = json.load(open("assets/levels/easy.json"))
        for level in easy:
            self.easy_levels.append(
                Level(
                    "easy",
                    level,
                    "assets/levels/easy/" + str(easy.index(level) + 1) + ".png",
                    "assets/textures/easy.png",
                )
            )
        # load the medium.json and convert to level classes
        medium = json.load(open("assets/levels/medium.json"))
        for level in medium:
            self.medium_levels.append(
                Level(
                    "medium",
                    level,
                    "assets/levels/medium/" + str(medium.index(level) + 1) + ".png",
                    "assets/textures/medium.png",
                )
            )
        # load the hard.json and convert to level classes
        hard = json.load(open("assets/levels/hard.json"))
        for level in hard:
            self.hard_levels.append(
                Level(
                    "hard",
                    level,
                    "assets/levels/hard/" + str(hard.index(level) + 1) + ".png",
                    "assets/textures/hard.png",
                )
            )
