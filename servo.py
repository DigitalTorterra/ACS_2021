"""
This file contains code for controlling
the servo motor
"""

# Import modules
from gpiozero import Servo
from controller import angle_max

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
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(SERVO_PIN, GPIO.OUT)

    # # Initalize the servo
    # global servo
    # servo = GPIO.PWM(SERVO_PIN, 50) # GPIO 13 for PWM with 50Hz
    # servo.start(2.5) # Initialization
    
    # Setup range
    myCorrection = 0
    maxPW = (2.0+myCorrection)/1000
    minPW = (1.0-myCorrection)/1000

    # Initialize servo
    global servo
    servo = Servo(SERVO_PIN, min_pulse_width=minPW, max_pulse_width=maxPW)

def clean_servo():
    global servo
    servo.detach()

def rotate(angle):
    """
    Author:
    This function rotates the servo to the desired
    angle
    Input: angle - current angle (in degrees) to
    rotate the servo to
    Output: None
    """

    # Calculate extension
    extension = 2*(angle/angle_max) - 1

    # Set servo
    global servo
    servo.value = extension

