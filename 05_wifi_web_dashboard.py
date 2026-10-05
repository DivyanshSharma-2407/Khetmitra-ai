"""
STEP 5: WiFi Web Dashboard (MicroPython)
--------------------------------------------
Purpose: Connect to WiFi, host a simple web page showing live soil
readings, with manual pump on/off buttons. Keeps automatic watering
running in the background unless manually overridden.

BEFORE RUNNING:
1. Update WIFI_SSID and WIFI_PASSWORD below.
2. Make sure DRY_THRESHOLD matches your calibration.

HOW TO USE:
1. Run this script in Thonny (or save as main.py on the board to run
   automatically on power-up).
2. It will print an IP address once connected - e.g. "Connected!
   IP address: 192.168.1.42"
3. On any device on the same WiFi, open a browser and go to that IP.
4. You'll see live readings and pump control buttons.

NOTE: MicroPython's built-in 'socket' module is used here instead of
a web framework, since MicroPython doesn't include Arduino's
WebServer library. It's more manual, but works well for this scale.
"""

import network
import socket
from machine import Pin, ADC
import time

WIFI_SSID = "YOUR_WIFI_NAME"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

SOIL_PIN = 34
RELAY_PIN = 26
DRY_THRESHOLD = 2200

AUTO_CHECK_INTERVAL_S = 10

soil_adc = ADC(Pin(SOIL_PIN))
soil_adc.atten(ADC.ATTN_11DB)

relay = Pin(RELAY_PIN, Pin.OUT)
relay.value(1)  # Pump starts OFF

pump_manual_override = False
last_auto_check = time.time()


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    print("Connecting to WiFi...")
    while not wlan.isconnected():
        time.sleep(0.5)
        print(".", end="")

    print("")
    print("Connected! IP address:", wlan.ifconfig()[0])
    return wlan.ifconfig()[0]


def build_page():
    soil_value = soil_adc.read()
    is_dry = soil_value > DRY_THRESHOLD
    status = "DRY" if is_dry else "Moist enough"

    html = """<html><head><title>Farm Automation Dashboard</title>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<meta http-equiv='refresh' content='5'>
<style>body{{font-family:sans-serif;text-align:center;padding-top:40px;}}
button{{font-size:18px;padding:12px 24px;margin:10px;}}</style></head><body>
<h1>Farm Automation Dashboard</h1>
<p>Soil moisture raw value: <b>{soil}</b></p>
<p>Status: <b>{status}</b></p>
<a href='/pump/on'><button>Pump ON</button></a>
<a href='/pump/off'><button>Pump OFF</button></a>
<p style='color:gray'>Page auto-refreshes every 5 seconds.</p>
</body></html>""".format(soil=soil_value, status=status)

    return html


def handle_request(request):
    global pump_manual_override

    if "/pump/on" in request:
        relay.value(0)  # Pump ON
        pump_manual_override = True
        return "REDIRECT"
    elif "/pump/off" in request:
        relay.value(1)  # Pump OFF
        pump_manual_override = False
        return "REDIRECT"
    else:
        return build_page()


ip_address = connect_wifi()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)
s.settimeout(0.2)  # Non-blocking-ish, so we can also run auto-watering logic

print("Web server started at http://" + ip_address)

while True:
    # --- Handle web requests ---
    try:
        conn, addr = s.accept()
        request = conn.recv(1024).decode()

        result = handle_request(request)

        if result == "REDIRECT":
            conn.send("HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n")
        else:
            conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
            conn.send(result)

        conn.close()
    except OSError:
        pass  # No incoming request this cycle - normal, keep looping

    # --- Automatic watering logic (runs unless manually overridden) ---
    if not pump_manual_override and (time.time() - last_auto_check) > AUTO_CHECK_INTERVAL_S:
        last_auto_check = time.time()
        soil_value = soil_adc.read()

        if soil_value > DRY_THRESHOLD:
            print("Auto-watering triggered.")
            relay.value(0)
            time.sleep(3)
            relay.value(1)
