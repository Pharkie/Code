import time
import asyncio
from machine import Pin

from rotary_irq_rp2 import RotaryIRQ


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
        max_val=20,  # Effectively sets max menu length
        reverse=False,
        range_mode=RotaryIRQ.RANGE_WRAP,
    )
    return rotary, sw


async def check_rotary(rotary, sw):
    print(f"Debug: rotary.value(): {rotary.value()}")


async def main():
    # Initialize the rotary encoder
    rotary, sw = setup_rotary_encoder(dt_pin=15, clk_pin=14, sw_pin=13)

    # Initial setting
    rotary.set(rotary.value(), 0, 1, 5)
    print(f"Initial setting: value={rotary.value()}, min_val=0, max_val=5")

    # Main loop
    while True:
        try:
            await check_rotary(rotary, sw)
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    asyncio.run(main())
