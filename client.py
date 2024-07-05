import socket
import threading

HOST = "127.0.0.1"
PORT = 9000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

message = input(" -> ")  # take input

while message.lower().strip() != 'bye':
    client.send(message.encode())  # send message
    data = client.recv(1024).decode()  # receive response
    print('Received from server: ' + data)  # show response

    message = input(" -> ")  # again take input

client.close()  # close the connection
