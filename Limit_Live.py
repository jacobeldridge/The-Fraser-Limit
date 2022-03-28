from cProfile import label
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

#This input class is for grouping the different input requirements, processes, and variables. 
class Input:
    #possible inputs for preset requirement
    presets = [
        "alternate",
        "concave_up",
        "concave_down"
    ]
    #Specefic errors for each requirement
    errors = [
        "This input cannot be left blank", 
        "This input must be a whole number", 
        "This input must be a real number", 
        "Please type 'y' or 'n'",
        "Please enter a valid preset",
        "|B| must be greater than 1"
        ]
    def __init__(self,text,on_enter,**paramaters):
    #On enter is an unused paramater which was going to be used to execute a function on input completion
    #The paramater was never used but its use case seemed valuable so I left it in.

        #Equating inputed strings to predefined functions
        paramater_dict = {
            "filled": self.must_be_filled,
            "int": self.must_be_int,
            "float": self.must_be_float,
            "y_n": self.must_be_y_n,
            "preset": self.preset,
            "greater_1": self.greater_1
        }
        #text that prompts the input
        self.text = text
        #Empty list to store requirement functions
        self.input_requirements = []
        #This loop iterates over every parameter argument and adds them to an empty list
        for paramater in paramaters.values():
            new_requirement = paramater_dict[paramater]
            self.input_requirements.append(new_requirement)
    #========================================================================================================================

    #These are all the different input requirement functions. This process could be done more generally and efficiently with a singular function,
    #but for the sake of expansion, organization, and simplicity, I made a function for each argument.
    #
    #If input string (which has already passed the float requirement) > 1: True
    def greater_1(self):
        if abs(float(self.user_input)) > 1:
            return True
        else:
            print(self.errors[5])
            return False
    #========================================================================================================================

    #Requires any input. This helps to give more specific errors.
    def must_be_filled(self):
        if (self.user_input == "") or (self.user_input == " "):
            print(self.errors[0])
            return False
        else:
            return True
    #========================================================================================================================

    #If input string is in preset list: True
    def preset(self):
        if self.user_input in self.presets:
            return True
        print(self.errors[4])
        return False
    #========================================================================================================================

    #If integer: True
    def must_be_int(self):
        try:
            int(self.user_input)
        except:
            print(self.errors[1])
            return False
        return True
    #========================================================================================================================

    #If float: True
    def must_be_float(self):
        try:
            float(self.user_input)
        except:
            print(self.errors[2])
            return False
        return True
    #========================================================================================================================

    #If 'y' or 'n': True
    def must_be_y_n(self):
        if (self.user_input == "y") or (self.user_input == "n"):
            return True
        else:
            print(self.errors[3])
            return False
    #========================================================================================================================

    #If any boolean in self.input_requirements is False: False
    def check(self):
        for requirement in self.input_requirements:
            if not requirement():
                return False
        return True
    #========================================================================================================================

    #This function creates a new input until the user input has no errors
    def call_input(self):
        while True:
            self.user_input = input(self.text)
            if self.check():
                break
            else:
                continue
        return self.user_input
    #========================================================================================================================
#========================================================================================================================

#This class groups together the different functions and variables required to generate the live graph 
class Graph():
    def __init__(self,proximity, delay, preset=None):
        #These are the default coordinate lists for each object
        self.x_list, self.y_list = [],[]
        #If there is a preset function passed, execute it
        if preset != None:
            preset = eval("self."+preset+"()")
        #This determines the initial y coordinate where x=a for f(x) and 'a' is a global constant
        self.y = f(a)
        #This equation determines the point of convergence for f(x)
        self.convergance = (c*b)/(b-1)
        #Passing paramaters to object instances
        self.delay = delay
        self.proximity = proximity
        #The graph will not work with no display time so zero is allowed to be passed as user input but is altered in execution
        if self.delay <= 0:   
            self.delay = .0001
        #This converts the paramater 'proximity' to an allowed range of error for f(x) which is used in the function to determine the number iterations for the program
        self.epsilon = 10**-proximity
        #Determines the number iterations for the program
        self.iterations = self.det_epoch()
        #Activates Matplotlib's interactive mode
        plt.ion()
        #Creates graph figure
        self.fig = plt.figure()
        #Defines graph positioning in the figure
        ax = self.fig.add_subplot(111)
        #Defines the figures color
        ax.set_facecolor('black')
        #Defines the properties of the line with no plot points
        self.line1, = ax.plot(self.x_list, self.y_list,color='white', linestyle='dashed', linewidth = 1,
        marker='o', markerfacecolor='white', markersize=9,label="F(x)")
        #Draws the point of convergence
        ax.axhline(self.convergance, c='red', ls='--', label="(c*b)\(b-1)")
        #Creates a legend for all lines on the axes
        leg = ax.legend()
        #Defines the bounds of the x-axis
        ax.set_xlim(0,self.iterations)
        #The conditions below are used to adjust the view of the graph based upon the position of the value of the first iteration
        #
        #If the first iteration is below the convergance the y-axis bounds are defined thusly
        if self.convergance > self.y:
            #The lower bound of the y-axis is the value of the first iteration
            #The upper bound is the convergance + the distance between the first iteration and the convergance
            ax.set_ylim(self.y,self.convergance+(self.convergance-self.y))
        #If the convergance = f(a) something broke. I left this in from past troubleshooting for any future editors
        elif self.convergance == self.y:
            print("Something is very broken...The point of convergence == f(a)")
            time.sleep(5)
            quit()
        #If the first iteration is above the convergance the y-axis bounds are defined thusly
        else:
            #The values of the bounds are equivalent but flipped
            ax.set_ylim(self.convergance+(self.convergance-self.y),self.y)
    #========================================================================================================================
    
    #This function contains the main loop for the live graph, and data generation
    def draw(self):
        #Draw datapoints
        self.fig.canvas.draw()
        #As long as the iteration counter does not equal the predetermined number of iterations the loop will continue
        for cur_iteration in range(self.iterations+1):
            #Adds iteration counter to x coordinate list
            self.x_list.append(cur_iteration)
            #Adds iteration value to y coordinate list
            self.y_list.append(self.y)
            #Display various informative values in the python terminal
            display(value=self.y, graph_convergance=self.convergance, progress=round((cur_iteration/self.iterations)*100), error=self.proximity, iteration=cur_iteration)
            #Run a new iteration of the function and redefine the variable that stores it
            self.y = f(self.y)
            #Pass the edited coordinate lists to the line object
            self.line1.set_data(self.x_list,self.y_list)
            #If there is no delay the graph will update too fast and it will not be visible
            time.sleep(self.delay)
            #Pushes the figure to window
            self.fig.canvas.flush_events()
        #User instruction
        print("\nClose graph to continue...")
        #Makes sure the window does not close until the user closes it
        plt.waitforbuttonpress()   
        #Returns coordinate lists for an optional spreadsheet
        return self.x_list, self.y_list 
    #========================================================================================================================

    #This is a function derived by Mr. Fraser to determine how many iterations are required to have a value within an error bound of epsilon
    def det_epoch(self):
        epoch_float = np.log(abs((a*b/self.epsilon)-(b**2*c/(self.epsilon*(b-1)))))/np.log(abs(b))
        epoch = int(np.ceil(epoch_float))
        return epoch
    #========================================================================================================================
    #This function sets the constants a,b, and c to values that will alternate in the function
    def alternate(self):
        global a,b,c
        a = 6
        b = -1.5
        c = 3
    #========================================================================================================================
    #This function sets the constants a,b, and c to values that will approach the point of convergence from below
    def concave_down(self):
        global a,b,c
        a = 6
        b = 1.5
        c = 3
    #========================================================================================================================
    #This function sets the constants a,b, and c to values that will approach the point of convergence from above
    def concave_up(self):
        global a,b,c
        a = 95
        b = 3
        c = -279
    #========================================================================================================================
#========================================================================================================================


#==========================================================================
#   ______                _   _                 
#  |  ____|              | | (_)                
#  | |__ _   _ _ __   ___| |_ _  ___  _ __  ___ 
#  |  __| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
#  | |  | |_| | | | | (__| |_| | (_) | | | \__ \
#  |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
#===========================================================================
#This function generates a random value for B with its special parameters
def generateB():
    #|B| can be any number greater than 1, but to make the graphs have reasonable bounds B is chosen between -10 and 10
    b_temp = random.randint(-10,10)
    #In the event the random number does not fit the requirements, another random value is generated until it does
    while abs(b_temp) <= 1:
        b_temp = random.randint(-10,10)
    return b_temp
#-------------------------------------------------------------

#Creates randomly generated inputs, formats inputed ones, or passes preset values
def new_session():
    global a,b,c
    randorgen = input("Would you like to directly input, have them randomly generated, or select a preset? ('input','gen', or 'preset'): ")
    new_screen()
    if randorgen == "gen":
        #Smaller bounds were selected to retain a good view of the process in the animation 
        a = random.randint(-1000,1000)
        b = generateB()
        c = random.randint(-1000,1000)
        #Function that calls for more user inputs
        prep()
    
    elif randorgen == "input":
        a_input = Input(text="Value for A: ",on_enter=None, parameter1='filled',paramater2='float')
        b_input = Input(text="Value for B: ",on_enter=None, parameter1='filled',paramater2='float',paramater3='greater_1')
        c_input = Input(text="Value for C: ",on_enter=None, parameter1='filled',paramater2='float')
        #Seperating each input call with a blank screen helps keep the terminal based UI clean
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
        #No other user inputs are required with presets so the program skips prep() and goes straight to the main process
        main_process(preset=preset_str)
        

    else:
        print("Error, invalid input.")
        new_session()  
        
#-----------------------------------------------------------------    
   
#This function saves the coordinate lists to columns on excel spreadsheet
def save_to_spread(*args):
    #Zipping files to input as columns rather than rows
    data = list(zip(*args))
    #The spreadsheets are named with date/time to ensure each name is different
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
#This function clears the screen
def new_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
#-----------------------------------------------------------------------------
#Terminal animation function to display updating data
def display(value, graph_convergance,progress, error, iteration):
    #The value is only rounded to the decimal place of the predefined error bound
    value = str(round(value,error))
    progress = str(progress)
    #This is the process for writing and rewriting data to the terminal screen
    sys.stdout.write("\033[A\033[A\033[A\rF(x) = {} \nCONVERGENCE = {} \nITERATION = {} \nPROGRESS = [{}%] ".format(value,graph_convergance,iteration,progress))
#-----------------------------------------------------------------------------

#Defines basic variables for the function and lots of stuff
def main_process(error_allowed=None,pause=None,preset=None):
    new_screen()
    #Checks for preset paramater
    if preset != None:
        graph = Graph(3, .5, preset)
        graph_drawn = graph.draw()
    else:
        graph = Graph(proximity=error_allowed, delay=pause)
        graph_drawn = graph.draw()
    new_screen()
    #Checks if user wants to save coordinate lists to spreadsheet
    save_input = Input(text="Would you like to save data to a spreadsheet? ('y' or 'n'): ",on_enter=None,paramater1="y_n")
    save = save_input.call_input()
    if save=="y":
        save_to_spread(graph_drawn[0], graph_drawn[1])
    new_screen()
    #Checks if user wants to run the program again
    again_input = Input(text="Would you like to run another simulation? ('y' or 'n'): ",on_enter=None,paramater1="y_n")
    again = again_input.call_input()
    if again=="y":
        boot_up()
    else:
        print("Process Completed")

#-----------------------------------------------------------------------------
def prep():
    #Input for Epsilon
    error_range_input = Input(text="Allowed range of error (10^-{your_input}): ",on_enter=None,parameter1='filled',paramater2='int')
    #Input for delay between iteration
    time_delay_input = Input(text="Delay between iterations (seconds): ",on_enter=None,parameter1='filled',paramater2='float')
    new_screen()
    error_range = int(error_range_input.call_input())
    new_screen()
    time_delay = float(time_delay_input.call_input())
    new_screen()
    #Overview of values to be used in the program
    print("VALUES FOR SIMULATION")
    print(">>>A: {}\n>>>B: {}\n>>>C: {}\n>>>Error Range: 10^-{}\n>>>Time Delay: {}".format(a,b,c,error_range,time_delay))
    #Checks to see if user approves of displayed data
    check = Input(text="Run Simulation? (y/n): ", on_enter=None, paramater1='y_n')
    if check.call_input()=='y':
        new_screen()
        main_process(error_range,time_delay)
    #If the user changes their mind on the displayed values they can go back and choose again
    else:
        new_screen()
        print(">>>Simulation has been aborted.")
        new_session()
#Startup function    
def boot_up():
    new_screen()
    new_session()
    new_screen()
    
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
    boot_up()   
    



# where it all started
# init: x = a/b + c
# per iteration: x/b + c
# convergance: cb/b-1
