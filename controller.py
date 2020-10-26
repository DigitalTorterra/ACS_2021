"""
This file contains code relating to
controlling the servo, mostly PID
or some subset of it, with gain 
scheduling or whatever fancy stuff
you guys do
"""

# Import modules

# Global Variables
initialized = False
angle = 0
angle_min = 0
angle_max = 45

# Function definitions
def initialize(data):
    """
    Author:
    This function should do whatever work
    is required to initialize the algorithm
    Input: data - output from filter, will
    be an ordered pair of data
    Output: None
    """
    height, velocity, acceleration, *_ = data

def step(data):
    """
    Author:
    This function should perform a computation
    step which takes in sensor data and updates
    the current recommended angle
    Input: data - output from filter, will
    be an ordered pair of data
    Output: None
    """
    height, velocity, acceleration, *_ = data

def get_angle():
    """
    Author:
    This function should output the current
    angle the servo should be extended to
    Input: None
    Output: current angle
    """
    return 0

def get_min():
    """
    Author:
    This function should output the minimum
    angle the servo can be rotated to
    Input: None
    Output: minimum angle
    """
    return 0

def get_max():
    """
    Author:
    This function should output the maximum
    angle the servo can be rotated to
    Input: None
    Output: maximum angle
    """
    return 0
