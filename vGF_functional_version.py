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

global ame # ADDED THIS

global mood 

global current_sprite






mood = tkinter.DoubleVar()


# Assets 

heart_sprite = Image.open('./resources/heart_sprite.png')

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
    def __init__(self, name, happiness ):
        self._name = name
        self._happiness = happiness
        mood.set(happiness)

    #getter and setters for happiness and affection, trigger events for certain thresholds
    @property
    def name(self):
        return self._name

    @property
    def happiness(self):
        return self._happiness
    
    @happiness.setter
    def happiness(self, happiness):

        global current_sprite
        
     
        # self._happiness = happiness

        if happiness >= 100:
            #trigger event
            print("happiness is at 100")
            self._happiness  = 100

        elif happiness <= 0:
            #trigger event
            print("happiness is at 0")

            self._happiness = 0
        
        elif happiness >= 50:
            current_sprite = random_image("Happy")
        
            self._happiness = happiness

        elif happiness < 50:
            current_sprite = random_image("Disappointed")
       
            self._happiness = happiness
        else:
            self._happiness = happiness

        mood.set(happiness)


        with open('./save.json') as json_file:
            data = json.load(json_file)
            data["happiness"] = self._happiness
            data["current_sprite"] = current_sprite
            # print(data)
        with open('./save.json', 'w') as outfile:
            json.dump(data, outfile)

     




        # if self._happiness >= 100:
        #     #trigger event
        #     print("happiness is at 100")
        #     self._happiness = 100
        # if ame._happiness <75 and happiness >= 75:
        #     #trigger event
        #     print("happiness is > 75")
        #     self._happiness = happiness
        # if happiness <= 25:
        #     #trigger event
        #     print("happiness is < 25")
        #     self._happiness = happiness
        # elif happiness <= 0:
        #     #trigger event
        #     print("happiness is at 0")
        #     self._happiness = 0
        
        

rewards = {'trash': 1, 'homework': 2, 'project': 5, 'work': 2, 'call': 1, 'book': 2, 'doctor': 2, 'dishes': 2,
    'chores': 3, 'chore': 3,}

# Logic

def main():
    global ame
    global current_sprite
   
    #check if a saved file exists
    if check_save():
        with open('./save.json') as json_file:
            data = json.load(json_file)
            name = data["name"]
            happiness = data["happiness"]
     
            ame = Ame(name, happiness)
            current_sprite = data["current_sprite"]
            # ame.happiness = 1000
            print(f"Name is {ame.name}, happiness is {ame.happiness}")
    else:
        init_ame()
        # print(os.path.isdir("./save.json"))

def check_save():
    # cwd = os.getcwd() 
    # print(cwd)
    # path = os.path.join(cwd, "save.json")
    # print(os.path.isdir("./save.json"))
    # print(os.path.isfile("./save.json"))
    return os.path.isfile("./save.json") 

#initiate if no saved file
def init_ame():

    global ame
    global current_sprite
    
    

    name = input("Enter name : ")
    ame = Ame(name, 50)
    current_sprite = random_image("Happy")
    #print(f"Name is {ame.name}, happiness is {ame.happiness}, affection is {ame.affection}")
    write_save()

#write to save file
def write_save():

   
    global current_sprite
    data = {"name": ame.name, "happiness": ame.happiness, "tasks": [], "current_sprite": current_sprite}
    with open('./save.json', 'w') as outfile:
        json.dump(data, outfile)




# GUI

#Images and choices whether finished task


# def popup():
#     #For images to pop out
#     global win
#     global frame
#     win = Tk()
#     win.title("Finish?")
#     win.geometry("500x500")
#     frame = Frame(win, width=600, height=400)
#     frame.pack()
#     frame.place(anchor='center', relx=0.5, rely=0.5)
    
# def beginning():
#     global img
#     r = random.choice(os.listdir(asking_image))
#     img=ImageTk.PhotoImage(Image.open(os.path.join(asking_image, r)))
#     label = Label(frame, image = img)
#     label.pack()
#     button = Button(win, text='Did you finish?', command=open_img).pack()
 
# def open_img():
#     clear_frame()
#     btn1=Button(win, text="Yes!", fg='blue', command =btn1_clicked)
#     btn1.place(x=80, y=50)
#     btn2=Button(win, text="No!", fg='red', command =btn2_clicked)
#     btn2.place(x=360, y=50)


# def btn1_clicked():
#     clear_frame()
#     win.title("Good boy! ^w^")
#     ameselfie()



# def btn2_clicked():
#     clear_frame()
#     win.title("How dare you...")
#     amedisappointed()

#Clear Frame Command

# def clear_frame():
#    for widgets in frame.winfo_children():
#       widgets.destroy()

# Mood Bar Frame


import random

def random_image(emotion):
    if emotion not in {"Happy", "Disappointed", "Asking", "Pillow", ""}:
        raise Exception("No such folder")
    path = os.path.join(os.curdir, "resources", "ame", emotion.capitalize())
    # print(path)
    choice = random.choice(os.listdir(path))
    # print(choice)
    return(os.path.join(path, choice))



def tkinter_app():

    
    def add_task():
        task = task_entry.get()
        if task != '':
            task_listbox.insert(tkinter.END, task)
            task_entry.delete(0, tkinter.END)
        else:
            tkinter.messagebox.showwarning(title="Warning!", message="Please enter a task.")
            return()

        with open('./save.json') as file:
            data  = json.load(file)
            tasks = data["tasks"]
        tasks.append(task)
        with open('./save.json', 'w') as outfile:
            json.dump(data, outfile)


    def complete_task():
        # global ame
        task_index = task_listbox.curselection()[0]
    
        task_string = str(task_listbox.get(task_index))
        task_listbox.delete(task_index)

        # if any(substring.lower() in task_string.lower() for substring in rewards.keys()):
        #     mood.set(mood.get() + rewards[''])

        substrings = task_string.split()
        for substring in substrings:
            if substring.lower() in rewards.keys():
                ame.happiness = (ame.happiness + rewards[substring])
                # print(ame)
            else:
                ame.happiness =  (ame.happiness + 1)
        # print(ame.happiness)
        mood.set(ame.happiness)

        remove(task_string)

        
            
    
    def fail_task():
        # global ame
        task_index = task_listbox.curselection()[0]
        task_string = str(task_listbox.get(task_index)).lower()
        task_listbox.delete(task_index)

        # if any(substring.lower() in task_string.lower() for substring in rewards.keys()):
        #     mood.set(mood.get() + rewards[''])

        substrings = task_string.split()
        for substring in substrings:
            if substring in rewards.keys():
                ame.happiness = (ame.happiness - rewards[substring])
            else:
                ame.happiness = (ame.happiness - 1)
        mood.set(ame.happiness)
        remove(task_string)
        
    def remove(task_string):
        with open('./save.json') as file:
            data  = json.load(file)
            tasks = data["tasks"]
        tasks.pop(tasks.index(task_string))
        with open('./save.json', 'w') as outfile:
            json.dump(data, outfile)

    mood_frame = tkinter.Frame(root)
    mood_frame.pack()

    resized_image= heart_sprite.resize((25,25))
    temp = ImageTk.PhotoImage(resized_image)
    heart_label = tkinter.Label(mood_frame, image=temp)
    heart_label.place(x = 1, y = 1)
    heart_label.pack(side=tkinter.LEFT)



    mood_bar = Progressbar(mood_frame, variable= mood, orient=tkinter.HORIZONTAL, length=250, mode="determinate")
    mood_bar.pack(side=tkinter.RIGHT)

    # Sprite


    # heart_sprite = Image.open('./resources/heart_sprite.png')

    # ame_sprite = Image.open(random_image("Happy")).resize((300, 300))


    # current_sprite = random_image("Happy")




    ame_sprite = Image.open(current_sprite)
    temp = ImageTk.PhotoImage(ame_sprite)
    sprite_label = tkinter.Label(root, image= temp)
    sprite_label.pack()


    # Task Frame

    task_frame = tkinter.Frame(root)
    task_frame.pack()

    task_listbox = tkinter.Listbox(task_frame, height=3, width=50)

    with open('./save.json') as json_file:
        data = json.load(json_file)
        tasks = data["tasks"]
        if len(tasks) > 0:
            for task in tasks:
                task_listbox.insert(tkinter.END, task)
    task_listbox.pack(side=tkinter.LEFT)

    #Scrollbar

    scrollbar = tkinter.Scrollbar(task_frame)

    task_listbox.config(yscrollcommand=scrollbar.set) # For scrolling functionality
    scrollbar.config(command=task_listbox.yview) # For scrolling functionality

    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)


    task_entry = tkinter.Entry(root, width=50)
    task_entry.pack()

    add_task_button = tkinter.Button(root, text="Add Task", width=48, command=add_task)
    add_task_button.pack()

    complete_task_button = tkinter.Button(root, text="Task Completed", width=48, command=complete_task)
    complete_task_button.pack()

    failed_task_button = tkinter.Button(root, text="Task Failed", width=48, command=fail_task)
    failed_task_button.pack()

        



    root.mainloop() # MOVED









#init main(), put this last
if __name__ == "__main__":

    main()

    tkinter_app()


   
