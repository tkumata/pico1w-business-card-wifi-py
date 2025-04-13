from log.debug import DebugHandler


class HttpHandler:
    # Load HTML File
    def load_html(self, filename):
        try:
            with open(filename, "r") as f:
                return f.read()
        except Exception as e:
            return f"<h1>Error loading file: {e}</h1>"

    # HTTP Server
    def handle_request(self, http):
        try:
            debug = DebugHandler("HTTP")

            client, addr = http.accept()
            debug.dprint("Request from", addr)
            client.recv(1024).decode()
            response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + \
                self.load_html('../presentation/businesscard.html')

            client.send(response.encode())
            client.close()
        except OSError:
            pass
