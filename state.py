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
    height, velocity, acceleration, *_ = data

def get_state_num():
    """
    Author:
    This function returns the current state
    Input: None
    Output: number of current state
    """
    return 0

def get_state_name():
    """
    Author:
    This function returns the name (in English)
    of the current state
    Input: None
    Output: string containing the current state
    """
    return "Armed"
