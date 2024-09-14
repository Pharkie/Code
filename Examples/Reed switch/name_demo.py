import machine
import time

# Initialize GPIO pins as input pins with pull-up resistors
reed_switches = [
    machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP),  # Switch 1
    machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP),  # Switch 2
    machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP),  # Switch 3
]

# Define human names for each switch state configuration
player_names = [
    "None",  # 000
    "Greta",  # 001
    "Trix Manhandle",  # 010
    "Chun Li",  # 011
    "Pac man",  # 100
    "Wolfdaughter",  # 101
    "The wolf",  # 110
    "Pharkie",  # 111
]


def read_reed_switch(index):
    # Read the state of the reed switch at the given index
    return reed_switches[index].value()


def get_switch_states():
    # Get the states of all reed switches
    states = [read_reed_switch(i) for i in range(3)]
    return ["CLOSED" if state == 0 else "OPEN" for state in states]


def get_player_name(states):
    # Convert states to a binary string and then to an integer
    binary_string = "".join(
        ["1" if state == "CLOSED" else "0" for state in states]
    )
    index = int(binary_string, 2)
    return player_names[index]


# Main loop
previous_states = get_switch_states()

# Print the initial state at startup
print(previous_states, get_player_name(previous_states))

while True:
    current_states = get_switch_states()
    if current_states != previous_states:
        player_name = get_player_name(current_states)
        print(current_states, player_name)
        previous_states = current_states
    time.sleep(1)  # Small delay to debounce the switches
