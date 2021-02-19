"""
This file contains code for controlling
the servo motor
"""

# Import modules
import RPi.GPIO as GPIO

# Global variables

# Constants
SERVO_PIN = 13
servo = None

# Functions
def initialize_servo():
    """
    Author:
    This function does whatever is necessary
    to initialize the servo motor
    Input: None
    Output: boolean value, True if successful
    """
    
    # Setup the GPIO library
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    # Initalize the servo
    global servo
    servo = GPIO.PWM(servoPIN, 50) # GPIO 13 for PWM with 50Hz
    servo.start(2.5) # Initialization

def clean_servo():
    global servo
    servo.stop()
    GPIO.cleanup()

def rotate(angle):
    """
    Author:
    This function rotates the servo to the desired
    angle
    Input: angle - current angle (in degrees) to
    rotate the servo to
    Output: None
    """
    pass
