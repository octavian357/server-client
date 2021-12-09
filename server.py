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

        # Lists For Clients and Their usernames
        self.clients = {}
        #self.usernames = []

        #start up information
        print(f'LINK START!')
        print(f'IP Address on server is {self.local_ip}')
        print(f'{self.now}')
        print('waiting for a connection...')

    # Sending Messages To All Connected Clients
    def broadcast(self, client, message):
        print(message.decode('ascii'))
        #print(len(self.clients))
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
                print('in except')
                #index = self.clients.index(client)
                username = self.clients[client]
                self.clients.pop(client)
                client.close()
                #self.username = self.usernames[index]
                
                self.broadcast(client, '{} left!'.format(username).encode('ascii'))
                #self.usernames.remove(username)
                break

    # Receiving / Listening Function
    def receive(self):
        while True:
            # Accept Connection
            client, address = self.server.accept()
            print("Connected with {}".format(str(address)))

            # Request And Store username
            client.send('NICK'.encode('ascii'))
            username = client.recv(1024).decode('ascii')
            
            #self.usernames.append(username)
            #self.clients.add(client)
            self.clients[client] = username
            # Print And Broadcast username
            #print("username is {}".format(username))
            self.broadcast(client, "{} joined the chat!".format(username).encode('ascii'))
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
        #self.receive()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()
 
if __name__ == '__main__':     
    host = ''
    port = 5000
    server = myServer(host, port)
    server.startServer()