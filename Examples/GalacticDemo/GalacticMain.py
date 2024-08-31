"""
Author: Adam Knowles
Version: 0.1
Description:

GitHub Repository: https://github.com/Pharkie/
License: GNU General Public License (GPL)
"""

# Micropython libs
import uasyncio

# My project
import shared_config
import galactic_Config
import galactic_utils


async def listen_for_commands():
    # Uses the uasyncio.StreamReader class to read input from the standard input asynchronously without blocking.
    print("Galactic listen_for_commands() started")

    while True:
        # Waits for a command and blocks the rest of this function, so need for sleep in this loop
        received_text = await shared_config.uart_sreader.readline()
        print(f"Command received: {received_text.decode().strip()}")


if __name__ == "__main__":
    print("Galactic program starting up...")
    # GalacticUtils.show_static_message("Waiting", GalacticConfig.PEN_BLUE, 0.2)

    # SharedUtils.connect_wifi()

    uasyncio.create_task(listen_for_commands())

    try:
        uasyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Close the event loop
        uasyncio.get_event_loop().close()
