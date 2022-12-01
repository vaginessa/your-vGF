import tkinter
import tkinter.messagebox
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk

root = tkinter.Tk()
root.title("Virtual Girlfriend")

# Assets 

heart_sprite = Image.open('./images/heart_sprite.png')

sprites = {"happy": './images/.png' , "sad": './images/.png' , "angry": './images/.png'} # List of sprite directories

# Global Variables

global mood 
mood = tkinter.DoubleVar()  # Mood variable, use mood.set() to change
mood.set(50)

rewards = {'trash': 1, 'homework': 2, 'project': 5, 'work': 2, 'call': 1, 'book': 2, 'doctor': 2, 'dishes': 2,
    'chores': 3, 'chore': 3,}

# Logic

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
            mood.set(mood.get() + rewards[substring])
 
def fail_task():
    task_index = task_listbox.curselection()[0]
    task_string = str(task_listbox.get(task_index)).lower()
    task_listbox.delete(task_index)

    # if any(substring.lower() in task_string.lower() for substring in rewards.keys()):
    #     mood.set(mood.get() + rewards[''])

    substrings = task_string.split()
    for substring in substrings:
        if substring in rewards.keys():
            mood.set(mood.get() - rewards[substring])

# GUI

# Mood Bar Frame

mood_frame = tkinter.Frame(root)
mood_frame.pack()

resized_image= heart_sprite.resize((25,25))
temp = ImageTk.PhotoImage(resized_image)
heart_label = tkinter.Label(mood_frame, image=temp)
heart_label.place(x = 1, y = 1)
heart_label.pack(side=tkinter.LEFT)

mood_bar = Progressbar(mood_frame, variable=mood, orient=tkinter.HORIZONTAL, length=250, mode="determinate")
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
