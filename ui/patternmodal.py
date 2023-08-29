from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder

Builder.load_file("ui/kv/patternmodal.kv")


class PatternModal(ModalView):
    """
    This class represents the modal that is used to show the pattern
    """

    level_no = None
    """
    The level number of the level that is being shown
    """

    preview_path = None
    """
    The path of the preview image of the level
    """

    parent_screen = None
    """
    Holds a reference to the parent screen
    """

    def __init__(self, *args, **kwargs):
        self.level_no = kwargs.pop("level_no")
        self.preview_path = kwargs.pop("preview_path")
        super().__init__(*args, **kwargs)

    pass
