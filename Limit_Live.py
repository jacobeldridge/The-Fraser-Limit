import random
import os
from fractions import Fraction
import time
from unicodedata import decimal
import numpy as np
import matplotlib.pyplot as plt
import csv
from time import gmtime, strftime
import sys

#======================================================================
#    ____  _     _           _       
#   / __ \| |   (_)         | |      
#  | |  | | |__  _  ___  ___| |_ ___ 
#  | |  | | '_ \| |/ _ \/ __| __/ __|
#  | |__| | |_) | |  __/ (__| |_\__ \
#   \____/|_.__/| |\___|\___|\__|___/
#              _/ |                  
#             |__/                   
#=======================================================================

class Input:
    def __init__(self,text,on_enter,**paramaters):

        self.text = text
        self.presets = [
            "oscilate",
            "concave_up",
            "concave_down"
        ]
        self.errors = [
            "This input cannot be left blank", 
            "This input must be a whole number", 
            "This input must be a real number", 
            "Please type 'y' or 'n'",
            "Please enter a valid preset",
            "|B| must be greater than 1"
            ]

        self.input_requirements = []

        paramater_dict = {
            "filled": self.must_be_filled,
            "int": self.must_be_int,
            "float": self.must_be_float,
            "y_n": self.must_be_y_n,
            "preset": self.preset,
            "greater_0": self.greater_0
        }

        for paramater in paramaters.values():
            #paramater should be a string
            new_requirement = paramater_dict[paramater]
            self.input_requirements.append(new_requirement)
    def greater_0(self):
        if abs(float(self.user_input)) > 1:
            return True
        else:
            print(self.errors[5])
            return False
    def must_be_filled(self):
        if (self.user_input == "") or (self.user_input == " "):
            print(self.errors[0])
            return False
        else:
            return True
    def preset(self):
        if self.user_input in self.presets:
            return True
        print(self.errors[4])
        return False
    def must_be_int(self):
        try:
            int(self.user_input)
        except:
            print(self.errors[1])
            return False
        return True

    def must_be_float(self):
        try:
            float(self.user_input)
        except:
            print(self.errors[2])
            return False
        return True

    def must_be_y_n(self):
        if (self.user_input == "y") or (self.user_input == "n"):
            return True
        else:
            print(self.errors[3])
            return False

    def check(self):
        for requirement in self.input_requirements:
            if not requirement():
                return False
        return True
            
    def call_input(self):
        while True:
            self.user_input = input(self.text)
            if self.check():
                break
            else:
                continue
        return self.user_input
        
class Graph():
    def __init__(self,proximity, delay, preset=None):
        if preset != None:
            preset = eval("self."+preset+"()")
        self.delay = delay
        if self.delay <= 0:   
            self.delay = .5 
        self.proximity = proximity
        self.epsilon = 10**-proximity

        self.x_list, self.y_list = [],[]
        self.y = (a/b) + c
        self.limit = (c*b)/(b-1)
        self.iterations = self.det_epoch()

        plt.ion()
        self.fig = plt.figure()

        ax = self.fig.add_subplot(111)
        ax.set_facecolor('black')

        self.line1, = ax.plot(self.x_list, self.y_list,color='white', linestyle='dashed', linewidth = 1,
        marker='o', markerfacecolor='white', markersize=9)

        ax.axhline(self.limit, c='red', ls='--')
        ax.set_xlim(0,self.iterations)

        if self.limit > self.y:
            ax.set_ylim(self.y,self.limit+(self.limit-self.y))
        elif self.limit == self.y:
            print("AAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHH")
        else:
            ax.set_ylim(self.limit+(self.limit-self.y),self.y)

    def draw(self):
        self.fig.canvas.draw()
        for cur_iteration in range(self.iterations+1):
            self.x_list.append(cur_iteration)
            self.y_list.append(self.y)
            display(value=self.y, graph_limit=self.limit, progress=round((cur_iteration/self.iterations)*100), error=self.proximity, iteration=cur_iteration)
            self.y = f(self.y)
            self.line1.set_data(self.x_list,self.y_list)
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            plt.pause(self.delay)
        print("\nClose graph to continue...")
        plt.waitforbuttonpress()   
        return self.x_list, self.y_list 

    def det_epoch(self):
        epoch_float = np.log(abs((a*b/self.epsilon)-(b**2*c/(self.epsilon*(b-1)))))/np.log(abs(b))
        epoch = int(np.ceil(epoch_float))
        # print("THIS IS THE EPOCH")
        # print(epoch_foat)
        # print(epoch)
        return epoch
    def oscilate(self):
        global a,b,c
        a = 6
        b = -1.5
        c = 3
    def concave_down(self):
        global a,b,c
        a = 6
        b = 1.5
        c = 3
    def concave_up(self):
        global a,b,c
        a = 95
        b = 3
        c = -279

#==========================================================================
#   ______                _   _                 
#  |  ____|              | | (_)                
#  | |__ _   _ _ __   ___| |_ _  ___  _ __  ___ 
#  |  __| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
#  | |  | |_| | | | | (__| |_| | (_) | | | \__ \
#  |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
#===========================================================================
#B has special parameters so when it is generated there are extra conditions
def generateB():
    b_temp = random.randint(-10,10)
    while b_temp <= 1:
        b_temp = random.randint(-10,10)
    return b_temp
#-------------------------------------------------------------

#Creates randomly generated inputs or formats inputed ones
def new_session():
    global a,b,c
    randorgen = input("Would you like to directly input, have them randomly generated, or select a preset? ('input','gen', or 'preset'): ")
    new_screen()
    if randorgen == "gen":
        a = random.randint(-1000,1000)
        b = generateB()
        c = random.randint(-1000,1000)
        prep()
    
    elif randorgen == "input":
        a_input = Input(text="Value for A: ",on_enter=None, parameter1='filled',paramater2='float')
        b_input = Input(text="Value for B: ",on_enter=None, parameter1='filled',paramater2='float',paramater3='greater_0')
        c_input = Input(text="Value for C: ",on_enter=None, parameter1='filled',paramater2='float')
        new_screen()
        a = float(a_input.call_input())
        new_screen()
        b = float(b_input.call_input())
        new_screen()
        c = float(c_input.call_input())
        new_screen()
        prep()
    elif randorgen == "preset":
        preset_input = Input(text="", on_enter=None, paramater1='filled', paramater2='preset')
        preset_input.text = f"Please choose one of the presets by entering its name: {preset_input.presets} "
        preset_str = preset_input.call_input()
        main_process(preset=preset_str)
        

    else:
        print("Error, invalid input.")
        new_session()  
        
#-----------------------------------------------------------------    
   
#Saves lists to columns on excel spreadsheet
def save_to_spread(*args):
    #Zipping files to input as columns rather than rows

    data = list(zip(*args))

    with open('{}.csv'.format(strftime("%Y-%m-%d---%H-%M-%S", gmtime())), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)
#----------------------------------------------------------------------------            

#This is the main function that generates the data for the graphs and other statistics
def f(x):
    y = (x/b)+c
    return y
#-----------------------------------------------------------------------------
#Terminal animation
def new_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
#-----------------------------------------------------------------------------
#Terminal animation
def display(value, graph_limit,progress, error, iteration):
    value = str(round(value,error))
    progress = str(progress)
    sys.stdout.write("\033[A\033[A\033[A\rF(x) = {} \nLIMIT = {} \nITERATION = {} \nPROGRESS = [{}%] ".format(value,graph_limit,iteration,progress))
    sys.stdout.flush()
#-----------------------------------------------------------------------------

#Defines basic variables for the function and lots of stuff
def main_process(error_allowed=None,pause=None,preset=None):
    # limit = (c*b)/(b-1)
    # print(">>>A = {}\nB = {}\nC = {}\n".format(a,b,c))
    # print(">>>x = (A/B) + C\nF(x)=(x/B)+C")
    # print(">>>Projected Limit: (CB)/(B-1) or {} or {}".format((c*b)/(b-1),limit))
    new_screen()
    if preset != None:
        graph = Graph(3, .5, preset)
        graph_drawn = graph.draw()
    else:
        graph = Graph(proximity=error_allowed, delay=pause)
        graph_drawn = graph.draw()
    new_screen()
    save_input = Input(text="Would you like to save data to a spreadsheet? ('y' or 'n'): ",on_enter=None,paramater1="y_n")
    save = save_input.call_input()
    if save=="y":
        save_to_spread(graph_drawn[0], graph_drawn[1])
    new_screen()
    again_input = Input(text="Would you like to run another simulation? ('y' or 'n'): ",on_enter=None,paramater1="y_n")
    again = again_input.call_input()
    if again=="y":
        run_simulation()
    else:
        print("Goodnight")

#-----------------------------------------------------------------------------
def prep():
    error_range_input = Input(text="Allowed range of error (10^-{your_input}): ",on_enter=None,parameter1='filled',paramater2='int')
    time_delay_input = Input(text="Delay between iterations (seconds): ",on_enter=None,parameter1='filled',paramater2='float')
    new_screen()
    error_range = int(error_range_input.call_input())
    new_screen()
    time_delay = float(time_delay_input.call_input())
    new_screen()
    print("VALUES FOR SIMULATION")
    print(">>>A: {}\n>>>B: {}\n>>>C: {}\n>>>Error Range: 10^-{}\n>>>Time Delay: {}".format(a,b,c,error_range,time_delay))
    check = Input(text="Run Simulation? (y/n): ", on_enter=None, paramater1='y_n')
    if check.call_input()=='y':
        new_screen()
        main_process(error_range,time_delay)
    else:
        print(">>>Simulation has been aborted.")
#Startup function    
def run_simulation():
    new_screen()
    new_session()
    new_screen()
    #user inputs
    
    

    #display values

# =========================================================================
#   __  __       _         _____                                     
#  |  \/  |     (_)       |  __ \                                    
#  | \  / | __ _ _ _ __   | |__) | __ ___   __ _ _ __ __ _ _ __ ___  
#  | |\/| |/ _` | | '_ \  |  ___/ '__/ _ \ / _` | '__/ _` | '_ ` _ \ 
#  | |  | | (_| | | | | | | |   | | | (_) | (_| | | | (_| | | | | | |
#  |_|  |_|\__,_|_|_| |_| |_|   |_|  \___/ \__, |_|  \__,_|_| |_| |_|
#                                           __/ |                    
#                                          |___/   
# ===========================================================================                  
if __name__ == "__main__":
    run_simulation()   
    



# where it all started
# init: x = a/b + c
# per iteration: x/b + c
# limit: cb/b-1
