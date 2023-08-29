from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.clock import Clock

Builder.load_file("ui/kv/leveltimer.kv")


class LevelTimer(FloatLayout):
    """
    This class represents the timer that is used to show time this level
    """

    time = StringProperty("0 Seconds")
    """
    The time to be shown on the timer
    """

    callback = None
    """
    The callback function to be called when the timer reaches 0
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_timer(self, time, callback):
        """
        Starts the timer with the specified time and callback function
        """
        self.time = str(time) + " Seconds"
        self.callback = callback
        self.ids.timer.text = self.time
        Clock.schedule_interval(self.update_timer, 1.1)

    def update_timer(self, dt):
        """
        Updates the timer every second
        """
        self.time = str(int(self.time.split(" ")[0]) - 1)
        self.ids.timer.text = self.time + " Seconds"
        if int(self.time) == 0:
            Clock.unschedule(self.update_timer)
            self.callback()
