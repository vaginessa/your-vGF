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

root = tkinter.Tk()
root.title("vGF - zGUI™")

global ame # ADDED THIS

global mood 


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
    def __init__(self, name, happiness , affection):
        self._name = name
        self._happiness = happiness
        self._affection = affection
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
        # self._happiness = happiness

        if happiness >= 100:
            r = random.choice(os.listdir(happy_image))
            img=ImageTk.PhotoImage(os.path.join(happy_image, r))
            happy100 = tkinter.Label(mood_frame, image=img)
            happy100.pack(side=tkinter.LEFT)
    
            print("happiness is at 100")
            self._happiness  = 100

        elif ame._happiness <75 and happiness >= 75:
            r = random.choice(os.listdir(happy_image))
            img=ImageTk.PhotoImage(os.path.join(happy_image, r))
            happy100 = tkinter.Label(mood_frame, image=img)
            happy100.pack(side=tkinter.LEFT)
            
            print("happiness is > 75")
            self._happiness = happiness

        elif happiness <= 25:
            r = random.choice(os.listdir(happy_image))
            img=ImageTk.PhotoImage(os.path.join(happy_image, r))
            happy100 = tkinter.Label(mood_frame, image=img)
            happy100.pack(side=tkinter.LEFT)
            
            print("happiness is < 25")
            self._happiness = happiness
        elif happiness <= 0:
            r = random.choice(os.listdir(happy_image))
            img=ImageTk.PhotoImage(os.path.join(happy_image, r))
            happy100 = tkinter.Label(mood_frame, image=img)
            happy100.pack(side=tkinter.LEFT)
            
            print("happiness is at 0")
            self._happiness = 0

        else:
            self._happiness = happiness

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

    @property
    def affection(self):
        return self._affection
    
    @affection.setter
    def affection(self, affection):
        if affection >= 100:
            #Trigger Event
            print("affection is at 100")
            self._affection  = 100
        elif affection <= 0:
            #Trigger Event
            print("affection is at 0")
            self._affection = 0
        else:
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
            # ame.happiness = 1000
            print(f"Name is {ame.name}, happiness is {ame.happiness}, affection is {ame.affection}")
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
    # global ame
    task_index = task_listbox.curselection()[0]
    task_string = str(task_listbox.get(task_index)).lower()
    task_listbox.delete(task_index)
    popupimage()

    # if any(substring.lower() in task_string.lower() for substring in rewards.keys()):
    #     mood.set(mood.get() + rewards[''])

    substrings = task_string.split()
    for substring in substrings:
        if substring in rewards.keys():
            ame.happiness = (ame.happiness + rewards[substring])
            # print(ame)
        else:
            ame.happiness =  (ame.happiness + 1)
    # print(ame.happiness)
    mood.set(ame.happiness)
 
def fail_task():
    global top
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

    title_list = ['Tsk.', 'What the hell.', 'Disappointing.','Get out of my sight.','There is something seriously wrong with you.', 'Loser']

    if ame.happiness >= 50:
        top = Toplevel(root)
        top.title(random.choice(title_list))
        kangeldisappointed()
    elif ame.happiness <50:
        top = Toplevel(root)
        top.title(random.choice(title_list))
        amedisappointed()

    response_list = ['Sorry..', "It won't happen again...", "I'm sorry...", "Please don't leave..."]
    button = Button(top, text=random.choice(response_list), command=top.destroy).pack()
        

# GUI

#Popup Texts
def popuptextencourage():
    tkinter.messagebox.showinfo("Happy", random.choice("Its so nice to feel special for once... To love someone more than anything in the world and have them love me back", "Everybody has a little raincloud form time to time. But sad poems can give the little raincloud a lil' hug! To make a nice happy rainbow!", "You’re always thinking about other people. You need to think of yourself once in a while. If you don’t, you might end up getting hurt at some point.", "You make me unbelievably proud, today and every day."))



#Images and choices questioning if finished task on task completion

def popupimage():
    #For images to pop out
    global img
    global top
    if ame.happiness >= 50:
        top = Toplevel(root)
        ask_list = ['Did my baby finish their work?', '^w^ Baby finished?', 'My cutie baby finished yet~?', "<3 Baby I'm lonely~ Done yet~?"]
        top.title(random.choice(ask_list))
        r = random.choice(os.listdir(asking_image))
        img=ImageTk.PhotoImage(Image.open(os.path.join(asking_image, r)))
        label = Label(top, image = img)
        label.pack()

    elif ame.happiness <50:
        top = Toplevel(root)
        ask_list = ['Huh? You finished?', 'Finished?', "Hm.. You're done?", "Done?"]
        top.title(random.choice(ask_list))
        r = random.choice(os.listdir(asking_image1))
        img=ImageTk.PhotoImage(Image.open(os.path.join(asking_image1, r)))
        label = Label(top, image = img)
        label.pack()
    button = Button(top, text='Did you finish?', command=open_img).pack()
 
def open_img():
    btn1=Button(top, text="Yes!", fg='blue', command =btn1_clicked)
    btn1.place(x=80, y=50)
    btn2=Button(top, text="No!", fg='red', command =btn2_clicked)
    btn2.place(x=240, y=50)


def btn1_clicked():
    topclear_frame()
    happy_list1 = ['Good boy! ^w^', 'You cutie! A reward for you! uwu', 'I love you~! <3', 'My capable lover~ Kyaa~~', 'Come ere my baby~!', 'Awww~ Lookie you~']
    top.title(random.choice(happy_list1))
    if ame.happiness >= 50:
        kangelselfie()
    
    elif ame.happiness <50:
        ameselfie()


    response_list = ['Hehe~', 'I love you~', 'Thanks baby~', 'Wubbie chu~', '>;3 Yay~']
    button = Button(top, text=random.choice(response_list), command=top.destroy).pack()



def btn2_clicked():
    topclear_frame()
    ame.happiness = (ame.happiness - 2)
    mood.set(ame.happiness)
    disappointed_list1 = ['How dare you lie to me...', 'I am disappointed in you for lying.', 'You liar!', 'Liar. Tsk.', '#41>?215?3!3']
    top.title(random.choice((disappointed_list1)))
    if ame.happiness >= 50:
        kangeldisappointed()
    elif ame.happiness <50:
        amedisappointed()
        
    response_list = ['Sorry..', "It won't happen again...", "I'm sorry...", "Please don't leave..."]
    button = Button(top, text=random.choice(response_list), command=top.destroy).pack()

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
   for widgets in root.winfo_children():
      widgets.destroy()

def topclear_frame():
   for widgets in top.winfo_children():
      widgets.destroy()

# Mood Bar Frame

mood_frame = tkinter.Frame(root)
mood_frame.pack()

resized_image= heart_sprite.resize((25,25))
temp = ImageTk.PhotoImage(resized_image)
heart_label = tkinter.Label(mood_frame, image=temp)
heart_label.place(x = 1, y = 1)
heart_label.pack(side=tkinter.LEFT)



mood_bar = Progressbar(mood_frame, variable= mood, orient=tkinter.HORIZONTAL, length=250, mode="determinate")
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

complete_task_button = tkinter.Button(root, text="Task Completed", width=48, command=complete_task)
complete_task_button.pack()

failed_task_button = tkinter.Button(root, text="Task Failed", width=48, command=fail_task)
failed_task_button.pack()

#Scrollbar








































#init main(), put this last
if __name__ == "__main__":

    main()

    root.mainloop() # MOVED
