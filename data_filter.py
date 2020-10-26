"""
This file contains all the code used to 
filter the sensor data, with whatever
libraries are required
"""

# Import libraries

# Global variables

# Functions
def filter_data(sensor_data):
    """
    Author:
    This is the main function, which
    filters incoming sensor data
    Input: sensor_data - a dict of data with these fields:
        - accelerometer: ordered tuple
          containing the x, y, and z
          accelerations
        - altimeter: the current height
          of the rocket
        - imu: a dict containing data from the IMU
            - acceleration: ordered tuple containing
              x, y, and z accelerations
            - orientation: ordered tuple containing
              the roll, pitch, and yaw of the rocket
    Output: ordered tuple containing the estimated
    height, (vertical) velocity, acceleration, and angle
    with the ground
    """
    return (0,0,0,0)
