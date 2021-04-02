import random
from tkinter import Tk, Frame, Button
from MazeGenerator import MazeGenerator


def main():
    # initialize window
    window = Tk()
    window.attributes("-fullscreen", True)

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=5)

    # initialize components
    buttonFrame = Frame(window, bg="grey")
    maze_gen = MazeGenerator(window)

    gen_maze_button = Button(buttonFrame,
                             text="Generate Maze",
                             command=lambda: maze_gen.generateMaze(wall_color="white",
                                                                   pointer_color="white",
                                                                   rows=random.randrange(10, 30),
                                                                   cols=random.randrange(10, 30)))

    # layout components
    buttonFrame.grid(row=0, column=0, sticky="NSEW")
    maze_gen.grid(row=0, column=1, sticky="NSEW")
    gen_maze_button.pack()

    window.mainloop()


main()
