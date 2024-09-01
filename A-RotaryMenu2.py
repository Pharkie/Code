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
        max_val=20,  # Effectively sets max menu length
        reverse=False,
        range_mode=RotaryIRQ.RANGE_WRAP,
    )
    return rotary, sw


def modify_menu(menu, depth=0):
    """
    Recursively modifies the menu to add ' >' to the end of any items that are submenus
    and adds a '< Back' option to each sub-menu, ensuring it is the last item.

    Args:
        menu (dict): The menu structure.
        depth (int): The current depth of the menu. Used to avoid adding '< Back' to the top-level menu.
    """
    keys = list(menu.keys())
    for key in keys:
        value = menu.pop(key)
        if isinstance(value, dict):
            new_key = f"{key} >"
            menu[new_key] = modify_menu(
                value, depth + 1
            )  # Recurse into the submenu
            if depth > 0:  # Ensure it's not the top-level menu
                menu[new_key]["< Back"] = None  # Add '< Back' option at the end
        else:
            menu[key] = value
    return OrderedDict(menu)


# Function to send a command
async def send_gu_text(text_to_send: str):
    """
    Sends a command to the UART interface.

    Args:
        command (str): The command to be sent.
    """

    await uart_swriter.awrite("{}\n".format(text_to_send))
    print("Sent text to GU:", text_to_send)


def get_current_menu_level(menu, current_path):
    """
    Helper function to get the current menu level based on the current path.

    Parameters:
    menu (dict): The entire menu structure.
    current_path (list): The current path in the menu.

    Returns:
    dict: The current menu level.
    """
    current_menu = menu
    for level, _ in current_path[:-1]:
        current_menu = current_menu[level]
    current_level, selected_index = current_path[-1]
    return current_menu[current_level]


async def send_gu_current_selection_text(menu, current_path):
    """
    Sends the current selection text to the GUI.

    Parameters:
    menu (dict): The entire menu structure.
    current_path (list): The current path in the menu.
    """
    current_menu = get_current_menu_level(menu, current_path)
    current_level, selected_index = current_path[-1]
    selected_option = list(current_menu.keys())[selected_index]
    # Send the selected option text to the GUI
    await send_gu_text(selected_option)


async def initialize_menu():
    main_menu = utils_json.load_menu_from_json("menu.json")
    modify_menu(main_menu)
    return main_menu


def initialize_rotary_encoder():
    return setup_rotary_encoder(dt_pin=15, clk_pin=14, sw_pin=13)


async def update_current_selection(main_menu, current_path, rotary):
    current_menu = get_current_menu_level(main_menu, current_path)
    menu_length = len(current_menu)

    rotary_value_this_menu = (
        rotary.value() % menu_length
    )  # Wrap around rotary values

    if (
        len(current_path) > 1
    ):  # Counteract the offset caused by previous selection
        rotary_value_fixed = (
            rotary_value_this_menu - current_path[-2][1]
        ) % menu_length
    else:
        rotary_value_fixed = rotary_value_this_menu

    if current_path[-1][1] != rotary_value_fixed:
        print(
            f"Debug: Rotary value change from {current_path[-1][1]} to {rotary_value_fixed}"
        )
        current_path[-1] = (current_path[-1][0], rotary_value_fixed)
        print(f"Debug: Current Path: {current_path}")
        await send_gu_current_selection_text(main_menu, current_path)


async def handle_button_press(
    main_menu, current_path, rotary, sw, button_pressed
):
    current_menu = get_current_menu_level(main_menu, current_path)
    menu_length = len(current_menu)
    rotary_value_this_menu = (
        rotary.value() % menu_length
    )  # Wrap around rotary values

    if (
        len(current_path) > 1
    ):  # Counteract the offset caused by previous selection
        rotary_value_fixed = (
            rotary_value_this_menu - current_path[-2][1]
        ) % menu_length
    else:
        rotary_value_fixed = rotary_value_this_menu

    if sw.value() == 0 and not button_pressed:
        button_pressed = True
        selected_option = list(current_menu.keys())[rotary_value_fixed]

        if current_menu[
            selected_option
        ]:  # If the selected option is a sub-menu
            current_path.append(
                (selected_option, 0)
            )  # Start at the first item in the new sub-menu
            await send_gu_current_selection_text(main_menu, current_path)
            print(f"Debug, Sub-menu selected, current Path: {current_path}")
        elif (
            selected_option == "< Back" and len(current_path) > 1
        ):  # If 'Back' is selected
            current_path.pop()
            await send_gu_current_selection_text(main_menu, current_path)
            print(f"Debug, Back selected, current Path: {current_path}")
        else:  # If the selected option is a leaf node
            print(f"Execute: {selected_option}")

        while sw.value() == 0:
            await asyncio.sleep(0.01)  # Debounce delay
    elif sw.value() == 1:
        button_pressed = False

    return button_pressed


async def main_loop():
    main_menu = await initialize_menu()
    rotary, sw = initialize_rotary_encoder()
    current_path = [
        ("Main Menu >", 0)
    ]  # Store tuples of (menu level, selected index)
    button_pressed = False

    await send_gu_current_selection_text(main_menu, current_path)

    while True:
        try:
            await update_current_selection(main_menu, current_path, rotary)
            button_pressed = await handle_button_press(
                main_menu, current_path, rotary, sw, button_pressed
            )
            await asyncio.sleep(0.05)
        except KeyboardInterrupt:
            break


# Call the main loop
asyncio.run(main_loop())


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
        max_val=20,  # Effectively sets max menu length
        reverse=False,
        range_mode=RotaryIRQ.RANGE_WRAP,
    )
    return rotary, sw


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
