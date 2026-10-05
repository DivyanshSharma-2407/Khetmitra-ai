# Farm Automation - MicroPython Version

Same 6-stage progression as before, rewritten in MicroPython. Pin numbers and logic are unchanged, so the README notes from the original version still apply for wiring.

## One-time setup (do this before any of the scripts will run)

1. **Install esptool** on your laptop:
   ```
   pip install esptool
   ```
2. **Download MicroPython firmware** for ESP32 from https://micropython.org/download/esp32/
3. **Erase and flash the board** (replace `<PORT>` with your board's port, e.g. COM5 or /dev/ttyUSB0):
   ```
   esptool.py --port <PORT> erase_flash
   esptool.py --port <PORT> write_flash -z 0x1000 <firmware_file.bin>
   ```
4. **Install Thonny** (https://thonny.org) - this is the easiest way to write/run MicroPython code on the board.
5. In Thonny: Tools > Options > Interpreter > select "MicroPython (ESP32)" and choose your port.
6. Open any `.py` file from this folder in Thonny and click **Run** - it executes directly on the board, no separate "upload" step needed like Arduino IDE.

## Files (same order as before)

1. `01_blink_test.py` - confirms MicroPython is flashed and running correctly
2. `02_soil_moisture_read.py` - calibrate your soil sensor's dry/wet values
3. `03_relay_pump_test.py` - confirm relay + pump wiring works
4. `04_auto_watering_logic.py` - combines sensor + pump automatically
5. `05_wifi_web_dashboard.py` - adds WiFi + live web dashboard with manual override
6. `06_rain_sensor.py` - adds rain detection, skips watering when raining

## Running a script permanently (without Thonny attached)

To make a script run automatically every time the ESP32 powers on (not just when Thonny is open), rename it to `main.py` and upload it to the board's root using Thonny's file browser (View > Files). The board will run `main.py` automatically on boot/reset.

## Note on Step 5 (web dashboard)

MicroPython doesn't have Arduino's built-in `WebServer` library, so this version uses Python's lower-level `socket` module directly. It works well at this scale but is more manual - each incoming request is read and responded to by hand rather than using route handlers.
