"""
This file contains all of the code used to read
data from sensors.

Sensors Used:
ADXL345 - Accelerometer
MPL3115A2 - Altimeter
MPU9250/6500 - IMU
"""

# Import libraries
import csv
import time
import logging
import data_manager
from data_manager import Data_Manager

# Parameters
ALTITUDE_STEPS = 100

# Global variables

accelerometer = None
altimeter = None
imu = None
times = None

read_row = lambda data, key: [row[key] for row in data]

# Initialization functions
def initialize_accelerometer(manager: Data_Manager, rows) -> bool:
    """
    Author: Nick Crnkovich
    This function initializes the accelerometer.
    Input: None
    Output: boolean, True if initialized correctly,
    false if initialized incorrectly
    """
    logging.info("Initializing accelerometer")
    global accelerometer
    
    manager.add_data(data_manager.Tuple_Data('adxl_acceleration'))
    
    # adxl_accelerationadxl_x = read_row(rows, 'adxl_acceleration_x')
    # adxl_accelerationadxl_y = read_row(rows, 'adxl_acceleration_y')
    # adxl_accelerationadxl_z = read_row(rows, 'adxl_acceleration_z')
    adxl_x = read_row(rows, 'ADXL X Acceleration')
    adxl_y = read_row(rows, 'ADXL Y Acceleration')
    adxl_z = read_row(rows, 'ADXL Z Acceleration')


    accelerometer = iter(zip(adxl_x, adxl_y, adxl_z))

    return True

def initialize_altimeter(manager: Data_Manager, rows) -> bool:
    """
    Author:
    This function initializes the altimeter.
    Input: None
    Output: boolean, True if initialized correctly,
    false if initialized incorrectly
    """
    logging.info("Initializing altimeter")
    global altimeter

    manager.add_data(data_manager.Scalar_Data('mpl_altitude'))

    altimeter = iter(read_row(rows, 'Altitude m'))
    
    return True

def initialize_imu(manager: Data_Manager, rows) -> bool:
    """
    Author:
    This function initializes the IMU.
    Input: None
    Output: boolean, True if initialized correctly,
    false if initialized incorrectly
    """
    logging.info("Initializing IMU")
    global imu

    manager.add_data(data_manager.Tuple_Data('mpu_acceleration'))
    manager.add_data(data_manager.Tuple_Data('mpu_gyroscope'))
    manager.add_data(data_manager.Tuple_Data('mpu_magnetometer'))

    mpu_accel_x = read_row(rows, 'mpu_acceleration_x')
    mpu_accel_y = read_row(rows, 'mpu_acceleration_y')
    mpu_accel_z = read_row(rows, 'mpu_acceleration_z')
    mpu_gyro_x = read_row(rows, 'mpu_gyroscope_x')
    mpu_gyro_y = read_row(rows, 'mpu_gyroscope_y')
    mpu_gyro_z = read_row(rows, 'mpu_gyroscope_z')
    mpu_mag_x = read_row(rows, 'mpu_magnetometer_x')
    mpu_mag_y = read_row(rows, 'mpu_magnetometer_y')
    mpu_mag_z = read_row(rows, 'mpu_magnetometer_z')

    imu = iter(zip(mpu_accel_x, mpu_accel_y, mpu_accel_z,
                   mpu_gyro_x, mpu_gyro_y, mpu_gyro_z,
                   mpu_mag_x, mpu_mag_y, mpu_mag_z))

    return True

def initialize_timer(manager: Data_Manager, rows) -> bool:
    """
    Initializes time data
    """
    logging.info("Initializing timer...")
    manager.add_data(data_manager.Scalar_Data('time'))

    global times
    times = iter(read_row(rows, 'Time ms'))

    return True

def initialize_sensors(path: str, manager: Data_Manager) -> bool:
    """
    This function initializes all the sensors
    Note: call other functions in the design
    """
    logging.info("Initializing sensors...")

    # Read in data
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]

    # Initialize active sensors
    result = initialize_timer(manager, rows)
    for sensor in manager.active_sensors:
        if sensor == 'IMU':
            result = result and initialize_imu(manager, rows)
        elif sensor == 'Accelerometer':
            result = result and initialize_accelerometer(manager, rows)
        elif sensor == 'Altimeter':
            result = result and initialize_altimeter(manager, rows)

    return result


# Reading Functions
def read_accelerometer(manager: Data_Manager):
    """
    Author:
    This function reads values from the accelerometer
    Input: None
    Output: Ordered tuple containing the x, y, and z
    acceleration
    """
    try:
        acceleration = next(accelerometer)
    except:
        acceleration = [0,0,0]
    manager.update_field('adxl_acceleration', acceleration)

def read_altimeter(manager: Data_Manager):
    """
    Author:
    This function reads values from the altimeter
    Input: None
    Output: Current height of the rocket
    """
    try:
        altitude = next(altimeter)
    except:
        altitude = 0
    manager.update_field('mpl_altitude', altitude)

def read_imu(manager: Data_Manager):
    """
    Author:
    This function reads values from the IMU
    Input: None
    Output: Dict containing any relevant sensor
    output from the IMU (minimum orientation and 
    acceleration)
    """
    data = next(imu)
    accel = data[:3]
    magnet_val = data[3:6]
    gyro_val = data[6:]

    manager.update_dict_field('mpu_acceleration', accel)
    manager.update_dict_field('mpu_magnetometer', magnet_val)
    manager.update_dict_field('mpu_gyroscope', gyro_val)

def read_time(manager: Data_Manager):
    """
    Returns the current time
    """
    current_time = next(times)
    manager.update_field('time', current_time)


def read_sensors(manager: Data_Manager):
    """
    Author:
    This function reads relevant values from every
    sensor.
    """

    read_time(manager)
    for sensor in manager.active_sensors:
        if sensor == 'IMU':
            read_imu(manager)
        elif sensor == 'Accelerometer':
            read_accelerometer(manager)
        elif sensor == 'Altimeter':
            read_altimeter(manager)
