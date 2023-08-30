import pygame
from kivy.app import App
from kivy.core.window import Window
from ui.welcomescreen import WelcomeScreen
from kivy.lang.builder import Builder
from kivy.properties import ListProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.animation import Animation
from functools import partial
from kivy.modules import inspector

Builder.load_string(
    """
#:import Window kivy.core.window.Window
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
 

<MainScreen>:
    transition: FadeTransition()
    id: main_screen
    canvas.before:
        StencilPush
        Ellipse:
            pos: Window.center[0] - root.transition_size[0] / 2, Window.center[1] - root.transition_size[1] / 2        
            size: root.transition_size
        StencilUse
    canvas.after:
        StencilUnUse
        StencilPop
    
"""
)


class MainScreen(ScreenManager):
    transition_size = ListProperty([0, 0])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # set the transition size to window size
        self.transition_size = (
            Window.size[0] + Window.size[0] / 1.5,
            Window.size[0] + Window.size[0] / 1.5,
        )

    def init_transition(self, callback):
        """
        Causes a transition effect. The transition effect is a circle that expands from the edges in and then shrinks
        The callback function is triggered after the first animation is complete
        """
        # animate transition size to 0 and then bind to the completion of the animation
        anim = Animation(transition_size=(0, 0), duration=0.5, t="in_out_circ")
        anim.bind(on_complete=partial(self.on_transition_complete, callback))
        anim.start(self)

    def on_transition_complete(self, callback, *args):
        """
        This function returns the animation to its original size
        """
        # trigger the callback
        callback()
        # animate transition size to window size
        anim = Animation(
            transition_size=(
                Window.size[0] + Window.size[0] / 1.5,
                Window.size[0] + Window.size[0] / 1.5,
            ),
            duration=1,
            t="in_out_circ",
        )
        anim.start(self)


class PuzzleGame(App):
    """
    This class is the main class of the game.
    """

    running = False
    """
    Stores the current state of the game
    """

    main_screen = None

    welcome_screen = None

    level_screen = None

    def build(self):
        """
        This method is called when the game is started.
        """
        self.running = True
        self.main_screen = MainScreen()
        inspector.create_inspector(Window, self.main_screen)
        return self.main_screen

    def on_start(self):
        """
        Runs as soon as the game launches
        """
        self.main_screen.switch_to(WelcomeScreen())
