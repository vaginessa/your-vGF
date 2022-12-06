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




#declare assets and variables
tk_root = Tk()
tk_root.configure()
tk_root.title("vGF - zGUI™")

tk_happiness_stat = tkinter.DoubleVar()
tk_affection_stat = tkinter.DoubleVar()

init_sprite = r"./resources/init_sprite.png"
happy_icon = r"./resources/happy_icon.png"
sad_icon = r"./resources/sad_icon.png"
affection_icon = r"./resources/heart_icon.png"
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
            get_stat_update("happiness", self._affection, affection_bonus)
        if stat[2] == 3 and happiness > self._happiness:
            affection_bonus = self._affection + 1
            get_stat_update("happiness", self._affection, affection_bonus)
        if stat[2] == 2 and happiness < self._happiness:
            affection_bonus = self._affection - 1
            get_stat_update("happiness", self._affection, affection_bonus)
        if stat[2] == 1 and happiness < self._happiness:
            affection_bonus = self._affection - 3
            get_stat_update("happiness", self._affection, affection_bonus)

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

class RandomEventTimer(th.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

class TaskEventTimer(th.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


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
    dev_console()
    







#backend functions

#initiate if no saved file
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
                #add tasks to gui
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

def update_char_name(name):
    ame.name = name
    write_save()

def create_task(name, time):
    for task in tasks:
        if name in task["name"]:
            return("\n###Enter another name###\n")
    try:
        time = float(time)
    except ValueError:
        return("###Enter a number###")
    tasks.append({"name": name, "time": time})
    write_save()

def delete_task(name):
    del_task = (next((index for (index, d) in enumerate(tasks) if d["name"] == name), None))
    if del_task:
        tasks.pop(del_task)
    else:
        return "\n###Task not found###\n"
    write_save()

def get_stat_update(stat_type, old, new):
    stages = ["0", "1-25", "25-50", "50-75", "75-99", "100"]
    old_stage = bisect.bisect([1, 25, 50, 75, 100], old)
    new_stage = bisect.bisect([1, 25, 50, 75, 100], new)
    if old_stage != new_stage:
        update_main(new_stage)
    return [stat_type, old_stage, new_stage]

def start_random_event(interval):
    global random_event_timer
    random_event_timer = RandomEventTimer(interval, random_event)
    random_event_timer.start()

def random_event():
    global active_event
    while active_event:
        time.sleep(5)
    active_event = True
    ctypes.windll.user32.MessageBoxW(0, "Surprise!", "Random event", 1)
    active_event = False

def start_task_timer(name, time):
    global task_event_timer
    time = round(float(time) * 60)
    task_event_timer = TaskEventTimer(time, task_event, [name])
    task_event_timer.start()

def task_event(name):
    global active_event
    while active_event:
        time.sleep(5)
    active_event = True
    ctypes.windll.user32.MessageBoxW(0, f"Task: {name}", f"Time's up!", 1)
    task_event_timer.cancel()
    active_event = False
    delete_task(name)






#tkinter elements
main_dialogue_text = ""

def init():
    global main_sprite
    if new_save:
        main_frame.grid(row=2, column=0)
        main_dialogue_text = "What do you want to call me uWu?~~"
        main_dialogue_label.config(text = main_dialogue_text)
        main_sprite_display = tkinter.Label(main_frame, image = main_sprite)
        main_sprite_display.grid(row=0, column=0)
        main_dialogue_label.grid(row=1, column=0)
        main_entry1.grid(row=2, column=0)
        main_button1.grid(row=3, column=0)
    else:
        init_main()

def submit_name():
    if main_entry1.get():
        update_char_name(main_entry1.get())
        init_main()
        update_main(3)
    
def init_main():
    stat_bar_frame.grid(row=0, column=0)
    main_frame.grid(row=1, column=0)
    update_gui_stats()
    happiness_bar.grid(row=0, column=1, padx = 10, pady = 10)
    affection_bar.grid(row=1, column=1, padx = 10, pady = 10)
    affection_sprite_display = tkinter.Label(stat_bar_frame, image = affection_sprite)
    affection_sprite_display.grid(row=1, column=0, padx = 10, pady = 10)
    stage = bisect.bisect([1, 25, 50, 75, 100], ame.happiness)
    update_main(stage)

def update_gui_stats():
    happiness_sprite_display = tkinter.Label(stat_bar_frame, image = happy_sprite)
    happiness_sprite_display.grid(row=0, column=0,  padx = 10, pady = 10)
    if ame.happiness >= 50:
        happiness_sprite_display.config(image = (happy_sprite))
    else:
        happiness_sprite_display.config(image = (sad_sprite))
    happiness_bar.config(variable = tk_happiness_stat)
    affection_bar.config(variable = tk_affection_stat)

def update_main(stage):
    global main_sprite
    dir = r"./resources/stage_" + str(stage)
    r = random.choice(os.listdir(dir))
    main_sprite = ImageTk.PhotoImage(Image.open(os.path.join(dir, r)).resize((522, 340)))
    main_sprite_display = tkinter.Label(main_frame, image = main_sprite)
    main_sprite_display.grid(row=0, column=0)
    main_dialogue_text = random.choice(diag_small_talk)
    main_dialogue_label.config(text = main_dialogue_text)
    main_dialogue_label.grid(row=1, column=0)
    
    

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
main_entry1 = Entry(main_frame)
main_button1 = Button(main_frame, text= "Submit", padx = 20, command=submit_name)
tk_root.after_idle(init)

#task elements
task_frame = tkinter.Frame(tk_root)

#dev console elements
console_frame = tkinter.Frame(tk_root)
console_label_text = "\nDev console\n\n1: Show stats\n2: Modify stats\n3: List tasks\n4: Create task\n5: Delete task\n6: Random event interval\n7: Start random events\n8: Stop random events\nEnter an option:"


#init main(), put this last
if __name__ == "__main__":
    main()



###to do, complete task, adjust meters, function to change sprite