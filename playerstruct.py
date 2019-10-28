from pygame import mixer
from os import listdir
from os.path import isfile, join
from tkinter import *
import tkinter as tk


class Mp3player():

    def __init__(self):
        self.initGUI()

    def initGUI(self):
        win = tk.Tk()
        label1 = tk.Label(win, text="Now Playing: ", fg="white", bg="black")
        frame1 = tk.Frame(win, bg="black")
        win.title("mp3player")
        win.resizable(False, False)
        win.geometry("500x400")
        frame1 = tk.Frame(win, bg="black")
        frame1.place(x=0, y=0, anchor="nw", width=500, height=400)
        win.mainloop()


if __name__ == "__main__":
    mp3 = Mp3player()
