import pygame
import pygame_gui
from ScreenHandler import ScreenHandler
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

    screen_handler = ScreenHandler()
    """
    The screen handler object that is responsible for managing the screens of the game.
    """

    ui_manager = None

    def start(self):
        """
        This method starts the game and the game loop
        """
        success, failures = pygame.init()
        print("{0} successes and {1} failures".format(success, failures))
        self.running = True
        # Create the window
        self.screen = pygame.display.set_mode((1280, 720))
        # Start reading the events of the game
        self.ui_manager = pygame_gui.UIManager((1280, 720))
        self.build_ui()
        self.temporary_event_handler()  # TODO: Remove this line
        # self.handle_events()

    def build_ui(self):
        """
        This method builds the user interface of the welome screen
        """
        pass

    def handle_events(self):
        """
        This method handles routing to eacvh screen's main event handler. This method
        is responsible for directing the flow of the game.
        """
        # pass
        while self.running:
            pass
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

    def temporary_display(self, temp, canvas):
        pygame.display.update()
        # the rainbow colors in order inside a list of rgb values
        for a in range(len(temp.current_level)):
            if temp.current_level[a].shape_type == "square":
                pygame.draw.polygon(
                    canvas,
                    temp.current_level[a].color,
                    (
                        temp.current_level[a].p1,
                        temp.current_level[a].p2,
                        temp.current_level[a].p3,
                        temp.current_level[a].p4,
                    ),
                )
            elif temp.current_level[a].shape_type == "triangle":
                pygame.draw.polygon(
                    canvas,
                    temp.current_level[a].color,
                    (
                        temp.current_level[a].p1,
                        temp.current_level[a].p2,
                        temp.current_level[a].p3,
                    ),
                )
            elif temp.current_level[a].shape_type == "circle":
                pygame.draw.circle(
                    canvas,
                    temp.current_level[a].color,
                    temp.current_level[a].center,
                    temp.current_level[a].radius,
                )
            elif temp.current_level[a].shape_type == "rhombus":
                pygame.draw.polygon(
                    canvas,
                    temp.current_level[a].color,
                    (
                        temp.current_level[a].p1,
                        temp.current_level[a].p2,
                        temp.current_level[a].p3,
                        temp.current_level[a].p4,
                    ),
                )
            print("Shape Type: ", temp.current_level[a].shape_type)
            print("index: ", temp.current_level[a].index)
            print("free_edges: ", temp.current_level[a].free_edges)
            print("all_edges:", temp.current_level[a].all_edges)
        self.screen.blit(canvas, (0, 0))
        pygame.display.update()

    def temporary_event_handler(self):
        # TODO: Remove this method
        while self.running:
            temp = LevelGenerator(0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    break
                elif event.type == pygame.KEYDOWN:
                    # when pressing the key A generate a new level
                    # clear the screen
                    temp.clear_level()
                    print("*" * 20)
                    print("Generating level")
                    print("*" * 20)
                    canvas = pygame.Surface((1280, 720))
                    canvas.fill((255, 255, 255))
                    if event.key == pygame.K_e:
                        temp.generate_level()
                        self.temporary_display(temp, canvas)
                    elif event.key == pygame.K_m:
                        temp.difficulty = 1
                        temp.generate_level()
                        self.temporary_display(temp, canvas)
                    elif event.key == pygame.K_h:
                        temp.difficulty = 2
                        temp.generate_level()
                        self.temporary_display(temp, canvas)
