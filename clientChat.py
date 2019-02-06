from socket import *
from time import sleep
from threading import *

class ListenThread(Thread):
    def __init__(self, socket):
        self.sock = socket
        super().__init__()
        self.start()

    def run(self):
        print('You are connected!\n')
        while True:
            print(self.sock.recv(4096).decode())

srv_address = 'localhost'
srv_port = 11111

username = input('Enter your username: ')

while True:
    try:
        socket = socket(AF_INET, SOCK_STREAM)
        socket.connect((srv_address, srv_port))
    #    print('Connected to {} on port {}'.format(srv_address, srv_port))
        socket.send(username.encode())
        listener = ListenThread(socket)
        break
    except:
        print('Unable to connect to the server')
        print('Retrying in 5 seconds...')
        sleep(5)

while True:
    message = input()
    socket.send(message.encode())