"""
Author: Adam Knowles
Version: 0.1
Description:

GitHub Repository: https://github.com/Pharkie/
License: GNU General Public License (GPL)
"""

# Micropython libs
import sys
import uasyncio

# My project
import SharedConfig
import GalacticConfig
import datetime_utils
import SharedUtils
import GalacticUtils


async def listen_for_commands():
    # Uses the uasyncio.StreamReader class to read input from the standard input asynchronously without blocking.
    print("Galactic listen_for_commands() started")
    reader = uasyncio.StreamReader(sys.stdin)

    while True:
        if GalacticConfig.gu.is_pressed(
            GalacticConfig.GalacticUnicorn.SWITCH_BRIGHTNESS_UP
        ):
            GalacticConfig.gu.adjust_brightness(+0.01)
            GalacticConfig.gu.update(GalacticConfig.picoboard)
            await uasyncio.sleep(0.01)

        if GalacticConfig.gu.is_pressed(
            GalacticConfig.GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN
        ):
            GalacticConfig.gu.adjust_brightness(-0.01)
            GalacticConfig.gu.update(GalacticConfig.picoboard)
            await uasyncio.sleep(0.01)

        # Waits for a command and blocks the rest of this function, so need for sleep in this loop
        command = await reader.readline()

        print(f"Command received: {command.decode().strip()}")
        if command == b"show-start\n":
            print("Show start")
        elif command == b"show-stop\n":
            print("Show stop")
        else:
            print("Unknown command:", command.decode().strip())


if __name__ == "__main__":
    print("Galactic Start program")
    GalacticUtils.show_static_message("Waiting", GalacticConfig.PEN_BLUE, 0.2)

    SharedUtils.connect_wifi()

    # Add the attract tasks to the event loop. Creates vars that can be accessed in functions to cancel or restart.
    command_task = uasyncio.create_task(listen_for_commands())

    try:
        uasyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Close the event loop
        uasyncio.get_event_loop().close()
