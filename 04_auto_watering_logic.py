"""
STEP 4: Automatic Watering Logic (MicroPython)
--------------------------------------------------
Purpose: Combine Steps 2 and 3 - water automatically when soil is dry.

WIRING: Soil sensor on GPIO 34, relay on GPIO 26 (same as before).

CALIBRATE FIRST: Update DRY_THRESHOLD using your own dry/wet numbers
from Step 2 before relying on this.
"""

from machine import Pin, ADC
import time

SOIL_PIN = 34
RELAY_PIN = 26

DRY_THRESHOLD = 2200  # TODO: replace with YOUR measured values

WATER_DURATION_S = 3
CHECK_INTERVAL_S = 10

soil_adc = ADC(Pin(SOIL_PIN))
soil_adc.atten(ADC.ATTN_11DB)

relay = Pin(RELAY_PIN, Pin.OUT)
relay.value(1)  # Pump starts OFF

print("Automatic watering system starting...")

while True:
    soil_value = soil_adc.read()
    print("Soil reading:", soil_value, end=" ")

    if soil_value > DRY_THRESHOLD:
        print("-> Soil is DRY. Watering now.")
        relay.value(0)  # Pump ON
        time.sleep(WATER_DURATION_S)
        relay.value(1)  # Pump OFF
        print("Watering complete.")
    else:
        print("-> Soil is moist enough. No action.")

    time.sleep(CHECK_INTERVAL_S)
