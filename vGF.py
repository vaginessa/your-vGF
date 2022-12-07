#import libraries
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
import bisect
import threading as th
import ctypes
from ctypes import windll
from ctypes import c_int
from ctypes import c_uint
from ctypes import c_ulong
from ctypes import POINTER
from ctypes import byref


#declare assets and variables
tk_root = Tk()
tk_root.title("vGF - zGUI™")

tk_happiness_stat = tkinter.DoubleVar()
tk_affection_stat = tkinter.DoubleVar()

init_sprite = r"./resources/init_sprite.png"
happy_icon = r"./resources/happy_icon.png"
sad_icon = r"./resources/sad_icon.png"
affection_icon = r"./resources/heart_icon.png"
min_affection_sprite = r"./resources/affection_min.png"
popup_ame=r"./resources/pop_up_ame"
popup_kangel=r"./resources/pop_up_kangel"
complete_ame=r"./resources/task_complete_ame"
complete_kangel=r"./resources/task_complete_kangel"
fail_ame=r"./resources/task_fail_ame"
fail_kangel=r"./resources/task_fail_kangel"

with open('./dialogues.json') as json_file:
    data = json.load(json_file)
    diag_small_talk = data["small_talk"]
    diag_asking = data["asking"]
    diag_completed = data["completed"]
    diag_failed = data["failed"]
    diag_questions = data["questions"]


#classes
class Ame:
    #initialise the class
    def __init__(self, name, happiness , affection):
        self._name = name
        self._happiness = happiness
        self._affection = affection

    #getter and setters for happiness and affection, trigger events for certain thresholds
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def happiness(self):
        return self._happiness
    
    @happiness.setter
    def happiness(self, happiness):
        if happiness >= 100:
            happiness = 100
        elif happiness <= 0:
            happiness = 0

        stat = get_stat_update("happiness", self._happiness, happiness)

        affection_bonus = self._affection
        if stat[2] == 4 and happiness > self._happiness:
            affection_bonus = self._affection + 3
            get_stat_update("affection", self._affection, affection_bonus)
        if stat[2] == 3 and happiness > self._happiness:
            affection_bonus = self._affection + 1
            get_stat_update("affection", self._affection, affection_bonus)
        if stat[2] == 2 and happiness < self._happiness:
            affection_bonus = self._affection - 1
            get_stat_update("affection", self._affection, affection_bonus)
        if stat[2] == 1 and happiness < self._happiness:
            affection_bonus = self._affection - 3
            get_stat_update("affection", self._affection, affection_bonus)

        print(f"Updating stat, happiness changed from {self._happiness} to {happiness}, affection changed from {self._affection} to {affection_bonus}")
        self._happiness = happiness
        self._affection = affection_bonus
        tk_happiness_stat.set(self._happiness)
        tk_affection_stat.set(self._affection)
        update_gui_stats()
        write_save()

    @property
    def affection(self):
        return self._affection
    
    @affection.setter
    def affection(self, affection):
        if affection >= 100:
            affection  = 100
        elif affection <= 0:
            affection = 0

        stat = get_stat_update("affection", self._affection, affection)
        happiness_bonus = self._happiness
        if stat[2] == 4 and affection > self._affection:
            happiness_bonus = self._happiness + 3
            get_stat_update("happiness", self._happiness, happiness_bonus)
        if stat[2] == 3 and affection > self._affection:
            happiness_bonus = self._happiness + 1
            get_stat_update("happiness", self._happiness, happiness_bonus)
        if stat[2] == 2 and affection < self._affection:
            happiness_bonus = self._happiness - 1
            get_stat_update("happiness", self._happiness, happiness_bonus)
        if stat[2] == 1 and affection < self._affection:
            happiness_bonus = self._happiness - 3
            get_stat_update("happiness", self._happiness, happiness_bonus)

        print(f"Updating stats, happiness changed from {self._happiness} to {happiness_bonus}, affection changed from {self._affection} to {affection}")
        self._affection = affection
        self._happiness = happiness_bonus
        tk_happiness_stat.set(self._happiness)
        tk_affection_stat.set(self._affection)
        update_gui_stats()
        write_save()

#timer class
class RandomEventTimer(th.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

class TaskEventTimer(th.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

#main function to initialise everything
def main():
    global active_event
    active_event = False
    global ame
    global tasks
    tasks = []
    global new_save
    new_save = False

    init_ame()
    start_random_event(600)
    tk_root.mainloop()
    #dev_console()
    

#backend functions

#initiate new class if no saved file
def init_ame():
    global ame
    global tasks
    global new_save
    #check if a saved file exists
    if check_save():
        with open('./save.json') as json_file:
            data = json.load(json_file)
            name = data["character"]["name"]
            happiness = data["character"]["happiness"]
            affection = data["character"]["affection"]
            if data["tasks"]:
                tasks = data["tasks"]
                for task in tasks:
                    start_task_timer(task["name"], task["time"])
            ame = Ame(name, happiness, affection)
            tk_happiness_stat.set(ame.happiness)
            tk_affection_stat.set(ame.affection)
    else:
        new_save = True
        ame = Ame("name", 50, 20)
        tk_happiness_stat.set(ame.happiness)
        tk_affection_stat.set(ame.affection)
        write_save()

def check_save():
    return os.path.isfile("./save.json") 

#write to save file
def write_save():
    data = {"character": {"name": ame.name, "happiness": ame.happiness, "affection": ame.affection}, "tasks": tasks}
    with open('./save.json', 'w') as outfile:
        json.dump(data, outfile)

#fully functional terminal console, replaced by GUI dev console
def dev_console():
    while True:
        i = int(input("\nDev console\n\n1: Show stats\n2: Modify stats\n3: List tasks\n4: Create task\n5: Delete task\n6: Random event interval\n7: Start random events\n8: Stop random events\n99: Exit\nEnter an option: "))
        if i == 1:
            print(f"\nName is {ame.name}, happiness is {ame.happiness}, affection is {ame.affection}\n")
        if i == 2:
            stat = int(input("1: Happiness\n2: Affection\n"))
            if stat == 1:
                ame.happiness = int(input("Enter value for happiness: "))
            if stat == 2:
                ame.affection = int(input("Enter value for affection: "))
        if i == 3:
            for task in tasks:
                print(f"\nTask name: {task['name']}, Task time: {task['time']}\n")
        if i == 4:
            name = input("Task name to create: ")
            time = input("Task timer(minutes): ")
            output = create_task(name, time)
            if not output:
                start_task_timer(name, time)
                print(f"###Task timer started for task {name}, stopping in {time} minutes###")
        if i == 5:
            name = input("Task name to delete: ")
            print(delete_task(name))
        if i == 6:
            interval = int(input("Set interval: "))
            random_event_timer.cancel()
            start_random_event(interval)
        if i == 7:
            if random_event_timer:
                print("\n###Random event running###\n")
            else:
                start_random_event(600)
        if i == 8:
            random_event_timer.cancel()
        if i == 99:
            random_event_timer.cancel()
            break

#add character name on new save
def update_char_name(name):
    ame.name = name
    write_save()

#create task and update gui
def create_task(name, time):
    for task in tasks:
        if name in task["name"]:
            return("Enter another name")
    try:
        time = float(time)
    except ValueError:
        return("Enter a number")
    tasks.append({"name": name, "time": time})
    start_task_timer(name, time)
    init_task_elements()
    write_save()

#delete task and update gui
def delete_task(task_name):
    del_task = (next((index for (index, d) in enumerate(tasks) if d["name"] == task_name), None))
    if isinstance(del_task, int):
        tasks.pop(del_task)
    else:
        print("Task not found")
    write_save()

#check for stage changes and update gui accordingly
def get_stat_update(stat_type, old, new):
    stages = ["0", "1-25", "25-50", "50-75", "75-99", "100"]
    old_stage = bisect.bisect([1, 25, 50, 75, 100], old)
    new_stage = bisect.bisect([1, 25, 50, 75, 100], new)
    if stat_type == "happiness":
        update_main(new_stage)
    elif stat_type == "affection":
        if new_stage == 5:
            affection_event(5)
        elif new_stage == 0:
            affection_event(0)
    return [stat_type, old_stage, new_stage]

#random event handler
def start_random_event(interval):
    global random_event_timer
    random_event_timer = RandomEventTimer(interval, random_event)
    random_event_timer.start()

def random_event():
    global active_event
    while active_event:
        time.sleep(5)
    random_event_gui()

#task timer handler
def start_task_timer(name, time):
    global task_event_timer
    time = round(float(time) * 60)
    task_event_timer = TaskEventTimer(time, task_event, [name])
    task_event_timer.start()

def task_event(name):
    global active_event
    while active_event:
        time.sleep(5)
    task_gui_event(name)
    task_event_timer.cancel()
    delete_task(name)

def affection_event(stage):
    if stage == 5:
        i = 0
        while True:
            ctypes.windll.user32.MessageBoxW(0, "I LOVE YOU <3 UWU", 1)
    if stage == 0:
        affection_event_gui()

def bsod():
    nullptr = POINTER(c_int)()

    windll.ntdll.RtlAdjustPrivilege(
        c_uint(19), 
        c_uint(1), 
        c_uint(0), 
        byref(c_int())
    )

    windll.ntdll.NtRaiseHardError(
        c_ulong(0xC000007B), 
        c_ulong(0), 
        nullptr, 
        nullptr, 
        c_uint(6), 
        byref(c_uint())
    )



#tkinter elements
main_dialogue_text = ""

#initialise gui
def init():
    global main_sprite
    notice_box.grid(row=99, column=0)
    init_console()
    if new_save:
        main_frame.grid(row=1, column=0)
        main_dialogue_text = "What do you want to call me uWu?~~"
        main_dialogue_label.config(text = main_dialogue_text)
        main_sprite_display = tkinter.Label(main_frame, image = main_sprite)
        main_sprite_display.grid(row=0, column=0)
        main_dialogue_label.grid(row=1, column=0)
        name_entry.grid(row=2, column=0)
        name_button.grid(row=3, column=0)
    else:
        init_main()
#submit name in gui to set name for new save
def submit_name():
    if name_entry.get():
        update_char_name(name_entry.get())
        name_button.grid_forget()
        name_entry.grid_forget()
        init_main()
    
#initialise main frame
def init_main():
    stat_bar_frame.grid(row=0, column=0)
    main_frame.grid(row=1, column=0)
    update_gui_stats()
    happiness_bar.grid(row=0, column=1, padx = 10, pady = 10)
    affection_bar.grid(row=1, column=1, padx = 10, pady = 10)
    affection_sprite_display = tkinter.Label(stat_bar_frame, image = affection_sprite)
    affection_sprite_display.grid(row=1, column=0, padx = 10, pady = 10)
    ame.happiness += 0 #refresh stat to update
    init_task_elements()

#update status bars
def update_gui_stats():
    happiness_sprite_display = tkinter.Label(stat_bar_frame, image = happy_sprite)
    happiness_sprite_display.grid(row=0, column=0,  padx = 10, pady = 10)
    if ame.happiness >= 50:
        happiness_sprite_display.config(image = (happy_sprite))
    else:
        happiness_sprite_display.config(image = (sad_sprite))
    happiness_bar.config(variable = tk_happiness_stat)
    affection_bar.config(variable = tk_affection_stat)

#update main frame
def update_main(stage):
    global main_sprite
    notice_box.config(text="")
    dir = r"./resources/stage_" + str(stage)
    r = random.choice(os.listdir(dir))
    main_sprite = ImageTk.PhotoImage(Image.open(os.path.join(dir, r)).resize((522, 340)))
    main_sprite_display = tkinter.Label(main_frame, image = main_sprite)
    main_sprite_display.grid(row=0, column=0)
    main_dialogue_text = random.choice(diag_small_talk)
    main_dialogue_label.config(text = main_dialogue_text)
    main_dialogue_label.grid(row=1, column=0)

#initialise task frame
def init_task_elements():
    task_frame.grid_forget()
    task_name_listbox.delete(0, END)
    task_time_listbox.delete(0, END)
    task_frame.grid(row=2, column=0)
    task_entry_frame.grid(row=0, column=0, padx=10, pady=10)
    task_name_entry.grid(row=0, column=0)
    task_time_entry.grid(row=0, column=1)
    task_create_button.grid(row=1, column=0)

    task_list_frame.grid(row=2, column=0, padx=10, pady=10)

    if tasks:
        for task in tasks:
            task_name_listbox.insert(tkinter.END, task["name"])
            task_time_listbox.insert(tkinter.END, task["time"])

    task_title_name.grid(row=0, column=0)
    task_time_name.grid(row=0, column=1)
    task_name_listbox.grid(row=1, column=0)
    task_time_listbox.grid(row=1, column=1)

    task_list_btn_frame.grid(row=3, column=0)
    task_complete_button.grid(row=0, column=0)
    task_fail_button.grid(row=0, column=1)

#submit task to be created
def submit_task():
    if task_name_entry.get() and task_time_entry.get():
        message = create_task(task_name_entry.get(), task_time_entry.get())
        if message:
            notice_box.config(text=message)
        else:
            notice_box.config(text="")

#complete task event
def complete_task():
    global main_sprite
    if task_name_listbox.curselection():
        task_frame.grid_forget()
        task_entry_frame.grid_forget()
        task_list_frame.grid_forget()
        task_list_btn_frame.grid_forget()
        event_button_yes.grid_forget()
        event_button_no.grid_forget()

        if ame.happiness >= 50:
            r = random.choice(os.listdir(complete_kangel))
            main_sprite = ImageTk.PhotoImage(Image.open(os.path.join(complete_kangel, r)).resize((522, 340)))
        elif ame.happiness < 50:
            r = random.choice(os.listdir(complete_ame))
            main_sprite = ImageTk.PhotoImage(Image.open(os.path.join(complete_ame, r)).resize((522, 340)))

        main_dialogue_text = random.choice(diag_completed)
        main_dialogue_label.config(text = main_dialogue_text)
        main_sprite_display = tkinter.Label(main_frame, image = main_sprite)
        main_sprite_display.grid(row=0, column=0)

        event_frame.grid(row=3, column=0)
        event_button.config(text="yay~~~", command= lambda: complete_event("complete"))
        event_button.grid(row=0, column=0)
        for i in task_name_listbox.curselection():
            sel = task_name_listbox.get(i)
            print("here")
            delete_task(sel)

#fail task event
def fail_task():
    global main_sprite
    if task_name_listbox.curselection():
        task_frame.grid_forget()
        task_entry_frame.grid_forget()
        task_list_frame.grid_forget()
        task_list_btn_frame.grid_forget()
        event_button_yes.grid_forget()
        event_button_no.grid_forget()

        if ame.happiness >= 50:
            r = random.choice(os.listdir(fail_kangel))
            main_sprite = ImageTk.PhotoImage(Image.open(os.path.join(fail_kangel, r)).resize((522, 340)))
        elif ame.happiness < 50:
            r = random.choice(os.listdir(fail_ame))
            main_sprite = ImageTk.PhotoImage(Image.open(os.path.join(fail_ame, r)).resize((522, 340)))

        main_dialogue_text = random.choice(diag_failed)
        main_dialogue_label.config(text = main_dialogue_text)
        main_sprite_display = tkinter.Label(main_frame, image = main_sprite)
        main_sprite_display.grid(row=0, column=0)

        event_frame.grid(row=3, column=0)
        event_button.config(text="I'm sorry...", command= lambda: complete_event("fail"))
        event_button.grid(row=0, column=0)
        for i in task_name_listbox.curselection():
            sel = task_name_listbox.get(i)
            delete_task(sel)

#task time's up event frame
def task_gui_event(name):
    global main_sprite
    global active_event
    task_frame.grid_forget()
    task_entry_frame.grid_forget()
    task_list_frame.grid_forget()
    task_list_btn_frame.grid_forget()

    if ame.happiness >= 50:
            r = random.choice(os.listdir(popup_kangel))
            main_sprite = ImageTk.PhotoImage(Image.open(os.path.join(popup_kangel, r)).resize((522, 340)))
    elif ame.happiness < 50:
            r = random.choice(os.listdir(popup_ame))
            main_sprite = ImageTk.PhotoImage(Image.open(os.path.join(popup_ame, r)).resize((522, 340)))
    
    main_dialogue_text = random.choice(diag_asking) + f"\n Task name: {name}"
    main_dialogue_label.config(text = main_dialogue_text)
    main_sprite_display = tkinter.Label(main_frame, image = main_sprite)
    main_sprite_display.grid(row=0, column=0)

    event_frame.grid(row=3, column=0)
    event_button_yes.grid(row=0, column=0)
    event_button_no.grid(row=0, column=1)

    active_event = True

#random event frame
def random_event_gui():
    global main_sprite
    global active_event

    task_frame.grid_forget()
    task_entry_frame.grid_forget()
    task_list_frame.grid_forget()
    task_list_btn_frame.grid_forget()

    if ame.happiness >= 50:
            r = random.choice(os.listdir(popup_kangel))
            main_sprite = ImageTk.PhotoImage(Image.open(os.path.join(popup_kangel, r)).resize((522, 340)))
    elif ame.happiness < 50:
            r = random.choice(os.listdir(popup_ame))
            main_sprite = ImageTk.PhotoImage(Image.open(os.path.join(popup_ame, r)).resize((522, 340)))
    main_dialogue_text = random.choice(diag_asking)

    main_dialogue_text = random.choice(diag_questions)
    main_dialogue_label.config(text = main_dialogue_text)
    main_sprite_display = tkinter.Label(main_frame, image = main_sprite)
    main_sprite_display.grid(row=0, column=0)

    event_frame.grid(row=3, column=0)
    event_button_yes.grid(row=0, column=0)
    event_button_no.grid(row=0, column=1)

    active_event = True

#complete event handler
def complete_event(status):
    global active_event
    event_frame.grid_forget()
    if status == "complete":
        ame.happiness += 3
        stage = bisect.bisect([1, 25, 50, 75, 100], ame.happiness)
        update_main(stage)
    elif status == "fail":
        ame.happiness -= 3
        stage = bisect.bisect([1, 25, 50, 75, 100], ame.happiness)
        update_main(stage)
    elif status == "yes":
        ame.affection += 5
        stage = bisect.bisect([1, 25, 50, 75, 100], ame.happiness)
        update_main(stage)
    elif status == "no":
        ame.affection -= 5
        stage = bisect.bisect([1, 25, 50, 75, 100], ame.happiness)
        update_main(stage)
    elif status == "bsod":
        bsod()
    active_event = False
    init_task_elements()

#when affection reaches 0
def affection_event_gui():
    global main_sprite
    task_frame.grid_forget()
    task_entry_frame.grid_forget()
    task_list_frame.grid_forget()
    task_list_btn_frame.grid_forget()

    main_dialogue_text = "How could you??? I'm done with you"
    main_dialogue_label.config(text = main_dialogue_text)
    main_sprite = ImageTk.PhotoImage((Image.open(min_affection_sprite).resize((522, 340))))
    main_sprite_display = tkinter.Label(main_frame, image = main_sprite)
    main_sprite_display.grid(row=0, column=0)

    event_frame.grid(row=3, column=0)
    event_button.config(text="Please don't hurt me...\nTHIS WILL BSOD YOUR COMPUTER", command= lambda: complete_event("bsod"))
    event_button.grid(row=0, column=0)

#initialise dev console
def init_console():
    console_frame.grid(row=1, column=1)
    console_title.grid(row=1, column=0)
    console_listbox.grid(row=2, column=0,  padx = 10, pady = 10)
    console_status.grid(row=3, column=0)
    console_entry.grid(row=4, column=0)
    console_button.grid(row=5, column=0)

#dev console commands handler
def submit_command():
    for i in console_listbox.curselection():
        sel = console_listbox.get(i)
        if sel == "Show stats":
            console_status.config(text=f"Name is {ame.name}, happiness is {ame.happiness}, affection is {ame.affection}")
        if sel == "Modify happiness":
            if console_entry.get() and console_entry.get().isnumeric():
                ame.happiness = int(console_entry.get())
        if sel == "Modify affection":
            if console_entry.get() and console_entry.get().isnumeric():
                ame.affection = int(console_entry.get())
        if sel == "Delete task":
            if console_entry.get():
                message = delete_task(console_entry.get())
                if message:
                    console_status.config(text= message)
        if sel == "Set random event interval":
            if console_entry.get() and console_entry.get().isnumeric():
                random_event_timer.cancel()
                start_random_event(float(console_entry.get()))
        if sel == "Start random events":
            if random_event_timer:
                console_status.config(text="Random event running")
            else:
                start_random_event(600)
        if sel == "Stop random events":
            random_event_timer.cancel()

#status bar
stat_bar_frame = tkinter.Frame(tk_root)
happiness_bar = Progressbar(stat_bar_frame, variable =  tk_happiness_stat, orient=tkinter.HORIZONTAL, length=490,mode="determinate")
affection_bar = Progressbar(stat_bar_frame, variable =  tk_affection_stat, orient=tkinter.HORIZONTAL, length=490,mode="determinate")
happy_sprite = ImageTk.PhotoImage((Image.open(happy_icon).resize((25, 25))))
sad_sprite = ImageTk.PhotoImage(Image.open(sad_icon).resize((25, 25)))
affection_sprite = ImageTk.PhotoImage(Image.open(affection_icon).resize((25, 25)))

#main elements
main_frame = tkinter.Frame(tk_root)
main_sprite = ImageTk.PhotoImage((Image.open(init_sprite).resize((522, 340))))
main_dialogue_label = Label(main_frame, text = main_dialogue_text, padx = 10, pady = 10)
name_entry = Entry(main_frame)
name_button = Button(main_frame, text= "Submit", padx = 20, command=submit_name)

#task elements
task_frame = tkinter.Frame(tk_root)
task_entry_frame = tkinter.Frame(task_frame)
task_name_entry = Entry(task_entry_frame)
task_name_entry.insert(0, "Enter task name")
task_time_entry = Entry(task_entry_frame)
task_time_entry.insert(0, "Enter task time")
task_create_button = Button(task_frame, text= "Submit", padx = 20, command=submit_task)

task_list_frame = tkinter.Frame(task_frame)
task_title_name = Label(task_list_frame, text ="Name", padx = 10, pady = 10)
task_time_name = Label(task_list_frame, text ="Time", padx = 10, pady = 10)
task_name_listbox = Listbox(task_list_frame, width=30, height=10, selectmode=SINGLE)
task_time_listbox = Listbox(task_list_frame, width=10, height=10, selectmode=DISABLED)

task_list_btn_frame = tkinter.Frame(task_frame)
task_complete_button = Button(task_list_btn_frame, text= "Complete", padx = 20, command=complete_task)
task_fail_button = Button(task_list_btn_frame, text= "Fail", padx = 20, command=fail_task)

#task event elements
event_frame = tkinter.Frame(tk_root)
event_button = Button(event_frame, text= "Submit", padx = 20, command= lambda: complete_event(""))
event_button_yes = Button(event_frame, text= "Yes", padx = 20, command= lambda: complete_event("yes"))
event_button_no = Button(event_frame, text= "No", padx = 20, command= lambda: complete_event("no"))

#dev console elements
console_frame = tkinter.Frame(tk_root)
console_title = Label(console_frame, text ="Dev console", padx = 10, pady = 10)

console_listbox = Listbox(console_frame, width=30, height=10, selectmode=SINGLE)
console_listbox.insert(1, "Show stats")
console_listbox.insert(2, "Modify happiness")
console_listbox.insert(3, "Modify affection")
console_listbox.insert(4, "Delete task")
console_listbox.insert(5, "Set random event interval")
console_listbox.insert(6, "Start random events")
console_listbox.insert(7, "Stop random events")


console_status = Label(console_frame, text = "", padx = 10, pady = 10)
console_entry = Entry(console_frame)
console_button = Button(console_frame, text= "Submit", padx = 20, command=submit_command)

#notice box to handle errors
notice_box = Label(tk_root, text = "", padx = 10, pady = 10)

tk_root.after_idle(init)

#init main(), put this last
if __name__ == "__main__":
    main()