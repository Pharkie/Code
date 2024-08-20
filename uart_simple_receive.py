from machine import UART, Pin
import uasyncio

import SharedConfig

# Initialize UART
# uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
# uart = SharedConfig.display_pico_uart


async def test_uart():
    print("UART test started")
    while True:
        # if uart.any():
        received_text = await SharedConfig.uart_sreader.readline()
        print(f"Command received: {received_text.decode().strip()}")
        # command = uart.read()
        # print(f"Command received: {command.decode().strip()}")


print("UART simple receive program starting up...")
uasyncio.run(test_uart())
