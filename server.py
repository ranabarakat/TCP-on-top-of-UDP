import socketserver
from TCP import *

HOST, PORT = "localhost", 9999


class MyUDPHandler(socketserver.BaseRequestHandler):
    connections = []

    def split_header_contents(self):
        # APPROACH 1

        # res = ''.join(format(i, '08b') for i in self.msg) # convert message to binary
        # header = res[:232] # take first 29 bytes for header
        # content = self.msg[232:] # rest is message
        # content = [content[i:i+8] for i in range(0, len(content), 8)] # split message to bytes
        # self.content = ''.join(chr(int(i,2)) for i in content) # convert message back to string

        # APPROACH 2

        header = self.msg[:29]  # take first 29 bytes for header
        self.content = self.msg[29:]  # rest is message
        header = ''.join(format(i, '08b')
                         for i in header)  # convert header to binary

        self.header = TCPHeader(header)

    def setup(self):
        self.current_connection = ServerConnection(
            self.request[1], (HOST, PORT))
        try:
            idx = MyUDPHandler.connections.index(self.current_connection)
            self.current_connection = MyUDPHandler[idx]
        except:
            print('New connection found')
            MyUDPHandler.connections.append(self.current_connection)

    def handle(self):
        self.msg = self.request[0].strip()
        self.split_header_contents()
        self.current_connection.handle(self.header)
        # self.split_header_contents()
        # CHECK WHICH CONNECTION
        # socket = self.request[1]
        # print("{}, {} wrote:".format(self.client_address[0],self.client_address[1]))
        # print('current object counter: {}'.format(self.counter))
        # print(data)
        # socket.sendto(data.upper(), self.client_address)

    def send(self):
        pass


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
