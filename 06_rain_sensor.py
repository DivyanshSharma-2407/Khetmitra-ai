"""
STEP 6: Rain Sensor Test + Integration (MicroPython)
--------------------------------------------------------
Purpose: Skip watering when rain is detected, even if soil reads dry.

WIRING:
- Rain sensor VCC -> ESP32 3.3V
- Rain sensor GND -> ESP32 GND
- Rain sensor DO  -> ESP32 GPIO 27

Most boards: digital output HIGH = dry, LOW = rain detected. Test
yours first (drip water on it) and flip RAIN_DETECTED_STATE if
reversed.

HOW TO USE:
1. Wire as above.
2. Run in Thonny, watch Serial output while dripping water on sensor
   to confirm which state means "raining" for your board.
3. Once confirmed, this integrated loop combines rain + soil + relay
   logic: rain detected always skips watering, regardless of soil
   dryness.
"""

from machine import Pin, ADC
import time

SOIL_PIN = 34
RELAY_PIN = 26
RAIN_PIN = 27

DRY_THRESHOLD = 2200       # TODO: use your Step 2 calibrated value
RAIN_DETECTED_STATE = 0    # 0 = LOW means rain; change to 1 if reversed

WATER_DURATION_S = 3
CHECK_INTERVAL_S = 10

soil_adc = ADC(Pin(SOIL_PIN))
soil_adc.atten(ADC.ATTN_11DB)

relay = Pin(RELAY_PIN, Pin.OUT)
relay.value(1)  # Pump starts OFF

rain_sensor = Pin(RAIN_PIN, Pin.IN)

print("Rain sensor + auto watering system starting...")

while True:
    soil_value = soil_adc.read()
    rain_state = rain_sensor.value()
    is_raining = (rain_state == RAIN_DETECTED_STATE)
    is_soil_dry = soil_value > DRY_THRESHOLD

    print("Soil:", soil_value, "| Rain detected:", "YES" if is_raining else "NO", end=" ")

    if is_raining:
        print("-> Skipping watering (rain detected).")
    elif is_soil_dry:
        print("-> Soil is dry and no rain. Watering now.")
        relay.value(0)
        time.sleep(WATER_DURATION_S)
        relay.value(1)
        print("Watering complete.")
    else:
        print("-> Soil moist enough. No action.")

    time.sleep(CHECK_INTERVAL_S)
