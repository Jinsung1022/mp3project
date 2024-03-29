#from node import Node
from mutagen.mp3 import MP3
from random import randrange
import contextlib
from os import listdir
from os.path import isfile, join
import os.path
from tkinter import *
from tkinter.filedialog import askdirectory
import tkinter as tk
import threading
import time
with contextlib.redirect_stdout(None):
    from pygame import mixer
    import pygame


class Node:

    def __init__(self, song, index):
        self.song = song
        self.index = index

    def get_song(self):
        return self.song

    def get_index(self):
        return self.index


class Mp3player:

    def __init__(self):
        self.win = tk.Tk()
        self.frame1 = tk.Frame(self.win, bg="black")
        self.canvas_frame = Frame(self.frame1)
        self.canvas = Canvas(self.canvas_frame, bg='#FFFFFF', width=600, height=350, scrollregion=(0, 0, 200, 800))
        self.label1 = tk.Label(self.frame1, text="", fg="white", bg="black")
        self.scale_label = tk.Label(self.frame1, text="", fg="white", bg="black")
        self.length_label = tk.Label(self.frame1, text="", fg="white", bg="black")
        self.scale_var = DoubleVar()
        self.index = 0
        self.song_length = 0
        self.value = 0
        self.status = IntVar()
        self.f = ""
        self.first = True
        self.directory = ""
        self.set_directory()
        if self.directory == "":
            sys.exit(1)
        self.song_list = [f for f in listdir(self.directory) if
                          isfile(join(self.directory, f))]
        self.resume_but = Button()
        self.loop_but = Radiobutton()
        self.st = 'p'
        self.track_on = False
        self.hor_scale = Scale()
        self.init_struct()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/100)), "units")

    def set_directory(self):
        if os.path.exists("dir.txt"):
            self.f = open("dir.txt", 'r')
            self.directory = self.f.readline()
        else:
            direct = askdirectory()
            if direct != '':
                self.directory = direct
                with open("dir.txt", 'w') as self.f:
                    self.f.write(self.directory)

    def change_dir(self):
        direct = askdirectory()
        self.f.close()
        if direct != '':
            self.directory = direct
            with open("dir.txt", 'w') as self.f:
                self.f.write(self.directory)
            self.canvas.delete("all")
            self.song_list = [f for f in listdir(self.directory) if
                              isfile(join(self.directory, f))]
            self.set_songs()

    def init_struct(self):
        mixer.init(22050, -16, 2, 4096)
        self.win.title("mp3player")
        self.win.resizable(False, False)
        self.win.geometry("700x500")
        self.frame1.place(x=0, y=0, anchor="nw", width=800, height=500)
        self.canvas_frame.place(x=50, y=150, anchor="nw", width=600, height=350)
        # Pause button
        pause_but = Button(self.frame1, text="Pause", command=lambda: [self.pause(), pause_but.place_forget()],
                           bg="grey", fg="white")
        pause_but.place(x=320, y=100)
        # Next & Prev button
        next_but = Button(self.frame1, text="Next", command=lambda: self.next_song(), bg="grey", fg="white")
        next_but.place(x=380, y=100)
        prev_but = Button(self.frame1, text="Prev", command=lambda: self.prev_song(), bg="grey", fg="white")
        prev_but.place(x=270, y=100)
        # Rewind button
        re_but = Button(self.frame1, text="Replay", command=lambda: self.rewind(), bg="grey", fg="white")
        re_but.place(x=600, y=100)
        # Standard button
        standard_but = Radiobutton(self.frame1, text="in order", variable=self.status,
                                   value=0, bg="grey", fg="black")
        standard_but.place(x=500, y=40)
        # Shuffle button
        shuffle_but = Radiobutton(self.frame1, text="shuffle", variable=self.status,
                                  value=2, bg="grey", fg="black")
        shuffle_but.place(x=500, y=70)
        # Looping button
        self.loop_but = Radiobutton(self.frame1, text="loop", variable=self.status,
                                    value=1, bg="grey", fg="black")
        self.loop_but.place(x=500, y=100)
        # Change directory button
        chdir_but = Button(self.frame1, text="Change Directory", command=lambda: self.change_dir(),
                           bg="grey", fg="white")
        chdir_but.place(x=600, y=0)
        vol_bar = Scale(self.frame1, from_=100, to=0, orient=VERTICAL,
                        command=self.change_vol, bg="black", fg="white")
        vol_bar.set(50)
        vol_bar.place(x=80, y=30)
        # Scroll bar
        vbar = Scrollbar(self.canvas_frame, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=vbar.set)
        self.canvas.pack()
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.set_songs()
        self.win.mainloop()

    def track_play(self):
        if self.st == 'p':
            self.value += 1
            minutes = self.value / 60
            seconds = self.value % 60
            self.scale_label.configure(text="%2.2d:%2.2d" % (minutes, seconds))
            self.scale_var.set(self.value)
        self.win.after(1000, lambda: self.track_play())

    def play_song(self, node):
        self.value = 0
        self.scale_var.set(0)
        if self.st == 'r':
            self.resume_but.place_forget()
            pause_but = Button(self.win, text="pause", command=lambda: [self.pause(), pause_but.place_forget()],
                               bg="grey",
                               fg="white", anchor="w")
            pause_but.place(x=320, y=100)
        self.scale_label["text"] = "0:00"
        full_str = self.directory + "\\" + node.get_song()
        self.index = node.get_index()
        # mixer.pre_init(48000, -16, 2, 4096)
        mixer.music.load(full_str)
        song = MP3(full_str)
        self.song_length = song.info.length
        self.length_label.configure(text="%2.2d:%2.2d" % (self.song_length/60, self.song_length % 60))
        mixer.music.play()
        pygame.mixer.music.set_pos(0)
        if not self.track_on:
            self.track_play()
            self.track_on = True
        '''
        # Running the loop for the progress
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()
        '''
        # Label the song
        self.label1['text'] = "Now Playing:  " + node.get_song()
        self.label1.place(x=180, y=60)
        # Song progression horizontal line
        # hor_bar = Label(self.frame1, text="_______________________________________", fg="white", bg="black")
        #self.song_length = float(self.song_length)

        if self.first:
            self.hor_scale = Scale(self.frame1, from_=0, to=self.song_length, variable=self.scale_var,
                                   resolution=0.01, length=300, orient=HORIZONTAL,
                                   command=self.change_pro, sliderlength=15,
                                   showvalue=False, bg="black", fg="white")
            self.hor_scale.place(x=180, y=10)
            self.scale_label.place(x=180, y=35)
            self.length_label.place(x=455, y=35)
            self.first = False
        else:
            self.hor_scale["to"] = self.song_length

        self.queue()
        # pygame.mixer.music.load(next_string)

    def change_pro(self, value):
        value = float(value)
        self.value = value
        # self.scale_var.set(self.value)
        minutes = value / 60
        seconds = value % 60
        self.scale_label.configure(text="%2.2d:%2.2d" % (minutes, seconds))
        pygame.mixer.music.pause()
        pygame.mixer.music.play()
        if self.st == 'r':
            pygame.mixer.music.pause()
        pygame.mixer.music.set_pos(value)
        # self.hor_scale.set(value)

    def change_vol(self, vol):
        volume = int(vol)/100
        pygame.mixer.music.set_volume(volume)

    def queue(self):
        pos = pygame.mixer.music.get_pos()
        if int(pos) == -1:
            self.next_song()
            # pygame.mixer.music.load(str1)
            # pygame.mixer.music.play()
            # self.index += 1
        self.win.after(1, self.queue)

    def set_songs(self):
        self.canvas['scrollregion'] = (0, 0, 200, (len(self.song_list)) * 55)
        y_coor = 0
        i = 0
        buttons = []
        for songs in self.song_list:
            buttons.append(
                tk.Button(self.canvas, text=songs, command=lambda c=Node(songs, i): self.play_song(c),
                          bg="gray11", fg="white", height=3, width=85))
            self.canvas.create_window(-1, y_coor, anchor=NW, window=buttons[i])
            y_coor += 55
            i += 1

    def next_song(self):
        if self.status.get() == 0:
            if self.index + 1 == len(self.song_list):
                node = Node(self.song_list[0], 0)
            else:
                node = Node(self.song_list[self.index + 1], self.index + 1)
        elif self.status.get() == 1:
            node = Node(self.song_list[self.index], self.index)
        else:
            num = randrange(len(self.song_list))
            node = Node(self.song_list[num], num)
        self.play_song(node)

    def prev_song(self):
        node = Node(self.song_list[self.index - 1], self.index - 1)
        self.play_song(node)

    def rewind(self):
        mixer.music.rewind()
        node = Node(self.song_list[self.index], self.index)
        self.play_song(node)
        self.st = 'p'
        pause_but = Button(self.win, text="Pause",
                           command=lambda: [self.pause(), pause_but.place_forget()],
                           bg="grey", fg="white", anchor="w")
        pause_but.place(x=320, y=100)

    def pause(self):
        mixer.music.pause()
        self.st = 'r'
        self.resume_but = Button(self.win, text="Resume",
                                 command=lambda: [self.resume(), self.resume_but.place_forget()],
                                 bg="grey", fg="white", anchor="w")
        self.resume_but.place(x=320, y=100)

    def resume(self):
        mixer.music.unpause()
        self.st = 'p'
        pause_but = Button(self.win, text="pause", command=lambda: [self.pause(), pause_but.place_forget()], bg="grey",
                           fg="white", anchor="w")
        pause_but.place(x=320, y=100)


if __name__ == "__main__":
    mp3 = Mp3player()
