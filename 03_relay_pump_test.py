"""
STEP 3: Relay + Pump Test (MicroPython)
------------------------------------------
Purpose: Confirm the ESP32 can switch the relay (and therefore the
pump) on and off.

WIRING:
- Relay VCC -> ESP32 5V
- Relay GND -> ESP32 GND
- Relay IN  -> ESP32 GPIO 26
- Pump wired through relay's COM/NO terminals with its own power
  source (check pump voltage rating - never power it from ESP32 pins)

SAFETY: Keep bare connections away from water. Relay bridges the
low-voltage ESP32 side and the pump's higher-power side safely.

ASSUMES an "active LOW" relay (LOW = ON). Swap the values below if
your relay behaves the opposite way.

HOW TO USE:
1. Wire as above (test pump in a bucket of water first).
2. Run in Thonny.
3. Pump should turn on for 3 seconds, off for 5, repeating.
"""

from machine import Pin
import time

RELAY_PIN = 26

relay = Pin(RELAY_PIN, Pin.OUT)
relay.value(1)  # Start OFF (active LOW relay)

print("Relay/pump test starting...")

while True:
    print("Pump ON")
    relay.value(0)  # ON
    time.sleep(3)

    print("Pump OFF")
    relay.value(1)  # OFF
    time.sleep(5)
