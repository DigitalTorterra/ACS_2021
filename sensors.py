"""
This file contains all of the code used to read
data from sensors.

Sensors Used:
ADXL345 - Accelerometer
MPL3115A2 - Altimeter
MPU9250/6500 - IMU
"""

# Import libraries
import time
import time
import board
import busio
import adafruit_adxl34x
import adafruit_mpl3115a2
import FaBo9Axis_MPU9250

# Global variables
i2c = busio.I2c(board.SCL, board.SDA)
accelerometer = None
altimeter = None
imu = None

mpu9250 = FaBo9Axis_MPU9250.MPU9250()

# Initialization functions
def initialize_accelerometer():
    """
    Author: Nick Crnkovich
    This function initializes the accelerometer.
    Input: None
    Output: boolean, True if initialized correctly,
    false if initialized incorrectly
    """
    acclerometer = adafruit_adxl34x.ADXL345(i2c)
    return True

def initialize_altimeter():
    """
    Author:
    This function initializes the altimeter.
    Input: None
    Output: boolean, True if initialized correctly,
    false if initialized incorrectly
    """
    altimeter = adafruit_mpl3115a2.MPL3115A2(i2c)
    altimeter.sealevel_pressure = 102250
    return True

def initialize_imu():
    """
    Author:
    This function initializes the IMU.
    Input: None
    Output: boolean, True if initialized correctly,
    false if initialized incorrectly
    """
    imu = FaBo9Axis_MPU9250.MPU9250()
    return True

def initialize_sensors():
    """
    Author:
    This function initializes all the sensors
    Note: call other functions in the design
    Input: None
    Output: boolean, True if initialized correctly,
    false if initialized incorrectly
    """
    return False

# Reading Functions
def read_accelerometer():
    """
    Author:
    This function reads values from the accelerometer
    Input: None
    Output: Ordered tuple containing the x, y, and z
    acceleration
    """
    return acclerometer.acceleration

def read_altimeter():
    """
    Author:
    This function reads values from the altimeter
    Input: None
    Output: Current height of the rocket
    """
    altitude = altimeter.altitude
    return altitude

def read_imu():
    """
    Author:
    This function reads values from the IMU
    Input: None
    Output: Dict containing any relevant sensor
    output from the IMU (minimum orientation and 
    acceleration)
    """
    accel = mpu9250.readAccel()

    out = {
        "acceleration": (0,0,0),
        "orientation": (0,0,0)
    }

    return out

def read_sensors():
    """
    Author:
    This function reads relevant values from every
    sensor.
    Note: Call other functions in this file!
    Input: None
    Output: Dict containing any relevant sensor data
    """

    out = {
        "accelerometer": (0,0,0),
        "altimeter": 0,
        "imu": {
            "acceleration": (0,0,0),
            "orientation": (0,0,0)
        }
    }

    return out
