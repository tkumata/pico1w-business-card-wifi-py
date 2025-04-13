from log.debug import DebugHandler


class DnsHandler:
    # Load HTML File
    def load_html(self, filename):
        try:
            with open(filename, "r") as f:
                return f.read()
        except Exception as e:
            return f"<h1>Error loading file: {e}</h1>"

    # DNS Server
    def handle_request(self, dns, ip):
        try:
            debug = DebugHandler("DNS")

            data, addr = dns.recvfrom(512)
            if not data:
                return
            debug.dprint("Request from", addr)

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
