import tkinter
import tkinter.messagebox
from tkinter.ttk import Progressbar
from tkinter import *
from PIL import Image, ImageTk
import time
from random import *
import random
import json
import os

selfie_image = r"./resources/kangel/Selfies"
disappointed_image = r"./resources/kangel/Disappointed"
asking_image = r"./resources/kangel/Asking"
happy_image = r"./resources/kangel/Happy"
yandere_image = r"./resources/kangel/Yandere"

selfie_image1 = r"./resources/ame/Selfies"
disappointed_image1 = r"./resources/ame/Disappointed"
asking_image1 = r"./resources/ame/Asking"
happy_image1 = r"./resources/ame/Happy"
pillow_image1 = r"./resources/ame/Pillow"

win = Tk()
win.title("Finish?")
win.geometry("500x500")
r = random.choice(os.listdir(asking_image))
img=ImageTk.PhotoImage(Image.open(os.path.join(asking_image, r)))
label = Label(win, image = img)
label.pack()

 
def open_img():
    clear_frame()
    global top
    global img
    top = Toplevel(win)
    top.title("Hmm?")
    r = random.choice(os.listdir(asking_image))
    img=ImageTk.PhotoImage(Image.open(os.path.join(asking_image, r)))
    label = Label(top, image = img)
    label.pack()
    btn1=Button(top, text="Yes!", fg='blue', command =btn1_clicked)
    btn1.place(x=80, y=50)
    btn2=Button(top, text="No!", fg='red', command =btn2_clicked)
    btn2.place(x=240, y=50)


def btn1_clicked():
    topclear_frame()
    top.title("Good boy! ^w^")
    ameselfie()



def btn2_clicked():
    topclear_frame()
    top.title("How dare you...")
    amedisappointed()

#Images for Ame

def ameselfie():
    global img
    r = random.choice(os.listdir(selfie_image1))
    img=ImageTk.PhotoImage(Image.open(os.path.join(selfie_image1, r)))
    label = Label(top, image = img)
    label.pack()

def amedisappointed():
    global img
    r = random.choice(os.listdir(disappointed_image1))
    img=ImageTk.PhotoImage(Image.open(os.path.join(disappointed_image1, r)))
    label = Label(top, image = img)
    label.pack()

def ameasking():
    global img
    r = random.choice(os.listdir(asking_image1))
    img=ImageTk.PhotoImage(Image.open(os.path.join(asking_image1, r)))
    label = Label(top, image = img)
    label.pack()

def amehappy():
    global img
    r = random.choice(os.listdir(happy_image1))
    img=ImageTk.PhotoImage(Image.open(os.path.join(happy_image1, r)))
    label = Label(top, image = img)
    label.pack()

def amepillow():
    global img
    r = random.choice(os.listdir(pillow_image1))
    img=ImageTk.PhotoImage(Image.open(os.path.join(pillow_image1, r)))
    label = Label(top, image = img)
    label.pack()

#Images for Kangel
def kangelselfie():
    global img
    r = random.choice(os.listdir(selfie_image))
    img=ImageTk.PhotoImage(Image.open(os.path.join(selfie_image, r)))
    label = Label(top, image = img)
    label.pack()

def kangeldisappointed():
    global img
    r = random.choice(os.listdir(disappointed_image))
    img=ImageTk.PhotoImage(Image.open(os.path.join(disappointed_image, r)))
    label = Label(top, image = img)
    label.pack()

def kangelasking():
    global img
    r = random.choice(os.listdir(asking_image))
    img=ImageTk.PhotoImage(Image.open(os.path.join(asking_image, r)))
    label = Label(top, image = img)
    label.pack()

def kangelhappy():
    global img
    r = random.choice(os.listdir(happy_image))
    img=ImageTk.PhotoImage(Image.open(os.path.join(happy_image, r)))
    label = Label(top, image = img)
    label.pack()

def kangelyandere():
    global img
    r = random.choice(os.listdir(yandere_image))
    img=ImageTk.PhotoImage(Image.open(os.path.join(yandere_image, r)))
    label = Label(top, image = img)
    label.pack()

#Clear Frame Command

def clear_frame():
   for widgets in win.winfo_children():
      widgets.destroy()

def topclear_frame():
   for widgets in top.winfo_children():
      widgets.destroy()


button = Button(win, text='Did you finish?', command=open_img).pack()
win.mainloop()