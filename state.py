"""
This file manages the current state that
the rocket is in. Talk to Patrick about
getting specific values for the transitions.
"""

# Import libraries

# Global variables
state = 0
state_values = [
    'Armed',
    'Launched',
    'Burnout',
    'Apogee',
    'Overshoot',
    'Landed'
]

# Functions
def state_transition(data):
    """
    Author:
    This function reads in data from the 
    Kalman filter and transitions to a
    different state depending on the current
    state and the position/velocity/speed
    of the rocket
    Input: data - ordered pair containing
    vertical position, velocity, and acceleration
    Output: None
    """
    #want: current state num, current state str,
    #nextstate = le_current_state
    # want: series of if statements for each state_values
    height, velocity, acceleration, *_ = data

    if RNstate == 0: # state_values is armed
        rock.LED.on()
        if acceleration > liftoff acceleration or height > liftoff height:
            new_state = 1

    if RNstate == 1 # state_values is launched
        if acceleration < liftoff acceleration or height > burnout height:
            new_state = 1
            
    if RNstate == 2 # state_values is burnout
        if acceleration > burnout acceleration:
            new_state = 1 #launch sate_values bc accel noise
        if velocity < 0:
            new_state = 3 #state_values is apogee
            # apogee = best scrabble word ever
        if height > apogee and velocity > 0:
            new_state = 4 #state_values is overshot

        if RNstate == 3: # state_values is apogee :))
            rock.LED.on()
            if velocity > 0:
                new_state = 2
            if velocity <= 10 and height <=10 and acceleration <=0:
                new_state = 5 #state_values is landed

        if RNstate == 4: #state_values is overshoot
            if velocity <= 0:
                new_state = 3 #state_values is apogee

        RNstate = new_state
        rock.LED.off()
                
            
            

def get_state_num():
    """
    Author:
    This function returns the current state
    Input: None
    Output: number of current state
    """
    return state
    #return 0

def get_state_name():
    """
    Author:
    This function returns the name (in English)
    of the current state
    Input: None
    Output: string containing the current state
    """
    return state_values[state]
