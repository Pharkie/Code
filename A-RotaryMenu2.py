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
async def send_gu_text(command: str):
    """
    Sends a command to the UART interface.

    Args:
        command (str): The command to be sent.
    """

    await uart_swriter.awrite("{}\n".format(command))
    print("Sent text to GU:", command)


async def send_gu_current_selection_text(menu, current_path):
    """
    Send the current menu item based on the selected index to the GUI.

    Parameters:
    menu (dict): The entire menu structure.
    current_path (list): The current path in the menu.

    Returns:
    None
    """
    current_menu, selected_index = get_current_menu_level(menu, current_path)
    menu_keys = list(current_menu.keys())
    selected_item = menu_keys[selected_index]
    await send_gu_text(selected_item)


def add_back_to_menus(menu, depth=0):
    """
    Recursively adds a 'Back' option to each sub-menu, ensuring it is the last item.

    Args:
        menu (dict): The menu structure.
        depth (int): The current depth of the menu. Used to avoid adding 'Back' to the top-level menu.
    """
    for key, value in menu.items():
        if isinstance(value, dict):
            add_back_to_menus(value, depth + 1)
            if (
                depth > 0 and value
            ):  # Ensure it's not the top-level menu and the sub-menu is not empty
                value["Back"] = None  # Add 'Back' option at the end


def get_current_menu_level(menu, current_path):
    """
    Helper function to get the current menu level and selected index based on the current path.

    Parameters:
    menu (dict): The entire menu structure.
    current_path (list): The current path in the menu.

    Returns:
    tuple: The current menu level and selected index.
    """
    current_menu = menu
    for level, _ in current_path[:-1]:
        current_menu = current_menu[level]
    current_level, selected_index = current_path[-1]
    return current_menu[current_level], selected_index


async def check_rotary():
    main_menu = utils_json.load_menu_from_json("menu.json")
    add_back_to_menus(main_menu)

    rotary, sw = setup_rotary_encoder(dt_pin=15, clk_pin=14, sw_pin=13)
    current_path = [
        ("Main Menu", 0)
    ]  # Store tuples of (menu level, selected index)
    button_pressed = False

    await send_gu_current_selection_text(main_menu, current_path)

    while True:
        try:
            current_menu, saved_index = get_current_menu_level(
                main_menu, current_path
            )
            menu_length = len(current_menu)
            val_new = (
                rotary.value() % menu_length
            )  # Ensure value is within menu length

            if sw.value() == 0 and not button_pressed:
                button_pressed = True
                selected_option = list(current_menu.keys())[val_new]

                if current_menu[
                    selected_option
                ]:  # If the selected option is a sub-menu
                    current_path.append(
                        (selected_option, 0)
                    )  # Start at the first item in the new sub-menu
                    val_new = 0  # Reset val_new to 0 when entering a sub-menu
                    # Recalculate val_new after changing the menu
                    current_menu, saved_index = get_current_menu_level(
                        main_menu, current_path
                    )
                    menu_length = len(current_menu)
                    val_new = (
                        rotary.value() % menu_length
                    )  # Ensure value is within menu length
                elif selected_option == "Back":  # If 'Back' is selected
                    if len(current_path) > 1:
                        current_path.pop()
                        # Use the saved index from the previous menu level
                        current_menu, saved_index = get_current_menu_level(
                            main_menu, current_path
                        )
                        val_new = saved_index
                        # Recalculate val_new after changing the menu
                        current_menu, saved_index = get_current_menu_level(
                            main_menu, current_path
                        )
                        menu_length = len(current_menu)
                        val_new = (
                            rotary.value() % menu_length
                        )  # Ensure value is within menu length
                elif not current_menu[
                    selected_option
                ]:  # If the selected option is a leaf node
                    print(f"Execute: {selected_option}")

                while sw.value() == 0:
                    await asyncio.sleep(0.01)  # Debounce delay
            elif sw.value() == 1:
                button_pressed = False

            if saved_index != val_new:
                current_path[-1] = (current_path[-1][0], val_new)
                await send_gu_current_selection_text(main_menu, current_path)

                print(f"Debug: Current Path: {current_path}")
                print(f"Debug: Current Menu: {list(current_menu.keys())}")
                print(f"Debug: saved_index: {saved_index}, val_new: {val_new}")

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
