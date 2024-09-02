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
from rotary_irq_rp2 import RotaryIRQ
import utils_shared

control_pico_uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

uart_swriter = asyncio.StreamWriter(control_pico_uart, {})


def print_function_name(func):
    def wrapper(*args, **kwargs):
        print(f"{func.__name__}() started")
        return func(*args, **kwargs)

    return wrapper


# Function to send a command
async def send_command(command: str):
    """
    Sends a command to the UART interface.

    Args:
        command (str): The command to be sent.
    """

    await uart_swriter.awrite("{}\n".format(command))
    print("Command sent:", command)


@print_function_name
async def check_rotary():
    """
    Check for rotary encoder and button press detection.
    """
    # Uses the uasyncio.StreamReader class to read input from the standard input asynchronously without blocking.
    # print(f"{check_rotary.__name__}() started")

    rotary, sw = setup_rotary_encoder(dt_pin=15, clk_pin=14, sw_pin=13)
    val_old = rotary.value()
    button_pressed = False

    while True:
        try:
            val_new = rotary.value()
            if sw.value() == 0 and not button_pressed:
                print("Button Pressed")
                print("Selected Number is:", val_new)
                await send_command("SELECT")
                button_pressed = True
                while sw.value() == 0:
                    time.sleep_ms(10)  # Debounce delay
            elif sw.value() == 1:
                button_pressed = False

            if val_old != val_new:
                val_old = val_new
                print("Sending number: ", val_new)
                await send_command(val_new)

            time.sleep_ms(50)
        except KeyboardInterrupt:
            break


def setup_rotary_encoder(dt_pin, clk_pin, sw_pin):
    """
    Sets up the rotary encoder and button.

    Args:
        dt_pin (int): Pin number for DT.
        clk_pin (int): Pin number for CLK.
        sw_pin (int): Pin number for the button switch.

    Returns:
        tuple: RotaryIRQ instance and button Pin instance.
    """
    sw = Pin(sw_pin, Pin.IN, Pin.PULL_UP)
    rotary = RotaryIRQ(
        pin_num_dt=dt_pin,
        pin_num_clk=clk_pin,
        min_val=0,
        max_val=3,
        reverse=False,
        range_mode=RotaryIRQ.RANGE_WRAP,
    )
    return rotary, sw


def main():
    print("Control program starting up...")

    utils_shared.connect_wifi()
    uart_writer = asyncio.StreamWriter(control_pico_uart, {})

    asyncio.create_task(check_rotary())

    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Close the event loop
        asyncio.get_event_loop().close()


if __name__ == "__main__":
    main()
