from socket import *
from threading import *
import urllib.request
import urllib.parse

def sendSMS(numbers, sender, message):
    data = urllib.parse.urlencode({'apikey': 'j/zjDwKhoa0-wcnOV52ZMPkse6PMEl4281jOt172Ey', 'numbers': numbers, 'message': message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.txtlocal.com/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return (fr)

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

                if text[0] == '#':
                    message = text[1:].split('-')
                    print(message)
                    print(numbers[message[0]] + " " + message[1] + " " + message[2])
                    resp = sendSMS(numbers[message[0]], message[1], message[2])
                    print(resp)
                    print('Poruka poslata!')

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

serverAddress = 'localhost'
serverPort = 11111

clients = []
numbers = {'Sara': '381644484252', 'Ana': '381644513163', 'Nemanja': '381641650346'}

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind((serverAddress, serverPort))
serverSocket.listen(5)
print('Server is ready to accept new connections!')

while True:
    clientSocket, clientAddress = serverSocket.accept()
    clientUsername = clientSocket.recv(4096).decode()
    client = ClientHandler(clientSocket, clientAddress, clientUsername)