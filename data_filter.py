"""
This file contains all the code used to 
filter the sensor data, with whatever
libraries are required
"""

# Import libraries
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
from filterpy.kalman import KalmanFilter
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
    with   the ground
    """
    f = KalmanFilter (dim_x=3, dim_z=2)
    # Importing data and saving as individual vectors because.
    accelXData = sensor_data[0]
    accelYData = sensor_data[1]
    accelZData = sensor_data[2]
    altimeterData = sensor_data[3]
    imuAccelXData = sensor_data[4]
    imuAccelYData = sensor_data[5]
    imuAccelZData = sensor_data[6]
    imuMagXData = sensor_data[7]
    imuMagYData = sensor_data[8]
    imuMagZData = sensor_data[9]
    imuGryoXData = sensor_data[10]
    imuGryoYData = sensor_data[11]
    imuGryoZData = sensor_data[12]
    timeData = sensor_data[13]
    
# Initializing state vector and state transition matrix
    f.x = np.array([3.5, 0., 0.]) # location, velocity, acceleration
    f.F = np.array([1., 1. ,1.], # state transition matri
                  [0., 1., 1.],
                  [0., 0., 1.])
    f.H = np.array([1., 0., 0.])  #measurement function/unit converstion
    f.R *= R  # measurement unertainty
    f.P[:] = P #convariance matrix
    f.Q[:] = Q # process uncertainty/noise

    dt = 0.1
    x 

    return (0,0,0,0)
