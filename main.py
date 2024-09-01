"""
Author: Adam Knowles
Version: 0.1
Description:

GitHub Repository: https://github.com/Pharkie/
License: GNU General Public License (GPL)
"""

# Micropython libs
# import urandom  # type: ignore
from machine import UART, Pin
import uasyncio

# My project
import galactic_config

import datetime_utils
import shared_utils
import galactic_utils

display_pico_uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
uart_sreader = uasyncio.StreamReader(display_pico_uart, {})


async def listen_for_commands():
    # Uses the uasyncio.StreamReader class to read input from the standard input asynchronously without blocking.
    print("listen_for_commands() started")

    while True:
        if galactic_config.gu.is_pressed(
            galactic_config.GalacticUnicorn.SWITCH_BRIGHTNESS_UP
        ):
            galactic_config.gu.adjust_brightness(+0.01)
            galactic_config.gu.update(galactic_config.picoboard)
            await uasyncio.sleep(0.01)

        if galactic_config.gu.is_pressed(
            galactic_config.GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN
        ):
            galactic_config.gu.adjust_brightness(-0.01)
            galactic_config.gu.update(galactic_config.picoboard)
            await uasyncio.sleep(0.01)

        # Waits for a command and blocks the rest of this function, so no need for sleep in this loop
        received_text = await uart_sreader.readline()
        received_text = received_text.decode().strip()
        print(f"Text received: {received_text}")
        galactic_utils.show_static_message(
            received_text, galactic_config.PEN_BLUE, 0.2
        )

        # if received_text == b"1111show-start\n":
        #     await stop_attract_start_show()
        # elif received_text == b"22222show-stop\n":
        #     stop_show_start_attract()
        # else:
        #     print("Unknown command:", received_text.decode().strip())


if __name__ == "__main__":
    print("Start program")
    galactic_utils.show_static_message("Start", galactic_config.PEN_BLUE, 0.2)

    shared_utils.connect_wifi()

    # Add the attract tasks to the event loop. Creates vars that can be accessed in functions to cancel or restart.
    command_task = uasyncio.create_task(listen_for_commands())

    try:
        uasyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Close the event loop
        uasyncio.get_event_loop().close()
