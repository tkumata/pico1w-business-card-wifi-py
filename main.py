import secrets
import socket
import time

import network
from machine import SPI, Pin

from classes.servers import Servers
from ssd1351 import SSD1351

# Define Color
COLORS = {
    "BLACK": 0,
    "WHITE": 0xFFFF,
    "RED": 0xF800,
    "GREEN": 0x07E0,
    "BLUE": 0x001F,
    "YELLOW": 0xFFE0,
    "CYAN": 0x07FF,
    "MAGENTA": 0xF81F,
}

# Init SPI
spi = SPI(0, baudrate=10000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))
dc = Pin(16, Pin.OUT)
cs = Pin(20, Pin.OUT)
rst = Pin(17, Pin.OUT)

# Init SSD1351 OLED Display
display = SSD1351(128, 128, spi, dc, cs, rst)

# Init objects
servers = Servers()

# DNS Socket (UDP)
dns = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dns.bind(('0.0.0.0', 53))
dns.setblocking(False)

# HTTP Socket (TCP)
http = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
http.bind(('0.0.0.0', 80))
http.listen(3)
http.setblocking(False)

# Init Wi-Fi as AP mode
ap = network.WLAN(network.AP_IF)
ap.config(essid=secrets.SSID, password=secrets.PASSWORD)
ap.active(True)
while not ap.active():  # Waiting for active
    pass
ip = ap.ifconfig()[0]

# Dispaly AP Info
display.text("下記APに接続し、何もせず", 0, 0, COLORS["MAGENTA"], size=1)
display.text("そのままお待ちください.", 0, 10, COLORS["MAGENTA"], size=1)
display.text("SSID:", 0, 30, COLORS["WHITE"], size=1)
display.text("{}".format(secrets.SSID), 0, 40, COLORS["CYAN"], size=1)
display.text("PASS:", 0, 50, COLORS["WHITE"], size=1)
display.text("{}".format(secrets.PASSWORD), 0, 60, COLORS["CYAN"], size=2)
display.show()


# Main Loop
while True:
    servers.dns_server(dns, ip)
    servers.http_server(http)
    time.sleep(0.001)
