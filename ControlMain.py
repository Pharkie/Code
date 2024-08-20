"""
Author: Adam Knowles
Version: 0.1
Description:

GitHub Repository: https://github.com/Pharkie/
License: GNU General Public License (GPL)
"""

# Micropython libs
import sys
import time
import asyncio

# My project
import SharedUtils
import SharedConfig


# Function to send a command
async def send_command(command: str):
    """
    Sends a command to the UART interface.

    Args:
        command (str): The command to be sent.
    """

    await SharedConfig.uart_swriter.awrite("{}\n".format(command))
    print("Command sent:", command)

    # SharedConfig.control_pico_uart.write(
    #     command + "\n"
    # )  # Append newline character to indicate end of command


async def send_test_commands():
    """
    Asynchronously sends test commands to the UART interface in a loop.
    """
    # Uses the uasyncio.StreamReader class to read input from the standard input asynchronously without blocking.
    print("send_test_commands() started")

    while True:
        # Waits for a command and blocks the rest of this function, so need for sleep in this loop
        print("Sending start command")
        await send_command("show-start")
        await asyncio.sleep(1)
        print("Sending stop command")
        await send_command("show-stop")
        await asyncio.sleep(1)


if __name__ == "__main__":
    print("Control program starting up...")

    # SharedUtils.connect_wifi()
    uart_writer = asyncio.StreamWriter(SharedConfig.control_pico_uart, {})

    asyncio.create_task(send_test_commands())

    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Close the event loop
        asyncio.get_event_loop().close()
