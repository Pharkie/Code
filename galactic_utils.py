"""
Author: Adam Knowles
Version: 0.1
Name: utils.py
Description: General utils not specific to a particular thing

GitHub Repository: https://github.com/Pharkie/AdamGalactic/
License: GNU General Public License (GPL)
"""

import galactic_config
import network  # type: ignore
import utime  # type: ignore

import uasyncio


def clear_picoboard():
    galactic_config.picoboard.set_pen(galactic_config.PEN_BLACK)
    galactic_config.picoboard.clear()
    galactic_config.gu.update(galactic_config.picoboard)


def show_static_message(message, pen_colour, brightness=1.0):
    previous_brightness = galactic_config.gu.get_brightness()
    clear_picoboard()

    galactic_config.picoboard.set_pen(galactic_config.PEN_GREY)

    # Calculate the X position to center the text horizontally
    text_width = galactic_config.picoboard.measure_text(message, 1)
    x_pos = (galactic_config.DISPLAY_WIDTH - text_width) // 2

    # Split the message into two lines if the text width is greater than display width
    if text_width > galactic_config.DISPLAY_WIDTH:
        # Find the index of the space closest to the center of the message
        space_index = len(message) // 2
        left_space_index = message.rfind(" ", 0, space_index)
        right_space_index = message.find(" ", space_index)

        # Choose the closest space to the center
        if left_space_index == -1 and right_space_index == -1:
            # If no space is found, split the message at the center
            space_index = len(message) // 2
        elif left_space_index == -1:
            space_index = right_space_index
        elif right_space_index == -1:
            space_index = left_space_index
        else:
            space_index = (
                left_space_index
                if (space_index - left_space_index)
                <= (right_space_index - space_index)
                else right_space_index
            )

        # Split the message into two lines at the space index
        line1 = message[:space_index]
        line2 = message[space_index + 1 :]

        # Calculate the X position to center each line horizontally
        text_width1 = galactic_config.picoboard.measure_text(line1, 1)
        x_pos1 = (galactic_config.DISPLAY_WIDTH - text_width1) // 2
        text_width2 = galactic_config.picoboard.measure_text(line2, 1)
        x_pos2 = (galactic_config.DISPLAY_WIDTH - text_width2) // 2

        # Display each line of the message on a separate line
        galactic_config.picoboard.text(
            text=line1, x1=x_pos1, y1=-1, wordwrap=-1, scale=1
        )
        galactic_config.picoboard.text(
            text=line2, x1=x_pos2, y1=5, wordwrap=-1, scale=1
        )
    else:
        # Display the message on a single line
        galactic_config.picoboard.text(
            text=message, x1=x_pos, y1=2, wordwrap=-1, scale=1
        )

    galactic_config.gu.set_brightness(brightness)
    galactic_config.gu.update(galactic_config.picoboard)
    galactic_config.gu.set_brightness(previous_brightness)


async def scroll_msg(msg_text):
    # print(f"scroll_msg() called with msg_text: {msg_text}")

    length = galactic_config.picoboard.measure_text(msg_text, 1)
    steps = (
        length + galactic_config.DISPLAY_WIDTH
    )  # Scroll the msg_text with a bit of padding, min 53

    p = galactic_config.DISPLAY_WIDTH
    for _ in range(steps):
        galactic_config.picoboard.set_pen(galactic_config.PEN_BLACK)
        galactic_config.picoboard.clear()
        galactic_config.picoboard.set_pen(galactic_config.PEN_YELLOW)
        galactic_config.picoboard.text(
            text=msg_text, x1=p, y1=2, wordwrap=-1, scale=1
        )
        galactic_config.gu.update(galactic_config.picoboard)
        p -= 1
        await uasyncio.sleep(0.03)

    # print("scroll_msg() complete")


def main():
    # Test clear_picoboard function
    print("Testing clear_picoboard()")
    clear_picoboard()
    print("clear_picoboard() test complete")
    utime.sleep(1)  # Delay for 1 second

    # Test show_static_message function
    print("Testing show_static_message()")
    show_static_message(
        "Hello World123456", galactic_config.PEN_GREEN, brightness=1
    )
    print("show_static_message() test complete")
    utime.sleep(1)  # Delay for 1 second

    # Test scroll_msg function
    print("Testing scroll_msg()")
    uasyncio.run(scroll_msg("Scrolling Message"))
    print("scroll_msg() test complete")
    utime.sleep(1)  # Delay for 1 second


if __name__ == "__main__":
    main()
