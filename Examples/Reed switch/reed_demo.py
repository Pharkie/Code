import machine
import time

# Initialize GPIO16 as an input pin with a pull-up resistor
reed_switch = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)


def read_reed_switch():
    # Read the state of the reed switch
    return reed_switch.value()


# Main loop
previous_state = read_reed_switch()

# Print the initial state at startup
if previous_state == 0:
    print("Reed switch is CLOSED")
else:
    print("Reed switch is OPEN")

while True:
    current_state = read_reed_switch()
    if current_state != previous_state:
        if current_state == 0:
            print("Reed switch is CLOSED")
        else:
            print("Reed switch is OPEN")
        previous_state = current_state
    time.sleep(0.1)  # Small delay to debounce the switch
