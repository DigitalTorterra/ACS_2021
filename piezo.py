# Import libraries
from gpiozero import TonalBuzzer, Buzzer
import data_manager
from data_manager import Data_Manager

# Constants
buzzerPIN = 21
buzzer = None
prev_state = None

def initialize_buzzer():
    global buzzer
    buzzer = TonalBuzzer(buzzerPIN)

def clean_buzzer():
    global buzzer
    buzzer.stop()

def update_buzzer(manager: Data_Manager):
    global buzzer
    global prev_state

    state = manager.read_field('state').get_value()

    if state != prev_state:
        next_state = state
        prev_state = state
    else:
        next_state = None

    if next_state == 'Armed':
        buzzer.play(440)
    elif next_state == 'Launched' or next_state == 'Apogee':
        buzzer.play(300)
    elif next_state == 'Burnout' or next_state == 'Overshoot': 
        buzzer.play(600)

    elif next_state == 'Landed':
        buzzer.play(800)

    elif next_state != None:
        buzzer.stop()

