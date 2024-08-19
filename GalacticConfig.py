"""
Author: Adam Knowles
Version: 0.1
Name: config.py
Description: Set up global config, variables and objects

GitHub Repository: https://github.com/Pharkie/
License: GNU General Public License (GPL)
"""

from galactic import GalacticUnicorn  # type: ignore
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY  # type: ignore
from pimoroni_i2c import PimoroniI2C  # type: ignore

# GU stuff
gu = GalacticUnicorn()
picoboard = PicoGraphics(DISPLAY)

DISPLAY_WIDTH = 53

# Pen colours
PEN_BLACK = picoboard.create_pen(0, 0, 0)
PEN_YELLOW = picoboard.create_pen(255, 105, 0)
PEN_GREY = picoboard.create_pen(96, 96, 96)
PEN_BLUE = picoboard.create_pen(153, 255, 255)
PEN_GREEN = picoboard.create_pen(38, 133, 40)

picoboard.set_font("bitmap6")

base_x = 9
char_width = 5
char_height = 5
