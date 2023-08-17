import pygame  # TODO: Remove this import
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from ui.welcomescreen import WelcomeScreen


sm = ScreenManager()


class PuzzleGame(App):
    """
    This class is the main class of the game.
    """

    running = False
    """
    Stores the current state of the game
    """

    def build(self):
        """
        This method is called when the game is started.
        """
        self.running = True
        sm.add_widget(WelcomeScreen(name="welcome"))
        return sm

    def on_start(self):
        """
        Runs as soon as the game launches
        """
        Window.size = (1280, 720)

        # def temporary_display(self, temp, canvas):
        #     pygame.display.update()
        #     # the rainbow colors in order inside a list of rgb values
        #     for a in range(len(temp.current_level)):
        #         if temp.current_level[a].shape_type == "square":
        #             pygame.draw.polygon(
        #                 canvas,
        #                 temp.current_level[a].color,
        #                 (
        #                     temp.current_level[a].p1,
        #                     temp.current_level[a].p2,
        #                     temp.current_level[a].p3,
        #                     temp.current_level[a].p4,
        #                 ),
        #             )
        #         elif temp.current_level[a].shape_type == "triangle":
        #             pygame.draw.polygon(
        #                 canvas,
        #                 temp.current_level[a].color,
        #                 (
        #                     temp.current_level[a].p1,
        #                     temp.current_level[a].p2,
        #                     temp.current_level[a].p3,
        #                 ),
        #             )
        #         elif temp.current_level[a].shape_type == "circle":
        #             pygame.draw.circle(
        #                 canvas,
        #                 temp.current_level[a].color,
        #                 temp.current_level[a].center,
        #                 temp.current_level[a].radius,
        #             )
        #         elif temp.current_level[a].shape_type == "rhombus":
        #             pygame.draw.polygon(
        #                 canvas,
        #                 temp.current_level[a].color,
        #                 (
        #                     temp.current_level[a].p1,
        #                     temp.current_level[a].p2,
        #                     temp.current_level[a].p3,
        #                     temp.current_level[a].p4,
        #                 ),
        #             )
        #         print("Shape Type: ", temp.current_level[a].shape_type)
        #         print("index: ", temp.current_level[a].index)
        #         print("free_edges: ", temp.current_level[a].free_edges)
        #         print("all_edges:", temp.current_level[a].all_edges)
        #     self.screen.blit(canvas, (0, 0))
        #     pygame.display.update()

        # def temporary_event_handler(self):
        # # TODO: Remove this method
        # while self.running:
        #     temp = LevelGenerator(0)
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             self.running = False
        #             pygame.quit()
        #             break
        #         elif event.type == pygame.KEYDOWN:
        #             # when pressing the key A generate a new level
        #             # clear the screen
        #             temp.clear_level()
        #             print("*" * 20)
        #             print("Generating level")
        #             print("*" * 20)
        #             canvas = pygame.Surface((1280, 720))
        #             canvas.fill((255, 255, 255))
        #             if event.key == pygame.K_e:
        #                 temp.generate_level()
        #                 self.temporary_display(temp, canvas)
        #             elif event.key == pygame.K_m:
        #                 temp.difficulty = 1
        #                 temp.generate_level()
        #                 self.temporary_display(temp, canvas)
        #             elif event.key == pygame.K_h:
        #                 temp.difficulty = 2
        #                 temp.generate_level()
        #                 self.temporary_display(temp, canvas)
