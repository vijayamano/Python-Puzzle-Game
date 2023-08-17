from customtkinter import CTkButton
from tkinter import Frame, Label, NW
from PIL import Image, ImageTk
import os


WORKING_DIR = os.getcwd()


class StartScreen:
    """
    Class for the tkinter start screen
    """

    root = None

    base_layout = None

    width = 500

    height = 500

    def __init__(self, root, width, height):
        """
        Constructor for the start screen
        :param root: the tkinter root
        """
        self.root = root
        self.width = width
        self.height = height
        self.base_layout = Frame(root)
        self.build_ui()

    def build_ui(self):
        """
        This method builds the user interface of the welome screen inside tkinter
        """
        # set the background of the base layout to an image by setting s label
        # with the image as the background
        START_BG = ImageTk.PhotoImage(
            file=WORKING_DIR + "/assets/textures/start_bg.png",
            size=(self.width, self.height),
        )
        lbl = Label(self.base_layout, image=START_BG)
        lbl.place(
            relx=0.5, rely=0.5, anchor="center", width=self.width, height=self.height
        )
        lbl.img = START_BG

        # add the start button
        button_bg = ImageTk.PhotoImage(
            file=WORKING_DIR + "/assets/textures/play_action_normal.png",
            size=(443, 140),
        )
        startButton = CTkButton(
            self.base_layout,
            text="",
            command=self.start_game,
            width=443,
            height=140,
            image=button_bg,
            fg_color="transparent",
            bg_color="red",
        )
        startButton.place(relx=0.5, rely=0.5, anchor="center", x=0, y=0)
        self.base_layout.place(
            relx=0.5, rely=0.5, anchor="center", width=self.width, height=self.height
        )

    def start_game():
        print("dskfsdkuhfui")
