import socket
import lib
import json


def call_func(d, args):
    if len(args) != 2:
        raise TypeError ('Invalid input format')
    func, params = args[0], args[1]
    if type(func) != str or type(params) != list:
        raise TypeError('Invalid input format')
    if not hasattr(d, func):
        raise NameError ('Undefined function name')
    for i, p in enumerate(params):
        if type(p) == list:
            params[i] = lib.unit(*p)
    return getattr(d, func)(*params)


def main():
    print('Starting server...', end='', flush=True)
    SERVER_ADDRESS = ('localhost', 8686)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(10)
    d = lib.Db()

    print('\rServer is running, press ctrl+c to stop ')
    while True:
        connection, address = server_socket.accept()
        print(f'\nNew connection from {address}')
        data = connection.recv(1024)
        print(f'Request: {data}')
        try:
            res = call_func(d, json.loads(data))
            if res is None:
                res = bytes('ok', encoding='UTF-8')
                print(f'Response: {res}')
                connection.send(res)
            else:
                res = bytes(json.dumps(res), encoding='UTF-8')
                print(f'Response: {res}')
                connection.send(res)
        except Exception as e:
            print(f'Exception on connection {address}: {e}')
            res = bytes(f'Error: {e}', encoding='UTF-8')
            print(f'Response: {res}')
            connection.send(res)
        connection.close()


main()
