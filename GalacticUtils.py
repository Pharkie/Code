"""
Author: Adam Knowles
Version: 0.1
Name: utils.py
Description: General utils not specific to a particular thing

GitHub Repository: https://github.com/Pharkie/AdamGalactic/
License: GNU General Public License (GPL)
"""

import GalacticConfig
import network  # type: ignore
import utime  # type: ignore

import uasyncio


def clear_picoboard():
    GalacticConfig.picoboard.set_pen(GalacticConfig.PEN_BLACK)
    GalacticConfig.picoboard.clear()
    GalacticConfig.gu.update(GalacticConfig.picoboard)


def show_static_message(message, pen_colour, brightness=1.0):
    # print(f"show_static_message() called with message: {message}, pen_colour: {pen_colour}, brightness: {brightness}")

    previous_brightness = GalacticConfig.gu.get_brightness()
    clear_picoboard()

    GalacticConfig.picoboard.set_pen(GalacticConfig.PEN_GREY)

    # Calculate the X position to center the text horizontally
    text_width = GalacticConfig.picoboard.measure_text(message, 1)
    x_pos = (GalacticConfig.DISPLAY_WIDTH - text_width) // 2

    # Split the message into two lines if the text width is greater than display width
    if text_width > GalacticConfig.DISPLAY_WIDTH:
        # Find the index of the space closest to the center of the message
        space_index = len(message) // 2
        while message[space_index] != " ":
            space_index += 1

        # Split the message into two lines at the space index
        line1 = message[:space_index]
        line2 = message[space_index + 1 :]

        # Calculate the X position to center each line horizontally
        text_width1 = GalacticConfig.picoboard.measure_text(line1, 1)
        x_pos1 = (GalacticConfig.DISPLAY_WIDTH - text_width1) // 2
        text_width2 = GalacticConfig.picoboard.measure_text(line2, 1)
        x_pos2 = (GalacticConfig.DISPLAY_WIDTH - text_width2) // 2

        # Display each line of the message on a separate line
        GalacticConfig.picoboard.text(
            text=line1, x1=x_pos1, y1=-1, wordwrap=-1, scale=1
        )
        GalacticConfig.picoboard.text(
            text=line2, x1=x_pos2, y1=5, wordwrap=-1, scale=1
        )
    else:
        # Display the message on a single line
        GalacticConfig.picoboard.text(
            text=message, x1=x_pos, y1=2, wordwrap=-1, scale=1
        )

    GalacticConfig.gu.set_brightness(brightness)
    GalacticConfig.gu.update(GalacticConfig.picoboard)
    GalacticConfig.gu.set_brightness(previous_brightness)


async def scroll_msg(msg_text):
    # print(f"scroll_msg() called with msg_text: {msg_text}")

    length = GalacticConfig.picoboard.measure_text(msg_text, 1)
    steps = (
        length + GalacticConfig.DISPLAY_WIDTH
    )  # Scroll the msg_text with a bit of padding, min 53

    p = GalacticConfig.DISPLAY_WIDTH
    for _ in range(steps):
        GalacticConfig.picoboard.set_pen(GalacticConfig.PEN_BLACK)
        GalacticConfig.picoboard.clear()
        GalacticConfig.picoboard.set_pen(GalacticConfig.PEN_YELLOW)
        GalacticConfig.picoboard.text(
            text=msg_text, x1=p, y1=2, wordwrap=-1, scale=1
        )
        GalacticConfig.gu.update(GalacticConfig.picoboard)
        p -= 1
        await uasyncio.sleep(0.03)

    # print("scroll_msg() complete")
