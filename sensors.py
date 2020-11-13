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
import board
import busio
import adafruit_adxl34x
import adafruit_mpl3115a2
import FaBo9Axis_MPU9250
import logging
import data_manager

# Parameters
ALTITUDE_STEPS = 100

# Global variables
i2c = busio.I2C(board.SCL, board.SDA)
manager = data_manager.Data_Manager()

accelerometer = None
altimeter = None
imu = None



# Initialization functions
def initialize_accelerometer():
    """
    Author: Nick Crnkovich
    This function initializes the accelerometer.
    Input: None
    Output: boolean, True if initialized correctly,
    false if initialized incorrectly
    """
    logging.info("Initializing accelerometer")
    global accelerometer
    
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    accelerometer.range = adafruit_adxl34x.Range.RANGE_16_G
    accelerometer.data_rate = adafruit_adxl34x.DataRate.RATE_100_HZ

    manager.add_data(data_manager.Tuple_Data('adxl_acceleration'))

    return True

def initialize_altimeter():
    """
    Author:
    This function initializes the altimeter.
    Input: None
    Output: boolean, True if initialized correctly,
    false if initialized incorrectly
    """
    logging.info("Initializing altimeter")
    global altimeter

    altimeter = adafruit_mpl3115a2.MPL3115A2(i2c)
    altimeter._ctrl_reg1 = adafruit_mpl3115a2._MPL3115A2_CTRL_REG1_OS1 | adafruit_mpl3115a2._MPL3115A2_CTRL_REG1_ALT

    pressure_sum = 0
    for i in range(ALTITUDE_STEPS):
        pressure_sum += altimeter.pressure
    altimeter.sealevel_pressure = int(pressure_sum / ALTITUDE_STEPS)

    manager.add_data(data_manager.Scalar_Data('mpl_altitude'))
    
    return True

def initialize_imu():
    """
    Author:
    This function initializes the IMU.
    Input: None
    Output: boolean, True if initialized correctly,
    false if initialized incorrectly
    """
    logging.info("Initializing IMU")
    global imu

    imu = FaBo9Axis_MPU9250.MPU9250()
    imu.configMPU9250(FaBo9Axis_MPU9250.GFS_2000, FaBo9Axis_MPU9250.AFS_16G)

    manager.add_data(data_manager.Tuple_Data('mpu_acceleration'))
    manager.add_data(data_manager.Tuple_Data('mpu_gyroscope'))
    manager.add_data(data_manager.Tuple_Data('mpu_magnetometer'))

    return True

def initialize_timer():
    """
    Initializes time data
    """
    logging.info("Initializing timer...")
    manager.add_data(data_manager.Scalar_Data('time'))

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
    logging.info("Initializing sensors...")
    return initialize_timer() and initialize_accelerometer() and initialize_altimeter() and initialize_imu()


# Reading Functions
def read_accelerometer():
    """
    Author:
    This function reads values from the accelerometer
    Input: None
    Output: Ordered tuple containing the x, y, and z
    acceleration
    """
    acceleration = accelerometer.acceleration
    manager.update_field('adxl_acceleration', acceleration)
    return acceleration

def read_altimeter():
    """
    Author:
    This function reads values from the altimeter
    Input: None
    Output: Current height of the rocket
    """
    altitude = altimeter.altitude
    manager.update_field('mpl_altitude', altitude)
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
    accel = imu.readAccel()
    magnet_val = imu.readGyro()
    gyro_val = imu.readMagnet()

    manager.update_dict_field('mpu_acceleration', accel)
    manager.update_dict_field('mpu_magnetometer', magnet_val)
    manager.update_dict_field('mpu_gyroscope', gyro_val)

    out = {
        "acceleration": accel,
        "magnetometer": magnet_val,
        "gyroscope": gyro_val
    }

    return out

def read_time():
    """
    Returns the current time
    """
    current_time = time.time()
    manager.update_field('time', current_time)

    return current_time


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
        "accelerometer": read_accelerometer(),
        "altimeter": read_altimeter(),
        "imu": read_imu(),
        "time": read_time()
    }


    return out


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    initialize_sensors()
    out = read_sensors()
    print(out)
