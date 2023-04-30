import socketserver
import socket
from host import Connection
from HTTPClient import *


SERVER = ('localhost', 9999)


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def setup(self):
        # Connection between gateway and UDP server
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.con = Connection(sock, SERVER)
        self.client = HTTPClient(self.con)

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        split = self.data.decode().split('\\r\\n')
        splitsplit = split[0].split()
        self.method = splitsplit[0]
        self.path = splitsplit[1]
        print("{}, {} wrote:".format(
            self.client_address[0], self.client_address[1]))
        print(self.data)
        print('Method: {}'.format(self.method))
        if self.method == 'GET':
            response = self.client.get(self.path)
            print('Sending: \n{}'.format(response))
            self.request.sendall(response.encode())
        elif self.method == 'POST':
            data = self.data.split("keep-alive\r\n")
            self.client.post(self.path, data)
        else:
            print('Unknown method')


if __name__ == "__main__":
    HOST, PORT = "localhost", 9900

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
