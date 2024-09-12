try:
    from machine import Pin
    import time
    import tm1637  # type: ignore See https://github.com/mcauser/micropython-tm1637
except ImportError as e:
    print(f"Failed to import required modules: {e}")
    print("Please ensure that the tm1637 library is installed.")
    # Exit the script if the import fails
    import sys

    sys.exit(1)


def initialize_display(clk_pin, dio_pin):
    try:
        # Create a TM1637 display instance
        tm = tm1637.TM1637(clk=Pin(clk_pin), dio=Pin(dio_pin))
        # Set the brightness (0-7)
        tm.brightness(7)
        # Test the display by showing '8888'
        tm.show("hipi")
        time.sleep(1)
        tm.show("    ")  # Clear the display
        return tm
    except Exception as exception_error:
        print(
            f"Failed to initialize display with CLK pin {clk_pin} and DIO pin {dio_pin}: {exception_error}"
        )
        return None


print("7-segment display demo using the MP TM1637 library")
# Initialize the display with the specified clock and data pins
clk_pin = 16  # Change to your CLK pin
dio_pin = 17  # Change to your DIO pin

print("Initializing display...")
tm = initialize_display(clk_pin, dio_pin)

if tm:
    print("Display initialized successfully.")
    # Demo loop to display numbers 0-9999
    while True:
        for i in range(10000):
            print(f"Displaying number: {i}")  # Debugging statement
            tm.numbers(i // 100, i % 100)  # Display the number in two parts
            time.sleep(0.05)
else:
    print("Please check the pin connections and try again.")
