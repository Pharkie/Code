from machine import UART, Pin
import uasyncio

import shared_config
import galactic_config

# Initialize UART
# uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
uart = shared_config.display_pico_uart


async def test_uart():
    print("UART test started")
    while True:
        if uart.any():
            # received_text = await shared_config.uart_sreader.readline()
            # print(f"Text received: {received_text.decode().strip()}")
            text_received = uart.read()
            print(f"Text received: {text_received.decode().strip()}")


print("UART simple receive program starting up...")
uasyncio.run(test_uart())
