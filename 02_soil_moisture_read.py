"""
STEP 2: Soil Moisture Sensor - Raw Reading (MicroPython)
-----------------------------------------------------------
Purpose: Read raw values from a capacitive soil moisture sensor.

WIRING:
- Sensor VCC  -> ESP32 3.3V
- Sensor GND  -> ESP32 GND
- Sensor AOUT -> ESP32 GPIO 34 (analog-capable pin)

HOW IT WORKS:
ESP32's ADC reads a voltage and converts it to a number. In
MicroPython, ADC readings are typically 0-4095 (12-bit), same range
as Arduino-style code, though this can vary slightly by port/firmware.
- Drier soil (or open air) -> higher number
- Wetter soil / in water   -> lower number

HOW TO USE:
1. Wire the sensor as above.
2. Run this script in Thonny.
3. Note the reading dry, then dip sensor in water, note the reading
   again. Write both down - needed for Step 4's threshold.
"""

from machine import Pin, ADC
import time

SOIL_PIN = 34

soil_adc = ADC(Pin(SOIL_PIN))
soil_adc.atten(ADC.ATTN_11DB)  # Allows reading full 0-3.3V range

print("Soil moisture raw reading test.")
print("Watch how the value changes between dry and wet.")

while True:
    raw_value = soil_adc.read()  # 0-4095
    print("Raw soil moisture value:", raw_value)
    time.sleep(1)
