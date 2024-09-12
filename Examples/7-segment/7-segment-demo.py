import machine
import time


class TM1637:
    def __init__(self, clk, dio):
        self.clk = machine.Pin(clk, machine.Pin.OUT)
        self.dio = machine.Pin(dio, machine.Pin.OUT)
        self.clk.init(machine.Pin.OUT, value=0)
        self.dio.init(machine.Pin.OUT, value=0)
        self.brightness = 7
        self.cmd_set_data = 0x40
        self.cmd_set_addr = 0xC0
        self.cmd_display_ctrl = 0x88 | self.brightness
        self.digits = [
            0x3F,
            0x06,
            0x5B,
            0x4F,
            0x66,
            0x6D,
            0x7D,
            0x07,
            0x7F,
            0x6F,
        ]

    def start(self):
        self.dio(1)
        self.clk(1)
        self.dio(0)
        self.clk(0)

    def stop(self):
        self.clk(0)
        self.dio(0)
        self.clk(1)
        self.dio(1)

    def write_byte(self, data):
        for i in range(8):
            self.clk(0)
            self.dio((data >> i) & 1)
            self.clk(1)
        self.clk(0)
        self.dio(1)
        self.clk(1)
        self.dio.init(machine.Pin.IN)
        ack = self.dio()
        self.dio.init(machine.Pin.OUT)
        return ack

    def display(self, data):
        self.start()
        self.write_byte(self.cmd_set_data)
        self.stop()
        self.start()
        self.write_byte(self.cmd_set_addr)
        for i in range(4):
            self.write_byte(self.digits[data[i]])
        self.stop()
        self.start()
        self.write_byte(self.cmd_display_ctrl)
        self.stop()


# Function to configure pins and run the demo
def run_demo(clk_pin, dio_pin):
    # Initialize the display
    tm = TM1637(clk=clk_pin, dio=dio_pin)

    # Demo loop to display numbers 0-9999
    while True:
        for i in range(10000):
            tm.display([i // 1000 % 10, i // 100 % 10, i // 10 % 10, i % 10])
            time.sleep(0.05)


# Example usage: configure pins 14 and 12
run_demo(clk_pin=16, dio_pin=17)
