# ESP32 Wi-Fi relay control (MicroPython)
# Uses a separate index.html file for the web page.
import network
import socket
import time
from machine import Pin

# ---------- SETTINGS ----------
from wifi_config import SSID, PASSWORD   # Wi-Fi details are kept in wifi_config.py
RELAY_PIN = 26              # GPIO connected to relay IN pin
ACTIVE_LOW = True           # Set to False if your relay works the opposite way
HTML_FILE = "index.html"
# ------------------------------

OFF_LEVEL = 1 if ACTIVE_LOW else 0
ON_LEVEL = 0 if ACTIVE_LOW else 1

# Start already OFF so the bulb doesn't flash on boot
relay = Pin(RELAY_PIN, Pin.OUT, value=OFF_LEVEL)
state = False


def set_relay(on):
    relay.value(ON_LEVEL if on else OFF_LEVEL)


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        timeout = 20
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    if not wlan.isconnected():
        raise RuntimeError("Wi-Fi connection failed. Check SSID/PASSWORD and use a 2.4GHz network.")
    ip = wlan.ifconfig()[0]
    print("Connected! Open this on your phone: http://" + ip)
    return ip


def load_template():
    # Read the HTML file from the ESP32's storage
    with open(HTML_FILE, "r") as f:
        return f.read()


def web_page():
    status = "ON" if state else "OFF"
    color = "#2e9e44" if state else "#c0392b"
    html = load_template()
    html = html.replace("%STATUS%", status)
    html = html.replace("%COLOR%", color)
    return html


ip = connect_wifi()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", 80))
s.listen(5)

while True:
    conn = None
    try:
        conn, addr = s.accept()
        conn.settimeout(3)
        request = conn.recv(1024).decode()
        first_line = request.split("\r\n")[0] if request else ""

        if "GET /on" in first_line:
            state = True
            set_relay(True)
        elif "GET /off" in first_line:
            state = False
            set_relay(False)

        response = web_page()
        conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n")
        conn.sendall(response)
    except Exception as e:
        print("Error:", e)
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass
