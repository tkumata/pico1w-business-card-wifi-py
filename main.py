import network
import socket
import time
import secrets
from machine import SPI, Pin
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

# Init Wi-Fi as AP mode
ap = network.WLAN(network.AP_IF)
ap.config(essid=secrets.SSID, password=secrets.PASSWORD)
ap.active(True)
while not ap.active():  # Waiting for active
    pass
ip = ap.ifconfig()[0]
print("AP started:", ip)

# DNS Socket (UDP)
dns = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dns.bind(('0.0.0.0', 53))
dns.setblocking(False)

# HTTP Socket (TCP)
http = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
http.bind(('0.0.0.0', 80))
http.listen(5)
http.setblocking(False)

# Dispaly AP Info
display.text("下記APに接続し、何もせず", 0, 0, COLORS["MAGENTA"], size=1)
display.text("そのままお待ちください", 0, 10, COLORS["MAGENTA"], size=1)
display.text("SSID:", 0, 30, COLORS["WHITE"], size=1)
display.text("{}".format(secrets.SSID), 0, 40, COLORS["CYAN"], size=2)
display.text("PASS:", 0, 60, COLORS["WHITE"], size=1)
display.text("{}".format(secrets.PASSWORD), 0, 70, COLORS["CYAN"], size=2)
display.show()


# Load HTML File
def load_html(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except Exception as e:
        return f"<h1>Error loading file: {e}</h1>"


# DNS Server
def dns_server(sock, ip):
    try:
        data, addr = sock.recvfrom(512)
        if not data:
            return
        print("DNS request from", addr)
        transaction_id = data[0:2]
        flags = b'\x81\x80'
        qdcount = data[4:6]
        ancount = qdcount
        nscount = b'\x00\x00'
        arcount = b'\x00\x00'
        dns_header = transaction_id + flags + qdcount + ancount + nscount + arcount
        query = data[12:]
        answer = b'\xc0\x0c' + b'\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'
        answer += bytes(map(int, ip.split('.')))
        dns_response = dns_header + query + answer
        sock.sendto(dns_response, addr)
    except OSError:
        pass


# HTTP Server
def http_server(sock):
    try:
        client, addr = sock.accept()
        print("HTTP request from", addr)
        request = client.recv(1024).decode()
        print("Request:", request)
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + load_html('namecard.html')
        client.send(response.encode())
        client.close()
    except OSError:
        pass


# Main Loop
while True:
    dns_server(dns, ip)
    http_server(http)
    time.sleep(0.001)
