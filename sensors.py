"""
This file contains all of the code used to read
data from sensors.

Sensors Used:
ADXL345 - Accelerometer
MPL3115A2 - Altimeter
MPU9250/6500 - IMU
"""

# Import libraries
import board
import busio 
import adafruit_mpl3115a2

# Global variables
i2c = busio.I2C(board.SCL, board.SDA)


# Initialization functions
def initialize_accelerometer():
    """
    Author:
    This function initializes the accelerometer.
    Input: None
    Output: boolean, True if initialized correctly,
    false if initialized incorrectly
    """
    return False

def initialize_altimeter():
    """
    Author:
    This function initializes the altimeter.
    Input: None
    Output: boolean, True if initialized correctly,
    false if initialized incorrectly
    """
    altimeter = adafruit_mpl3115a2.MPL3115A2(i2c)
    return False

def initialize_imu():
    """
    Author:
    This function initializes the IMU.
    Input: None
    Output: boolean, True if initialized correctly,
    false if initialized incorrectly
    """
    return False

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
    return (0,0,0)

def read_altimeter():
    """
    Author:
    This function reads values from the altimeter
    Input: None
    Output: Current height of the rocket
    """
    sensor.sealevel_pressure = 102250 
    pressure = sensor.pressure
    altitude = sensor.altitude
    temperature = sensor.temperature
    time.sleep(1.0)
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
