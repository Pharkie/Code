import time
from rotary_irq_rp2 import RotaryIRQ
from machine import Pin


def setup_rotary_encoder(dt_pin, clk_pin, sw_pin):
    """
    Sets up the rotary encoder and button.

    Args:
        dt_pin (int): Pin number for DT.
        clk_pin (int): Pin number for CLK.
        sw_pin (int): Pin number for the button switch.

    Returns:
        tuple: RotaryIRQ instance and button Pin instance.
    """
    sw = Pin(sw_pin, Pin.IN, Pin.PULL_UP)
    rotary = RotaryIRQ(
        pin_num_dt=dt_pin,
        pin_num_clk=clk_pin,
        min_val=0,
        max_val=10,
        reverse=False,
        range_mode=RotaryIRQ.RANGE_WRAP,
    )
    return rotary, sw


def main():
    """
    Main function to run the rotary encoder and button press detection.
    """
    rotary, sw = setup_rotary_encoder(dt_pin=15, clk_pin=14, sw_pin=13)
    val_old = rotary.value()
    button_pressed = False

    while True:
        try:
            val_new = rotary.value()
            if sw.value() == 0 and not button_pressed:
                print("Button Pressed")
                print("Selected Number is:", val_new)
                button_pressed = True
                while sw.value() == 0:
                    time.sleep_ms(10)  # Debounce delay
            elif sw.value() == 1:
                button_pressed = False

            if val_old != val_new:
                val_old = val_new
                print("result =", val_new)

            time.sleep_ms(50)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
