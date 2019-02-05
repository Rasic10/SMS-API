from socket import *
from threading import *


class ClientHandler(Thread):
    def __init__(self, clientSocket, clientAddress, clientUsername):
        self.sock = clientSocket
        self.address = clientAddress
        self.username = clientUsername

        clients.append(self)
        super().__init__()
        self.start()

    def run(self):
        print('<{}> has connected!'.format(self.username))

        while True:
            try:
                text = self.sock.recv(4096).decode()
                send_to_client = '<{}> {}'.format(self.username, text)
                print('<{}> {}'.format(self.username, text))

                for client in clients:
                    if self != client:
                        client.sock.send(send_to_client.encode())

            except ConnectionResetError:
                dc_message = 'User {} has disconnected'.format(self.username)
                print(dc_message)
                clients.remove(self)
                for client in clients:
                    client.sock.send(dc_message.encode())
                self.sock.close()
                break

serverAddress = '192.168.10.101'
serverPort = 11111

clients = []

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind((serverAddress, serverPort))
serverSocket.listen(5)
print('Server is ready to accept new connections!')

while True:
    clientSocket, clientAddress = serverSocket.accept()
    clientUsername = clientSocket.recv(4096).decode()
    client = ClientHandler(clientSocket, clientAddress, clientUsername)