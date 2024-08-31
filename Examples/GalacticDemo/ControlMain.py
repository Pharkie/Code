"""
Author: Adam Knowles
Version: 0.1
Description:

GitHub Repository: https://github.com/Pharkie/
License: GNU General Public License (GPL)
"""

# Micropython libs
from machine import UART, Pin
import sys
import time
import asyncio

# My project
import shared_utils

control_pico_uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

uart_swriter = asyncio.StreamWriter(control_pico_uart, {})


# Function to send a command
async def send_command(command: str):
    """
    Sends a command to the UART interface.

    Args:
        command (str): The command to be sent.
    """

    await uart_swriter.awrite("{}\n".format(command))
    print("Command sent:", command)


async def send_test_commands():
    """
    Asynchronously sends test commands to the UART interface in a loop.
    """
    # Uses the uasyncio.StreamReader class to read input from the standard input asynchronously without blocking.
    print("send_test_commands() started")

    while True:
        # Waits for a command and blocks the rest of this function, so need for sleep in this loop
        # print("Sending start command")
        await send_command("BOO")
        await asyncio.sleep(1)
        # print("Sending stop command")
        await send_command("HISS")
        await asyncio.sleep(1)


if __name__ == "__main__":
    print("Control program starting up...")

    # shared_utils.connect_wifi()
    uart_writer = asyncio.StreamWriter(control_pico_uart, {})

    asyncio.create_task(send_test_commands())

    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Close the event loop
        asyncio.get_event_loop().close()
