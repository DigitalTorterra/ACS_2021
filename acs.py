"""
This file contains the main function, which will
continually read data from sensors, filter it,
update the flight state, move the servo, and 
write output.
"""


# Import modules
import sensors
import data_filter
import state
import controller
import servo
import scribe

# Initialize modules
sensors.initialize_sensors()
servo_angle = 0
extension = 0

def main():
    # Main loop
    while True:
        # Attempt to execute
        try:
            # Read data
            sensors.read_sensors()

            # Filter data
            data_filter.filter_data(sensors.manager)

            # Update flight state
            state.state_transition(filtered_data)
            curr_state = state.get_state_name()

            # PID
            if curr_state == 'Burnout':
                if not controller.initialized:
                    controller.initialize(filtered_data)

                extension = controller.step(filtered_data, extension)
                servo_angle = controller.get_angle(extension)

            elif curr_state == 'Overshoot':
                servo_angle = controller.get_max()
            else:
                servo_angle = 0

            # Servo
            servo.rotate(angle)

            # Output to file
            scribe.write_row(data, filtered_data, servo_angle,
                    curr_state)

        # Handle error
        except:
            print('We regret to inform you that your code has a tumor')

# Python stuff to make code more clean
if __name__ == '__main__':
    main()
