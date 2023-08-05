import pygame
import random

from levels.LevelGenerator import LevelGenerator


class PuzzleGame:
    """
    This is the primary clas of the game and is responsible for managing the main game loop and events.
    """

    running = False
    """
    This is a boolean flag that indicates whether the game is running or not.
    """

    screen = None
    """
    The main screen surface of the screen. Can either be None or a pygame.Surface object.
    """

    framerate = 60
    """
    The framerate of the game. This is the number of times the game will update per second.
    Defaults to 670 frames per second.
    """

    def start(self):
        """
        This method starts the game and the game loop
        """
        success, failures = pygame.init()
        print("{0} successes and {1} failures".format(success, failures))
        self.running = True
        # Create the window
        self.screen = pygame.display.set_mode((1080, 1080))
        # Start reading the events of the game
        self.screen.fill((255, 255, 255))  # TEMPORARY
        pygame.display.update()
        while True:
            self.handle_events()

    def handle_events(self):
        """
        Responsible for taking any user input for each game tick and deciding what to do with it.
        """
        temp = LevelGenerator(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                break
            elif event.type == pygame.KEYDOWN:
                # when pressing the key A generate a new level
                # clear the screen
                self.screen.fill((255, 255, 255))
                temp.clear_level()
                if event.key == pygame.K_a:
                    pygame.display.update()
                    temp.generate_level()
                    pygame.display.update()
                    # the rainbow colors in order inside a list of rgb values
                    colors = [
                        (255, 0, 0),
                        (255, 127, 0),
                        (255, 255, 0),
                        (0, 255, 0),
                        (0, 0, 255),
                        (75, 0, 130),
                        (148, 0, 211),
                    ]
                    for a in range(len(temp.current_level)):
                        if temp.current_level[a].shape_type == "square":
                            pygame.draw.polygon(
                                self.screen,
                                colors[(a + 7) % 7],
                                (
                                    temp.current_level[a].p1,
                                    temp.current_level[a].p2,
                                    temp.current_level[a].p3,
                                    temp.current_level[a].p4,
                                ),
                            )
                        elif temp.current_level[a].shape_type == "triangle":
                            pygame.draw.polygon(
                                self.screen,
                                colors[(a + 7) % 7],
                                (
                                    temp.current_level[a].p1,
                                    temp.current_level[a].p2,
                                    temp.current_level[a].p3,
                                ),
                            )
                        print("Shape Type: ", temp.current_level[a].shape_type)
                        print("index: ", temp.current_level[a].index)
                        print("free_edges: ", temp.current_level[a].all_edges)
                        print("all_edges:", temp.current_level[a].free_edges)
                    # add the surface to the center of the display screen
                    self.screen.blit(
                        self.screen,
                        (0, 0),
                    )
                    pygame.display.update()
                    continue
