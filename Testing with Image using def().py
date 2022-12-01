from tkinter import *
from PIL import ImageTk, Image
import os

win = Tk()
win.title("Finish?")
win.geometry("500x500")
frame = Frame(win, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)
img = ImageTk.PhotoImage(Image.open("C:\\Users\\Edward\\Downloads\\ame sprites\\stream_ame_talk_003_0.png"))
label = Label(frame, image = img)
image = img
label.pack()

def beginning():
    button = Button(win, text='Did you finish?', command=open_img).pack()

def open_img():
    clear_frame()
    btn1=Button(win, text="Yes!", fg='blue', command =lambda: btn1_clicked)
    btn1.place(x=80, y=100)
    btn2=Button(win, text="No!", fg='red', command =lambda: btn2_clicked)
    btn2.place(x=200, y=100)


def btn1_clicked():
    win.title("Good boy! ^w^")
    img1=ImageTk.PhotoImage(Image.open("C:\\Users\\Edward\\Downloads\\twitter selfies\\twitter selfies\\tweet_selfie_ame_happy_001.png"))
    label.configure(img=img1)
    image = img1



def btn2_clicked(img):
    win.title("Bad boy...")
    label['img'] = ImageTk.PhotoImage("C:\\Users\\Edward\\Downloads\\ame sprites\\stream_ame_tv_004.png")

def clear_frame():
   for widgets in frame.winfo_children():
      widgets.destroy()


beginning()
win.mainloop()