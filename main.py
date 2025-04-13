import secrets
import socket
import time

import network
from machine import SPI, Pin

from domain.dns import DnsHandler
from domain.http import HttpHandler
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
dns_handler = DnsHandler()
http_handler = HttpHandler()

# DNS Socket (UDP)
dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dns_socket.bind(('0.0.0.0', 53))
dns_socket.setblocking(False)

# HTTP Socket (TCP)
http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
http_socket.bind(('0.0.0.0', 80))
http_socket.listen(5)
http_socket.setblocking(False)

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
    dns_handler.handle_request(dns_socket, ip)
    http_handler.handle_request(http_socket)
    time.sleep(0.001)
