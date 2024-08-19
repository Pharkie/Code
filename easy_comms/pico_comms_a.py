# Pico_comms_a
# Sends commands and listens to responses from pico_comms_b

from easy_comms.easy_comms import Easy_comms
from time import sleep

print("Initializing Easy_comms...")
com1 = Easy_comms(uart_id=0, baud_rate=9600)
com1.start()
print("Easy_comms started.")

while True:
    print("Reading message...")
    message = com1.read()

    if message is not None:
        print(f"Message received: {message}")
    else:
        print("No message received.")

    sleep(1)
    print("Sleeping for 1 second...")
