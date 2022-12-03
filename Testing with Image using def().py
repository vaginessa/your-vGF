from tkinter import *
from PIL import ImageTk, Image
import os
import random

selfie_image = r"./resources/kangel/Selfies"
disappointed_image = r"./resources/kangel/Disappointed"
asking_image = r"./resources/kangel/Asking"
happy_image = r"./resources/kangel/Happy"
yandere_image = r"./resources/kangel/Yandere"

win = Tk()
win.title("Finish?")
win.geometry("500x500")
frame = Frame(win, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)
r = random.choice(os.listdir(asking_image))
img=ImageTk.PhotoImage(Image.open(os.path.join(asking_image, r)))
label = Label(frame, image = img)
label.pack()

def beginning():
    button = Button(win, text='Did you finish?', command=open_img).pack()
 
def open_img():
    clear_frame()
    btn1=Button(win, text="Yes!", fg='blue', command =btn1_clicked)
    btn1.place(x=80, y=50)
    btn2=Button(win, text="No!", fg='red', command =btn2_clicked)
    btn2.place(x=360, y=50)


def btn1_clicked():
    clear_frame()
    win.title("Good boy! ^w^")
    selfie()



def btn2_clicked():
    clear_frame()
    win.title("How dare you...")
    disappointed()

def selfie():
    global img
    r = random.choice(os.listdir(selfie_image))
    img=ImageTk.PhotoImage(Image.open(os.path.join(selfie_image, r)))
    label = Label(frame, image = img)
    label.pack()

def disappointed():
    global img
    r = random.choice(os.listdir(disappointed_image))
    img=ImageTk.PhotoImage(Image.open(os.path.join(disappointed_image, r)))
    label = Label(frame, image = img)
    label.pack()

def clear_frame():
   for widgets in frame.winfo_children():
      widgets.destroy()


beginning()
win.mainloop()