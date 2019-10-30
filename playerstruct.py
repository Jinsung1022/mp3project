from pygame import mixer
from os import listdir
from os.path import isfile, join
from tkinter import *
import tkinter as tk


class Mp3player:

    def __init__(self):
        self.win = tk.Tk()
        self.frame1 = tk.Frame(self.win, bg="black")
        self.canvas_frame = Frame(self.frame1)
        self.canvas = Canvas(self.canvas_frame, bg='#FFFFFF', width=600, height=350, scrollregion=(0, 0, 200, 800))
        self.label1 = tk.Label(self.win, text="", fg="white", bg="black")
        self.init_struct()

    def init_struct(self):
        mixer.init(22050, -16, 2, 4096)
        self.win.title("mp3player")
        self.win.resizable(False, False)
        self.win.geometry("700x500")
        self.frame1.place(x=0, y=0, anchor="nw", width=800, height=500)
        self.canvas_frame.place(x=50, y=150, anchor="nw", width=600, height=350)
        pause_but = Button(self.win, text="pause", command=lambda: [self.pause(), pause_but.place_forget()], bg="grey",
                           fg="white")
        pause_but.place(x=320, y=100)
        vbar = Scrollbar(self.canvas_frame, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=vbar.set)
        self.canvas.pack()

        self.set_songs()
        self.win.mainloop()

    def play_song(self, song):
        full_str = r'C:\Users\Jinsung\Downloads\downloadbash' + "\\" + song
        # mixer.pre_init(48000, -16, 2, 4096)
        mixer.music.load(full_str)
        mixer.music.play(2)
        self.label1['text'] = "Now Playing:  " + song
        self.label1.place(x=135, y=50)

    def set_songs(self):
        onlyfiles = [f for f in listdir(r'C:\Users\Jinsung\Downloads\downloadbash') if
                     isfile(join(r'C:\Users\Jinsung\Downloads\downloadbash', f))]
        self.canvas['scrollregion'] = (0, 0, 200, (len(onlyfiles)) * 85)
        y_coor = 0
        buttons = []
        i = 0
        for songs in onlyfiles:
            buttons.append(
                tk.Button(self.canvas, text=songs, command=lambda c=songs: self.play_song(c), bg="black", fg="white",
                          height=3, width=85))
            self.canvas.create_window(-1, y_coor, anchor=NW, window=buttons[i])
            y_coor += 55
            i += 1

    def pause(self):
        mixer.music.pause()
        resume_but = Button(self.win, text="resume", command=lambda: [self.resume(), resume_but.place_forget()],
                            bg="grey", fg="white", anchor="w")
        resume_but.place(x=320, y=100)

    def resume(self):
        mixer.music.unpause()
        pause_but = Button(self.win, text="pause", command=lambda: [self.pause(), pause_but.place_forget()], bg="grey",
                           fg="white", anchor="w")
        pause_but.place(x=320, y=100)


if __name__ == "__main__":
    mp3 = Mp3player()
