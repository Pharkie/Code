from machine import Pin, UART
import uasyncio

uart = UART(0, 9600, parity=None, stop=1, bits=8)


async def sender():
    count = 0
    swriter = uasyncio.StreamWriter(uart, {})
    while True:
        await swriter.awrite("Hello uart {}\n".format(count))
        count += 1
        await uasyncio.sleep(0.5)  # This made the problem go away


async def receiver():
    sreader = uasyncio.StreamReader(uart)
    while True:
        res = await sreader.readline()
        print("Received", res)


loop = uasyncio.get_event_loop()
loop.create_task(sender())
loop.create_task(receiver())
loop.run_forever()
