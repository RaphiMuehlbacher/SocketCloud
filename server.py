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
            self.request.sendall(self.files_list().encode())

        while True:
            self.data: str = self.request.recv(1024).strip().decode()
            if not self.data:
                break
            print(f"Received from {self.ip} action: {self.data}")

            action, file_name = self.data.split(" ", 1)
            if action == "upload":
                self.upload_name(file_name)
                self.request.sendall(f"File created: {os.path.join(self.ip, file_name)}".encode())
                self.upload_content(file_name)
            elif action == "download":
                self.download(file_name)
            else:
                self.request.sendall("Unknown command!".encode())

    def files_list(self):
        files = os.listdir(self.ip)
        str_files = ""
        for file in files:
            str_files += file + "\n"
        return str_files

    def upload_name(self, file_name: str):
        with open(os.path.join(self.ip, file_name), "wb") as file:
            print(f"File created: {os.path.join(self.ip, file_name)}")

    def upload_content(self, file_name):
        print("Started writing content")
        data = b""
        data_length = int(self.request.recv(10).strip())
        print(f"Data lengh: {data_length}")
        while len(data) < data_length:
            data += self.request.recv(1024)

        print(f"Data in bytes: {data}")
        with open(os.path.join(self.ip, file_name), "wb") as file:
            file.write(data)
        print("File uploaded")

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

