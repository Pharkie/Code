# Easy comms is a simple class that allows you to send and receive messages over a serial port.

from machine import UART, Pin
from time import time_ns
from typing import Optional


class Easy_comms:
    def __init__(
        self, uart_id: int, baud_rate: int = 9600, timeout: int = 1000
    ):
        """
        Initialize the Easy_comms class.

        :param uart_id: UART ID to use.
        :param baud_rate: Baud rate for the UART communication.
        :param timeout: Timeout for reading messages in milliseconds.
        """
        self.uart_id = uart_id
        self.baud_rate = baud_rate
        self.timeout = timeout  # milliseconds

        # Initialize the UART serial port
        self.uart = UART(self.uart_id, self.baud_rate)
        self.uart.init()

    def send(self, message: str) -> None:
        """
        Send a message over the UART.

        :param message: The message to send.
        """
        print(f"sending message: {message}")
        message = message + "\n"
        self.uart.write(bytes(message, "utf-8"))

    def start(self) -> None:
        """
        Start the communication by sending an initial message.
        """
        message = "ahoy\n"
        print(message)
        self.send(message)

    def read(self) -> Optional[str]:
        """
        Read a message from the UART.

        :return: The received message or None if no message is received within the timeout period.
        """
        start_time = time_ns()
        message = ""
        while (time_ns() - start_time) // 1_000_000 < self.timeout:
            if self.uart.any() > 0:
                message += self.uart.read().decode("utf-8")
                if "\n" in message:
                    return message.strip("\n")
        return None  # Return None if no message is received within the timeout period.
