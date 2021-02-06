"""
This file contains all the code used to 
filter the sensor data, with whatever
libraries are required
"""

# Import libraries
import numpy as np
import matplotlib.pyplot as plt
# import openpyxl
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise


# Global variables
my_filter = None
t_prev = None


# Functions
def initialize_filter():
    """
    This function initializes the Kalman filter and
    returns the initialized filter.
    """

    global my_filter

    # Initialize object
    my_filter = KalmanFilter(dim_x=3, dim_z=3)       

    # Measurement/state conversion matrix
    my_filter.H = np.array([[1,0,0],                 
                            [0,0,1],
                            [0,0,1]])

    # Covariance matrix
    my_filter.P *= 100

    # Measurement Noise
    my_filter.R *= 5

    # Process Noise
    my_filter.Q = Q_discrete_white_noise(dim=3, dt=0.1, var=0.13)

    # Initial position
    my_filter.x = np.array([0,0,0])

    
def gen_phi(dt):
    """"
    This function generates a state transition matrix
    "phi" from a timestep.
    """
    dp = 1
    ds = 0
    di = (dt**2)/2

    phi = np.array([[dp, dt, di],
                    [ds, dp, dt],
                    [ds, ds, dp]])

    return phi

def get_dt(in_time):
    """
    Appropriately handle the creation of
    a timestep from the current and previous
    times.
    """
    global t_prev

    if t_prev == None:
        dt = 0.1
    else:
        dt = in_time - t_prev
    t_prev = in_time
    return dt

def transform_acceleration(in_accel):
    return in_accel[1]



def filter_data(sensor_data):
    """
    Author: Patrick
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

    # Load globals
    global my_filter
    global t_prev

    # Make sure filter is initialized
    if my_filter == None:
        raise Error("Filter not initialized!")

    # Read in sensor data
    alt = sensor_data.read_field('mpl_altitude')
    adxl_accel = sensor_data.read_field('adxl_acceleration')
    mpu_accel = sensor_data.read_field('mpu_acceleration')
    t = sensor_data.read_field('time')

    t = t.get_value()
    alt = alt.get_value()
    adxl_accel = adxl_accel.get_value_list()
    mpu_accel = mpu_accel.get_value_list()

    # Timestep and acceleration
    dt = get_dt(t)
    #adxl_accel = transform_acceleration(adxl_accel)
    adxl_accel = mpu_accel
    mpu_accel = transform_acceleration(mpu_accel)
    adxl_accel = mpu_accel

    # Appropriately update filter parameters
    z = np.array([alt, adxl_accel, mpu_accel])
    my_filter.F = gen_phi(dt)

    # Perform the prediction/update steps
    my_filter.predict()
    my_filter.update(z)

    # Log the output

    return my_filter.x
