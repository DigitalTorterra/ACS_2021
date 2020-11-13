"""
This file writes any relevant information
to a CSV file for later usage
"""

# Import modules
import glob
import utils
import csv

# Global variables
root_dir = './data/'
file_name = 'out'
file_extension = '.csv'
file_path = ''

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
    files = glob.glob(f'{root_dir}{file_name}*{file_extension}')
    file_nums = map(utils.string_to_int, files)
    out_num = max(file_nums) + 1 

    global file_path
    file_path = f'{root_dir}{file_name}{out_num}{file_extension}'


def initialize_file():
    """
    This function creates the file and writes
    its header.
    Input: None
    Output: None
    """
    gen_filename()

    with open(file_path, 'w') as f:
        writer = csv.DictWriter(f, )


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
