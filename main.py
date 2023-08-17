import tkinter as tk
from PIL import Image, ImageTk


def quitGame(event):
    window.destroy()


window = tk.Tk()
window.geometry("500x500")

canvas = tk.Canvas(window, width=900, height=900)
canvas.pack()

# creating background
bgImage = ImageTk.PhotoImage(
    Image.open("E:/Coding/Puzzle-Game-Pygame/assets/textures/start_bg.png")
)
bg = canvas.create_image(0, 0, image=bgImage, anchor=tk.NW)

# creating button which supports png transparency
quitImage = ImageTk.PhotoImage(
    Image.open("E:/Coding/Puzzle-Game-Pygame/assets/textures/title_card.png")
)
quitButton = canvas.create_image(50, 50, image=quitImage)
canvas.tag_bind(quitButton, "<Button-1>", quitGame)

window.mainloop()
