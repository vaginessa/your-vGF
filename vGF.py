import tkinter
import tkinter.messagebox
from tkinter.ttk import Progressbar
from tkinter import *
from PIL import Image, ImageTk
import time
from random import *
import json
import os

root = tkinter.Tk()
root.title("vGF - zGUI™")

#For images to pop out

win = Tk()
win.title("Finish?")
win.geometry("500x500")
frame = Frame(win, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

# Assets 

heart_sprite = Image.open('./images/heart_sprite.png')

sprites = {"happy": './images/.png' , "sad": './images/.png' , "angry": './images/.png'} # List of sprite directories

# Assets for Ame

selfie_image1 = r"./resources/ame/Selfies"
disappointed_image1 = r"./resources/ame/Disappointed"
asking_image1 = r"./resources/ame/Asking"
happy_image1 = r"./resources/ame/Happy"
pillow_image1 = r"./resources/ame/Pillow"

#Assets for Kangel

selfie_image = r"./resources/kangel/Selfies"
disappointed_image = r"./resources/kangel/Disappointed"
asking_image = r"./resources/kangel/Asking"
happy_image = r"./resources/kangel/Happy"
yandere_image = r"./resources/kangel/Yandere"

#class for character
class Ame:

    valid_range = range(0, 100) #sets allowed value for stats

    #initialise the class
    def __init__(self, name, happiness , affection):
        self._name = name
        self._happiness = happiness
        self._affection = affection

    #getter and setters for happiness and affection, trigger events for certain thresholds
    @property
    def name(self):
        return self._name

    @property
    def happiness(self):
        return self._happiness
    
    @happiness.setter
    def happiness(self, happiness):
        if happiness >= 100:
            #trigger event
            print("happiness is at 100")
            self._happiness = 100
        elif happiness <= 0:
            #trigger event
            print("happiness is at 0")
            self._happiness = 0
        self._happiness = happiness
            
    @property
    def affection(self):
        return self._affection
    
    @affection.setter
    def affection(self, affection):
        if affection >= 100:
            #trigger event
            print("affection is at 100")
            self._affection  = 100
        elif affection <= 0:
            #trigger event
            print("affection is at 0")
            self._affection = 0
        self._affection = affection

rewards = {'trash': 1, 'homework': 2, 'project': 5, 'work': 2, 'call': 1, 'book': 2, 'doctor': 2, 'dishes': 2,
    'chores': 3, 'chore': 3,}

# Logic

def main():
    global ame
    #check if a saved file exists
    if check_save():
        with open('./save.json') as json_file:
            data = json.load(json_file)
            name = data["name"]
            happiness = data["happiness"]
            affection = data["affection"]
            ame = Ame(name, happiness, affection)
    else:
        init_ame()

def check_save():
    return os.path.isfile("./save.json")

#initiate if no saved file
def init_ame():
    global ame
    name = input("Enter name : ")
    ame = Ame(name, 50, 20)
    #print(f"Name is {ame.name}, happiness is {ame.happiness}, affection is {ame.affection}")
    write_save()

#write to save file
def write_save():
    data = {"name": ame.name, "happiness": ame.happiness, "affection": ame.affection}
    with open('./save.json', 'w') as outfile:
        json.dump(data, outfile)

def add_task():
    task = task_entry.get()
    if task != '':
        task_listbox.insert(tkinter.END, task)
        task_entry.delete(0, tkinter.END)
    else:
        tkinter.messagebox.showwarning(title="Warning!", message="Please enter a task.")

def complete_task():
    task_index = task_listbox.curselection()[0]
    task_string = str(task_listbox.get(task_index)).lower()
    task_listbox.delete(task_index)

    # if any(substring.lower() in task_string.lower() for substring in rewards.keys()):
    #     mood.set(mood.get() + rewards[''])

    substrings = task_string.split()
    for substring in substrings:
        if substring in rewards.keys():
            ame.happiness = (ame.happiness + rewards[substring])
 
def fail_task():
    task_index = task_listbox.curselection()[0]
    task_string = str(task_listbox.get(task_index)).lower()
    task_listbox.delete(task_index)

    # if any(substring.lower() in task_string.lower() for substring in rewards.keys()):
    #     mood.set(mood.get() + rewards[''])

    substrings = task_string.split()
    for substring in substrings:
        if substring in rewards.keys():
            ame.happiness = (ame.happiness - rewards[substring])

# GUI

#Images and choices whether finished task

def beginning():
    global img
    r = random.choice(os.listdir(asking_image))
    img=ImageTk.PhotoImage(Image.open(os.path.join(asking_image, r)))
    label = Label(frame, image = img)
    label.pack()
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

# Mood Bar Frame

mood_frame = tkinter.Frame(root)
mood_frame.pack()

resized_image= heart_sprite.resize((25,25))
temp = ImageTk.PhotoImage(resized_image)
heart_label = tkinter.Label(mood_frame, image=temp)
heart_label.place(x = 1, y = 1)
heart_label.pack(side=tkinter.LEFT)

mood_bar = Progressbar(mood_frame, variable=ame.happiness, orient=tkinter.HORIZONTAL, length=250, mode="determinate")
mood_bar.pack(side=tkinter.RIGHT)


# Task Frame

task_frame = tkinter.Frame(root)
task_frame.pack()

task_listbox = tkinter.Listbox(task_frame, height=3, width=50)
task_listbox.pack(side=tkinter.LEFT)

scrollbar = tkinter.Scrollbar(task_frame)

task_listbox.config(yscrollcommand=scrollbar.set) # For scrolling functionality
scrollbar.config(command=task_listbox.yview) # For scrolling functionality

scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)



task_entry = tkinter.Entry(root, width=50)
task_entry.pack()

add_task_button = tkinter.Button(root, text="Add Task", width=48, command=add_task)
add_task_button.pack()

complete_task_button = tkinter.Button(root, text="Delete Task", width=48, command=complete_task)
complete_task_button.pack()

failed_task_button = tkinter.Button(root, text="Task failed", width=48, command=fail_task)
failed_task_button.pack()

#Scrollbar





































root.mainloop()

#init main(), put this last
if __name__ == "__main__":
    main()