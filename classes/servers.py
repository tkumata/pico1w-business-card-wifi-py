from classes.debug import Debug


class Servers:
    # def __init__(self):
    # self.dns = dns
    # self.http = http

    # Load HTML File
    def load_html(self, filename):
        try:
            with open(filename, "r") as f:
                return f.read()
        except Exception as e:
            return f"<h1>Error loading file: {e}</h1>"

    # DNS Server
    def dns_server(self, dns, ip):
        try:
            debug = Debug("DNS")

            data, addr = dns.recvfrom(512)
            if not data:
                return
            debug.dprint("DNS request from", addr)

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

            dns.sendto(dns_response, addr)
        except OSError:
            pass

    # HTTP Server
    def http_server(self, http):
        try:
            debug = Debug("HTTP")

            client, addr = http.accept()
            debug.dprint("HTTP request from", addr)
            client.recv(1024).decode()
            response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + \
                self.load_html('../presentations/businesscard.html')

            client.send(response.encode())
            client.close()
        except OSError:
            pass
