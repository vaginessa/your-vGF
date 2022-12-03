### hw's local file

#import the packages here
import time
from random import *
import json
import os
import bisect

#class for character
class Ame:

    #initialise the class
    def __init__(self, name, happiness , affection):
        self._name = name
        self._happiness = happiness
        self._affection = affection

    #getter and setters for happiness and affections, trigger events for certain thresholds
    @property
    def name(self):
        return self._name

    @property
    def happiness(self):
        return self._happiness
    
    @happiness.setter
    def happiness(self, happiness):
        if happiness >= 100:
            happiness = 100
        elif happiness <= 0:
            happiness = 0
        update_sprite("happiness", self.happiness, happiness)
        self._happiness = happiness
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
        self._affection = affection
        write_save()



#create main function
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
            ame.happiness = 1000
            print(f"Name is {ame.name}, happiness is {ame.happiness}, affection is {ame.affection}")
            write_save()
    else:
        init_ame()

def check_save():
    return os.path.isfile("./save.json")

#initiate if no saved file
def init_ame():
    global ame

    name = input("Enter name : ")
    ame = Ame(name, 50, 20)
    print(f"Name is {ame.name}, happiness is {ame.happiness}, affection is {ame.affection}")
    write_save()

#write to save file
def write_save():
    data = {"name": ame.name, "happiness": ame.happiness, "affection": ame.affection}
    with open('./save.json', 'w') as outfile:
        json.dump(data, outfile)

def update_sprite(stat, old, new):
    stages = ["0", "1-25", "25-50", "50-75", "75-99", "100"] #ed to change this based on names of sprite groups, this can be a global list instead
    old_stage = bisect.bisect([1, 25, 50, 75, 100], old)
    new_stage = bisect.bisect([1, 25, 50, 75, 100], new)
    if new_stage != old_stage:
        print(f"Change stat for {stat}, new stage is {stages[new_stage]}")
        #change sprite, pass the values to the change sprite function

#init main(), put this last
if __name__ == "__main__":
    main()