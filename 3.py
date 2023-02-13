from tkinter import *
import configparser
from pynput import keyboard
import pyperclip
import tools
import os
from tkinter.filedialog import askdirectory
import pyglet
import tkinter.font as tkFont
pyglet.font.add_file("font.ttf")

fff = pyglet.font.load("SF Mono SC")

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
window = Tk()
bg='#FFFFFF'
window.configure(bg=bg)
aa, bb, path = StringVar(), StringVar(), StringVar()
path.set(os.path.join(os.path.expanduser('~'), "Desktop"))
old = None
p_old = None
id, key = '', ''
print(len(tkFont.families()))