from kivy.core.audio import SoundLoader


class AudioHandler(object):
    """
    This class is responsible for handling all the audio related operations
    It is a singleton class
    """

    main_bgm = None
    """
    The main background music
    """

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(AudioHandler, cls).__new__(cls)
        return cls.instance

    def start_main_bgm(self):
        """
        This function is used to start the main background music
        """
        if self.main_bgm is None:
            self.main_bgm = SoundLoader.load("assets/audio/main.wav")
            self.main_bgm.loop = True
            self.main_bgm.volume = 0.1
        if self.main_bgm.state == "stop":
            self.main_bgm.play()

    def stop_main_bgm(self):
        """
        This function is used to stop the main background music
        """
        self.main_bgm.stop()
        self.main_bgm = None

    def click_sound(self):
        """
        This function is used to play the click sound
        """
        click_sound = SoundLoader.load("assets/audio/click.mp3")
        click_sound.volume = 1.1
        click_sound.play()

    def win_sound(self):
        """
        This function is used to play the win sound
        """
        self.main_bgm.stop()
        win_sound = SoundLoader.load("assets/audio/win.mp3")
        win_sound.volume = 1.1
        win_sound.play()

    def lose_sound(self):
        """
        This function is used to play the lose sound
        """
        self.main_bgm.stop()
        lose_sound = SoundLoader.load("assets/audio/loose.wav")
        lose_sound.volume = 1.1
        lose_sound.play()

    def error_sound(self):
        """
        This function is used to play the error sound
        """
        error_sound = SoundLoader.load("assets/audio/error.mp3")
        error_sound.volume = 1.1
        error_sound.play()
