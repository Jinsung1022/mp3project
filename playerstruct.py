from pygame import mixer
from os import listdir
from os.path import isfile, join
from tkinter import *
import tkinter as tk


class Mp3player:

    def __init__(self):
        self.win = tk.Tk()
        self.frame1 = tk.Frame(self.win, bg="black")
        self.init_struct()

    def init_struct(self):
        label1 = tk.Label(self.win, text="Now Playing: ", fg="white", bg="black")
        self.win.title("mp3player")
        self.win.resizable(False, False)
        self.win.geometry("500x400")
        self.frame1.place(x=0, y=0, anchor="nw", width=500, height=400)
        self.win.mainloop()

    def play_song(self, song):
        full_str = r'C:\Users\Jinsung\Downloads\downloadbash' + "\\" + song
        # mixer.pre_init(48000, -16, 2, 4096)
        mixer.music.load(full_str)
        mixer.music.play(2)
        label1 = tk.Label(self.win, text="Now Playing:  " + song, fg="white", bg="black")
        label1.place(x=135, y=100)

    def set_songs(self):
        onlyfiles = [f for f in listdir(r'C:\Users\Jinsung\Downloads\downloadbash') if
                     isfile(join(r'C:\Users\Jinsung\Downloads\downloadbash', f))]
        x_coor = -1
        y_coor = 200
        buttons = []
        i = 0
        for songs in onlyfiles:
            buttons.append(
                tk.Button(self.frame1, text=songs, command=lambda c=songs: self.play_song(c), bg="black", fg="white",
                          height=3, width=70))
            buttons[i].place(x=x_coor, y=y_coor)
            y_coor += 55
            i += 1


if __name__ == "__main__":
    mp3 = Mp3player()
