"""
This file manages the current state that
the rocket is in. Talk to Patrick about
getting specific values for the transitions.
"""

# Import libraries
import data_manager
from data_manager import Data_Manager

# Global variables
state = 0

# Constants
state_values = [
    'Armed',
    'Launched',
    'Burnout',
    'Apogee',
    'Overshoot',
    'Landed'
]
LIFTOFF_ACCEL = 40
LIFTOFF_HEIGHT = 30
BURNOUT_ACCEL = -6.125
BURNOUT_HEIGHT = 300
APOGEE_VELOCITY = 0
OVERSHOOOT_HEIGHT = 1621
LANDED_ACCEL = 0
LANDED_VELOCITY = 10
LANDED_HEIGHT = 10

# Functions
def initialize_state(manager: Data_Manager):
    manager.add_data(data_manager.Scalar_Data('state'))

def get_state(state_name: str) -> int:
    return state_values.index(state_name)

def state_transition(manager: Data_Manager):
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

    global state

    # Read in data from manager
    height = manager.read_field('kalman_height').get_value()
    velocity = manager.read_field('kalman_velocity').get_value()
    acceleration = manager.read_field('kalman_acceleration').get_value()

    next_state = state

    # Armed
    if state == get_state('Armed'):
        if acceleration > LIFTOFF_ACCEL or height > LIFTOFF_HEIGHT:
            next_state = get_state('Launched')

    
    # Launched
    if state == get_state('Launched'):
        if acceleration < BURNOUT_ACCEL or height > BURNOUT_HEIGHT:
            next_state = get_state('Burnout')

    # Burnout
    if state == get_state('Burnout'):
        if velocity < APOGEE_VELOCITY:
            next_state = get_state('Apogee')
        
        elif height > OVERSHOOOT_HEIGHT:
            next_state = get_state('Overshoot')

        elif acceleration > BURNOUT_ACCEL:
            next_state = get_state('Launched')

    # Apogee
    if state == get_state('Apogee'):
        if velocity > APOGEE_VELOCITY:
            next_state = get_state('Burnout')
        
        elif acceleration < LANDED_ACCEL and velocity < LANDED_VELOCITY and height < LANDED_HEIGHT:
            next_state = get_state('Landed')

    # Overshoot
    if state == get_state('Overshoot'):
        if velocity < APOGEE_VELOCITY:
            next_state = get_state('Apogee')

    state = next_state
    state_name = get_state_name()
                
    # Record result
    manager.update_field('state', state_name)

    return state_name
            
            

def get_state_num():
    """
    Author:
    This function returns the current state
    Input: None
    Output: number of current state
    """
    return state

def get_state_name():
    """
    Author:
    This function returns the name (in English)
    of the current state
    Input: None
    Output: string containing the current state
    """
    return state_values[state]
