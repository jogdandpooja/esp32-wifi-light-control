Option 3: Allow microphone for HTTP during testing

For local development only:

1]Open Chrome.

2]Go to chrome://flags/#unsafely-treat-insecure-origin-as-secure

3]Enable Insecure origins treated as secure.

4]Enter your HTTP website URL, for example:
http://192.168.1.10:3000

5]Relaunch Chrome.

ESP32 Wi-Fi Light Control with Voice Commands

Control a 230V AC bulb from your phone using an ESP32, a relay module and MicroPython. Open a web page served by the ESP32, then tap ON / OFF or use voice commands.

Features
Web page hosted on the ESP32 (works on any phone or laptop on the same Wi-Fi)
ON / OFF buttons with live status
Voice control in the browser ("on", "off") in English, Hindi and Marathi
Separate files for the page (index.html) and the logic (main.py)
Wi-Fi details kept in a separate file that is not pushed to GitHub
Hardware
Part	Notes
ESP32 DevKit	USB-C or micro-USB, with MicroPython installed
1-channel 5V relay module	e.g. SRD-05VDC, 10A 250VAC
Bulb holder + bulb	230V AC bulb (B22 or E27)
Mains plug with 2-core wire	live and neutral
Jumper wires, insulation tape or a plastic box	
Wiring
Low-voltage side (ESP32 to relay)
ESP32 pin	Relay pin
VIN (5V)	VCC
GND	GND
D26 (GPIO 26)	IN
Mains side (230V AC) - disconnect power before wiring
Plug live    -> relay COM (middle terminal)
Relay NO     -> bulb holder terminal 1
Bulb holder terminal 2 -> plug neutral

Only the live wire goes through the relay. Neutral goes straight from the plug to the bulb holder.

Safety: mains voltage can seriously hurt you. Unplug everything before wiring, keep the mains side off the breadboard, cover all bare copper, and put the relay in a plastic box. If you are not experienced with mains wiring, ask a qualified person to check it before powering on.

Project files
File	Purpose
main.py	Wi-Fi, relay control and web server (runs on the ESP32)
index.html	Web page with ON/OFF buttons and voice control
wifi_config.example.py	Template for your Wi-Fi details
wifi_config.py	Your real Wi-Fi details (create it yourself, ignored by Git)
Setup
Copy wifi_config.example.py to wifi_config.py and enter your Wi-Fi name and password. The ESP32 only supports 2.4GHz Wi-Fi.
Close Thonny or any other program using the ESP32's serial port.
Install mpremote:
python -m pip install mpremote
Find your port:
python -m mpremote connect list
Upload the files (replace COM5 with your port):
python -m mpremote connect COM5 fs cp main.py :main.py
python -m mpremote connect COM5 fs cp index.html :index.html
python -m mpremote connect COM5 fs cp wifi_config.py :wifi_config.py
Run it:
python -m mpremote connect COM5 run main.py

The terminal prints Connected! Open this on your phone: http://<ip-address>.

To start automatically on power-up, reset the board (python -m mpremote connect COM5 reset). main.py runs by itself whenever the ESP32 gets power.

You can also upload the files with Thonny (File -> Save as -> MicroPython device) if you prefer.

Usage
Make sure your phone is on the same Wi-Fi as the ESP32.
Open the printed address in Chrome.
Tap ON or OFF.
Voice control
Tap Start voice, choose a language and allow the microphone.
Say "on" or "off" (Hindi and Marathi words like "चालू" and "बंद" also work).

Voice recognition runs in the browser and needs an internet connection on the phone. Because the page uses http://, Chrome may block the microphone. To allow it, open chrome://flags/#unsafely-treat-insecure-origin-as-secure, add your ESP32 address (for example http://192.168.1.61), set it to Enabled and relaunch Chrome.

Troubleshooting
Problem	Fix
ENOENT error	index.html is not on the board. Upload it again.
ImportError: wifi_config	wifi_config.py is missing on the board or named wrongly.
failed to access COM5	Another program is using the port. Close Thonny and other serial tools.
Wi-Fi connection failed	Check the SSID spelling and password, and use a 2.4GHz network.
Relay works backwards	Set ACTIVE_LOW = False in main.py, or move the wire to the other outer relay terminal.
Relay clicks but the bulb is off	Check the holder wiring, the COM/NO terminals, tight screws, and that the bulb works.
Relay never clicks	Check VIN to VCC, GND to GND and D26 to IN.

