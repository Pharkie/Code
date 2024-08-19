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

# BME680 stuff
BME_ENABLED = False
PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}  # type: ignore

if BME_ENABLED:
    i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
    bme = BreakoutBME68X(
        i2c
    )  # Declare once. If you put this in a function and keep calling it, it will crash the panel after a while. # type: ignore
    # Configure the BME680. These are defaults anyway, but here in case I want to change them later
    bme.configure(FILTER_COEFF_3, STANDBY_TIME_1000_MS, OVERSAMPLING_16X, OVERSAMPLING_2X, OVERSAMPLING_1X)  # type: ignore

# Other stuff
from wifi_creds import WIFI_SSID, WIFI_PASSWORD

CHANGE_INTERVAL = 6  # seconds

base_x = 9
char_width = 5
char_height = 5

clock_digits_x = [
    base_x,
    base_x + 1 * char_width,
    base_x + (2 * char_width) + 2,
    base_x + (3 * char_width) + 2,
    base_x + (4 * char_width) + 5,
    base_x + (5 * char_width) + char_width,
]
clock_digit_all_y = -1
