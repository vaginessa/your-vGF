### hw's local file

#import the packages here
import time
from random import *
import json
import os

#class for character
class Ame:

    valid_range = range(0, 100) #sets allowed value for stats

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

#init main(), put this last
if __name__ == "__main__":
    main()