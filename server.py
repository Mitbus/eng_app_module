import socket
import lib
import json

print('Starting server...', end='\r')
SERVER_ADDRESS = ('localhost', 8686)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.listen(10)

d = lib.Db()
print('Server is running,\npress ctrl+c to stop')
while True:
    connection, address = server_socket.accept()
    print(f'New connection from {address}')

    data = connection.recv(1024)
    data = json.loads(str(data))
    print(data)

    connection.send(bytes('Hello from server!', encoding='UTF-8'))

    connection.close()