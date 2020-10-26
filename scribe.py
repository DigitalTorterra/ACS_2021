"""
This file writes any relevant information
to a CSV file for later usage
"""

# Import modules

# Global variables
filename = './data/out.csv'

# Functions
def gen_filename():
    """
    This function sets the filename
    to a unique value that does not
    exist in the current directory.
    Either use a timestamp, numbering,
    random number, etc.
    Input: None
    Output: None
    """
    pass

def initialize_file():
    """
    This function creates the file and writes
    its header.
    Input: None
    Output: None
    """
    pass

def write_row(data, filtered_data, angle, state):
    """
    This function writes the current state
    (raw data, filtered data, servo angle and state)
    to the file
    Input: data - dict containing data
           filtered_data: filtered output from data filter
           angle: extension of the servo
           state: state of the system
    Output: None
    """
    pass
