import socket
import os


HOST = "80.92.115.97"
PORT = 43293

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")


while True:
    file_list: str = client.recv(1024).decode()
    print(file_list)
    action, file_name = input("Choose an action: ").split(" ", 1)

    if action == "upload":
        if not os.path.isfile(file_name):
            print("File doesn't exist.")
            continue

        with open(file_name, "rb") as file:
            content: bytes = file.read()

        client.sendall(f"{action} {file_name}".encode())

        data_length = len(content)
        client.sendall(f"{data_length}".encode().ljust(10))

        response = client.recv(1024)
        print(response.decode())
        client.sendall(content)


client.close()
