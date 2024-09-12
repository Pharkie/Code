import network
import time


def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    # Wait for connection
    max_attempts = 10
    attempt = 0
    while not wlan.isconnected() and attempt < max_attempts:
        print("Connecting to Wi-Fi...")
        time.sleep(1)
        attempt += 1

    if wlan.isconnected():
        print("Connected to Wi-Fi")
        print("Network config:", wlan.ifconfig())
    else:
        print("Failed to connect to Wi-Fi")


# Replace with your Wi-Fi credentials
ssid = "MooseCave"
password = "This7Muggles2%"

connect_to_wifi(ssid, password)
