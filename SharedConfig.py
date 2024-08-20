"""
Author: Adam Knowles
Version: 0.1
Name: config.py
Description: Set up global config, variables and objects

GitHub Repository: https://github.com/Pharkie/
License: GNU General Public License (GPL)
"""

from machine import UART, Pin
import uasyncio

from wifi_creds import WIFI_SSID, WIFI_PASSWORD

control_pico_uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
display_pico_uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

uart_swriter = uasyncio.StreamWriter(control_pico_uart, {})
uart_sreader = uasyncio.StreamReader(display_pico_uart)
