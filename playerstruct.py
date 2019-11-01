from node import Node
from pygame import mixer
import pygame
from os import listdir
from os.path import isfile, join
from tkinter import *
import tkinter as tk


class Mp3player:

    num_played = 0

    def __init__(self):
        self.win = tk.Tk()
        self.frame1 = tk.Frame(self.win, bg="black")
        self.menu_frame = tk.Frame(self.win, bg="black")
        self.canvas_frame = Frame(self.frame1)
        self.canvas = Canvas(self.canvas_frame, bg='#FFFFFF', width=600, height=350, scrollregion=(0, 0, 200, 800))
        self.label1 = tk.Label(self.win, text="", fg="white", bg="black")
        self.index = 0

        self.song_list = [f for f in listdir(r'C:\Users\Jinsung\Downloads\downloadbash') if
                          isfile(join(r'C:\Users\Jinsung\Downloads\downloadbash', f))]
        self.init_struct()

    def init_struct(self):
        mixer.init(22050, -16, 2, 4096)
        self.win.title("mp3player")
        self.win.resizable(False, False)
        self.win.geometry("700x500")
        self.frame1.place(x=0, y=0, anchor="nw", width=800, height=500)
        self.menu_frame.place(x=0, y=0, anchor="nw", width=800, height=500)
        self.canvas_frame.place(x=50, y=150, anchor="nw", width=600, height=350)
        # Pause button
        pause_but = Button(self.win, text="pause", command=lambda: [self.pause(), pause_but.place_forget()], bg="grey",
                           fg="white")
        pause_but.place(x=320, y=100)
        # Next & Prev button
        next_but = Button(self.win, text="Next", command=lambda: self.next_song(), bg="grey", fg="white")
        next_but.place(x=380, y=100)
        prev_but = Button(self.win, text="Prev", command=lambda: self.prev_song(), bg="grey", fg="white")
        prev_but.place(x=270, y=100)
        # Rewind button
        re_but = Button(self.win, text="Replay", command=lambda: mixer.music.rewind(), bg="grey", fg="white")
        re_but.place(x=600, y=100)
        list_but = Button(self.win, text="Songs", bg="grey", fg="white")
        list_but.place(x=0, y=0)
        # Back to menu button
        menu_but = Button(self.win, text="Back to Menu", bg="grey", fg="white")
        menu_but.place(x=0, y=0)
        # Scroll bar
        vbar = Scrollbar(self.canvas_frame, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=vbar.set)
        self.canvas.pack()
        self.set_songs()

        self.win.mainloop()

    def play_song(self, node):
        full_str = r'C:\Users\Jinsung\Downloads\downloadbash' + "\\" + node.get_song()
        self.index = node.get_index()
        # mixer.pre_init(48000, -16, 2, 4096)
        mixer.music.load(full_str)
        # mixer.music.play(2)
        mixer.music.play()
        self.label1['text'] = "Now Playing:  " + node.get_song()
        self.label1.place(x=270, y=50)
        self.queue()
        # pygame.mixer.music.load(next_string)

    def queue(self):
        pos = pygame.mixer.music.get_pos()
        if int(pos) == -1:
            self.next_song()
            # pygame.mixer.music.load(str1)
            # pygame.mixer.music.play()
            # self.index += 1
        self.win.after(1, self.queue)

    def set_songs(self):
        self.canvas['scrollregion'] = (0, 0, 200, (len(self.song_list) - 2) * 77)
        y_coor = 0
        buttons = []
        i = 0
        for songs in self.song_list:
            buttons.append(
                tk.Button(self.canvas, text=songs, command=lambda c=Node(songs, i): self.play_song(c),
                          bg="black", fg="white", height=3, width=85))
            self.canvas.create_window(-1, y_coor, anchor=NW, window=buttons[i])
            y_coor += 55
            i += 1

    def next_song(self):
        node = Node(self.song_list[self.index + 1], self.index + 1)
        self.play_song(node)

    def prev_song(self):
        node = Node(self.song_list[self.index - 1], self.index - 1)
        self.play_song(node)

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
