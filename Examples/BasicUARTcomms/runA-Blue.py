import time
from machine import UART, Pin  # we need to import UART to use it

# Initialize UART 0 on Pico A, TX pin is GP0 and RX pin is GP1
test_uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

print("Blue Control Pico starting up...")

while True:
    test_uart.write("ON")  # Send 'ON' message to Pico B
    time.sleep(1)  # Wait for 2 seconds

    test_uart.write("OFF")  # Send 'OFF' message to Pico B
    time.sleep(1)  # Wait for 2 seconds
