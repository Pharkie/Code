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

# My project
from rotary_irq_rp2 import RotaryIRQ
import utils_shared
import utils_json

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


def add_back_option(menu, depth=0):
    """
    Recursively adds a 'Back' option to each sub-menu, ensuring it is the last item.

    Args:
        menu (dict): The menu structure.
        depth (int): The current depth of the menu. Used to avoid adding 'Back' to the top-level menu.
    """
    for key, value in menu.items():
        if isinstance(value, dict):
            add_back_option(value, depth + 1)
            if (
                depth > 0 and value
            ):  # Ensure it's not the top-level menu and the sub-menu is not empty
                value["Back"] = None  # Add 'Back' option at the end


async def check_rotary():
    """
    Asynchronous function that checks the rotary encoder for menu navigation.

    Loads the menu, adds a 'Back' option to each sub-menu,
    sets up the rotary encoder and button, and continuously checks for changes
    in the rotary encoder value and button press.

    Parameters:
    None

    Returns:
    None
    """
    menu = utils_json.load_menu_from_json("menu.json")
    print("Loaded menu:", menu)  # Print the menu for debugging

    add_back_option(menu)  # Add 'Back' option to each sub-menu

    rotary, sw = setup_rotary_encoder(dt_pin=15, clk_pin=14, sw_pin=13)
    current_path = ["Main Menu"]
    selected_indices = {
        "Main Menu": 0
    }  # Dictionary to store selected index for each menu level
    button_pressed = False

    await print_current_menu_item(
        menu, current_path, selected_indices["Main Menu"]
    )

    while True:
        try:
            current_menu = menu
            for level in current_path:
                current_menu = current_menu[level]
            menu_length = len(current_menu)

            current_level = current_path[-1]
            val_new = (
                rotary.value() % menu_length
            )  # Ensure value is within menu length

            if sw.value() == 0 and not button_pressed:
                button_pressed = True
                selected_option = list(current_menu.keys())[val_new]
                if selected_option == "Back":
                    if len(current_path) > 1:
                        current_path.pop()
                    current_level = current_path[-1]
                elif current_menu[selected_option]:
                    current_path.append(selected_option)
                    selected_indices[selected_option] = (
                        0  # Start at the first item in the new sub-menu
                    )
                else:
                    print(f"Selected: {selected_option}")
                while sw.value() == 0:
                    await asyncio.sleep(0.01)  # Debounce delay
            elif sw.value() == 1:
                button_pressed = False

            if selected_indices[current_level] != val_new:
                selected_indices[current_level] = val_new
                await print_current_menu_item(menu, current_path, val_new)

            await asyncio.sleep(0.05)
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
        max_val=10,
        reverse=False,
        range_mode=RotaryIRQ.RANGE_WRAP,
    )
    return rotary, sw


async def print_current_menu_item(menu, current_path, selected_index):
    current_menu = menu
    for level in current_path:
        current_menu = current_menu[level]
    menu_keys = list(current_menu.keys())
    # if selected_index >= len(menu_keys):
    #     selected_index = 0  # Reset to the first item if out of range
    selected_item = menu_keys[selected_index]
    # print(f"Current Selection: {selected_item}")
    await send_command(selected_item)


def main():
    print("Control program starting up...")

    utils_shared.connect_wifi()

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
