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
import SharedUtils


async def listen_for_commands():
    # Uses the uasyncio.StreamReader class to read input from the standard input asynchronously without blocking.
    print("listen_for_commands() started")
    reader = uasyncio.StreamReader(sys.stdin)

    while True:
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
    print("Control Start program")

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
