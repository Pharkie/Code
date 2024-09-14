from machine import UART, Pin
import uasyncio

import config_shared
import galactic_config

# Initialize UART
display_pico_uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))


async def test_uart():
    print("UART test started")
    while True:
        if display_pico_uart.any():
            # received_text = await shared_config.uart_sreader.readline()
            # print(f"Text received: {received_text.decode().strip()}")
            text_received = display_pico_uart.read()
            print(f"Text received: {text_received.decode().strip()}")


print("UART simple receive program starting up...")
uasyncio.run(test_uart())
