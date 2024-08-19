"""
Author: Adam Knowles
Version: 0.1
Description:

GitHub Repository: https://github.com/Pharkie/
License: GNU General Public License (GPL)
"""

# Micropython libs
import urandom  # type: ignore
import TFL
import uasyncio
import sys

# My project
import config
import datetime_utils
import temp_etc_utils
import panel_attract_functions
import panel_liveshow
import utils
import cache_online_data


async def listen_for_commands():
    # Uses the uasyncio.StreamReader class to read input from the standard input asynchronously without blocking.
    # print("listen_for_commands() started")
    reader = uasyncio.StreamReader(sys.stdin)

    while True:
        if config.gu.is_pressed(config.GalacticUnicorn.SWITCH_BRIGHTNESS_UP):
            config.gu.adjust_brightness(+0.01)
            config.gu.update(config.picoboard)
            await uasyncio.sleep(0.01)

        if config.gu.is_pressed(config.GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN):
            config.gu.adjust_brightness(-0.01)
            config.gu.update(config.picoboard)
            await uasyncio.sleep(0.01)

        # Waits for a command and blocks the rest of this function, so need for sleep in this loop
        command = await reader.readline()

        print(f"Command received: {command.decode().strip()}")
        if command == b"show-start\n":
            await stop_attract_start_show()
        elif command == b"show-stop\n":
            stop_show_start_attract()
        else:
            print("Unknown command:", command.decode().strip())


if __name__ == "__main__":
    print("Start program")
    utils.show_static_message("Waiting", config.PEN_BLUE, 0.2)

    utils.connect_wifi()

    # Add the attract tasks to the event loop. Creates vars that can be accessed in functions to cancel or restart.
    command_task = uasyncio.create_task(listen_for_commands())

    try:
        uasyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Close the event loop
        uasyncio.get_event_loop().close()
