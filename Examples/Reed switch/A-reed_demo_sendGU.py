"""
Author: Adam Knowles
Version: 0.1
Description:

GitHub Repository: https://github.com/Pharkie/
License: GNU General Public License (GPL)
"""

# Micropython libs
from machine import UART, Pin
import asyncio
from collections import OrderedDict

# My project
import utils_shared
import utils_json

control_pico_uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

uart_swriter = asyncio.StreamWriter(control_pico_uart, {})

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


# Function to send a command
async def send_gu_text(text_to_send: str):
    """
    Sends a command to the UART interface.

    Args:
        command (str): The command to be sent.
    """

    await uart_swriter.awrite("{}\n".format(text_to_send))
    print("Sent text to GU:", text_to_send)


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


async def main_loop():
    # Main loop
    previous_states = get_switch_states()

    # Print the initial state at startup
    print(previous_states, get_player_name(previous_states))

    while True:
        current_states = get_switch_states()
        if current_states != previous_states:
            player_name = get_player_name(current_states)
            print(current_states, player_name)
            await send_gu_text(player_name)
            previous_states = current_states
        await asyncio.sleep(1)  # Small delay to debounce the switches


def main():
    print("Control program starting up...")

    asyncio.create_task(main_loop())

    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Close the event loop
        asyncio.get_event_loop().close()


if __name__ == "__main__":
    main()
