import socketserver

HOST = "127.0.0.1"
PORT = 9000


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            self.data: bytes = self.request.recv(1024).strip()
            if not self.data:
                break
            print(f"Received from {self.client_address[0]} wrote: {self.data.decode()}")
            self.request.sendall(self.data.upper())



def main():
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print(f"Server starting on {HOST}:{PORT}")
        print(f"Clients should connect to {HOST}:{PORT}")
        print(f"This will keep running until you interrupt the program with Ctrl-C")
        server.serve_forever()
