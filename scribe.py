"""
This file writes any relevant information
to a CSV file for later usage
"""

# Import modules
import logging
import glob
import utils
import csv
import data_manager

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
    file_nums = list(map(utils.string_to_int, files))
    out_num = max(file_nums) + 1 if len(file_nums) > 0 else 0

    global file_path
    file_path = f'{root_dir}{file_name}{out_num}{file_extension}'


def initialize_file(manager):
    """
    This function creates the file and writes
    its header.
    Input: None
    Output: None
    """
    gen_filename()

    with open(file_path, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=manager.get_field_names())
        writer.writeheader()


def write_row(manager):
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
    with open(file_path, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(utils.format_float_list(manager.get_field_values()))


if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)

    import sensors
    sensors.initialize_sensors()
    initialize_file(sensors.manager)

    while True:
        try:
            sensors.read_sensors()
            write_row(sensors.manager)
        except Exception as e:
            logging.error(e)
