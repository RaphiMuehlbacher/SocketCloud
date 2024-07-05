import socketserver
import os

HOST = "172.16.254.101"
PORT = 43293


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.ip = self.client_address[0]
        print(f"{self.ip} connected to the server")

        if not os.path.isdir(self.ip):
            os.mkdir(self.ip)
            self.request.sendall("You have no files".encode())
        else:
            self.send_files_list()

        while True:
            self.data: str = self.request.recv(1024).strip().decode()
            if not self.data:
                break
            print(f"Received from {self.ip} action: {self.data}")

            action, file_name = self.data.split(" ", 1)
            if action == "upload":
                self.upload_file(file_name)
            elif action == "download":
                self.download(file_name)
            else:
                self.request.sendall("Unknown command!".encode())

    def send_files_list(self):
        files = os.listdir(self.ip)
        if files:
            file_list = "\n".join(files)
            self.request.sendall(file_list.encode())
        else:
            self.request.sendall("You have no files stored".encode())

    def upload_file(self, file_name):
        self.request.sendall(f"File created: {os.path.join(self.ip, file_name)}".encode())

        with open(os.path.join(self.ip, file_name), "wb") as file:
            data = b""
            while True:
                new_data = self.request.recv(1024)
                if not new_data:
                    break
                data += new_data
            file.write(data)
        print(f"File uploaded: {os.path.join(self.ip, file_name)}")

    def download(self, file_name: str):
        pass


def main():
    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        print(f"Server starting on {HOST}:{PORT}")
        print(f"Clients should connect to {HOST}:{PORT}")
        print(f"This will keep running until you interrupt the program with Ctrl-C")
        server.serve_forever()


if __name__ == "__main__":
    main()
