import socket
import threading
import datetime

class myServer:
    def __init__(self, host, port):
        # Connection Data
        self.host = host
        self.port = port
        self.now = datetime.datetime.now()

        # Starting Server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()

        #Get ip_address for later display
        self.hostname = socket.gethostname()
        self.local_ip = socket.gethostbyname(self.hostname)

        # Lists For Clients and Their Nicknames
        self.clients = set()
        self.nicknames = []

        #start up information
        print(f'LINK START!')
        print(f'IP Address on server is {self.local_ip}')
        print(f'{self.now}')
        print('waiting for a connection...')

    # Sending Messages To All Connected Clients
    def broadcast(self, client, message):
        print(message.decode('ascii'))
        for c in self.clients:
            if c != client:
                c.send(message)

    # Handling Messages From Clients
    def handle(self, client):
        while True:
            try:
                # Broadcasting Messages
                message = client.recv(1024)
                self.broadcast(client, message)
            except:
                # Removing And Closing Clients
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast(client, '{} left!'.format(nickname).encode('ascii'))
                self.nicknames.remove(nickname)
                break

    # Receiving / Listening Function
    def receive(self):
        while True:
            # Accept Connection
            client, address = self.server.accept()
            print("Connected with {}".format(str(address)))

            # Request And Store Nickname
            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            self.nicknames.append(nickname)
            self.clients.add(client)
            
            # Print And Broadcast Nickname
            print("Nickname is {}".format(nickname))
            self.broadcast(client, "{} joined!".format(nickname).encode('ascii'))
            client.send('Connected to server!'.encode('ascii'))

            # Start Handling Thread For Client
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    #send messages to client
    def write(self):
        while True:
            inp = input()
            message = f'Server: {inp}'
            for c in self.clients:
                c.send(message.encode('ascii')) 
                break

    def startServer(self):
        thread = threading.Thread(target=self.receive)
        thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()
 
if __name__ == '__main__':     
    host = '192.168.0.124'
    port = 5000
    server = myServer(host, port)
    server.startServer()