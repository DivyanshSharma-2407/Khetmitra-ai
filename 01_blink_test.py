"""
STEP 1: Blink Test (MicroPython)
---------------------------------
Purpose: Confirm the ESP32 is flashed with MicroPython correctly and
Thonny (or another tool) can run code on it.

SETUP REQUIRED BEFORE THIS WORKS:
1. Install Python on your laptop (if not already installed).
2. Install esptool: pip install esptool
3. Download the MicroPython firmware .bin for ESP32 from
   micropython.org/download/esp32/
4. Erase and flash the board:
   esptool.py --port <YOUR_PORT> erase_flash
   esptool.py --port <YOUR_PORT> write_flash -z 0x1000 <firmware.bin>
5. Install Thonny (thonny.org), set Interpreter to "MicroPython (ESP32)"
   and select your port.
6. Open this file in Thonny and click Run - it runs directly on the
   board without a separate "upload" step like Arduino IDE.

WHAT IT DOES: Blinks the onboard LED once per second, forever, and
prints a message each time so you can watch it in Thonny's Shell.
"""

from machine import Pin
import time

LED_PIN = 2  # Onboard LED on most ESP32 boards (change if needed)

led = Pin(LED_PIN, Pin.OUT)

print("Setup complete. Starting blink loop...")

while True:
    led.value(1)  # LED ON
    print("LED ON - Hello from ESP32 (MicroPython)")
    time.sleep(1)

    led.value(0)  # LED OFF
    print("LED OFF")
    time.sleep(1)
