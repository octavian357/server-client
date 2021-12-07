import socket
import threading

class myClient():
    def __init__(self):
        self.port = 0
        self.ipaddy = ''
        self.username = ''
    
    # Connecting To Server
    def clientConnect(self, port, ipaddy, username):
        #update vars
        self.port = port
        self.ipaddy = ipaddy
        self.username = username
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ipaddy, port))

    # Listening to Server and Sending username
    def receive(self):
        while True:
            try:
                # Receive Message From Server
                # If 'NICK' Send username
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.username.encode('ascii'))
                else:
                    print(message)
            except:
                # Close Connection When Error
                print("An error occured!")
                self.client.close()
                break
            
    # Sending Messages To Server
    def write(self):
        while True:
            message = '{}: {}'.format(self.username, input(''))
            self.client.send(message.encode('ascii'))
            
    def stratClient(self):        
        # Starting Threads For Listening And Writing
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()
        
if __name__ == '__main__':    
    port = 5000
    ipaddy = '24.158.110.60'
    username = input("Choose your username: ")
    client = myClient()
    client.clientConnect(port, ipaddy, username)
    client.stratClient()