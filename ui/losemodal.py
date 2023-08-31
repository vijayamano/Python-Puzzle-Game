from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder

Builder.load_file("ui/kv/losemodal.kv")


class LoseModal(ModalView):
    """
    This class is used to represent the modal that is displayed when the user looses
    """

    parent_screen = None
    """
    Stores a reference to the parent screen
    """

    def __init__(self, parent_screen, **kwargs):
        self.parent_screen = parent_screen
        super().__init__(**kwargs)
