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


class ServerConnection():
    def __init__(self, src, dest) -> None:
        self.socket = (src, dest)
        # 0 = not done, 1 = stage one done, 2 = stage 2 done, 3 = 3 way handshake complete
        self.handshake = 0
        self.ongoing = False

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, ServerConnection) and hash(self.socket) == hash(__value.socket)

    def handle(self, header):
        if self.handshake < 3:
            if ServerConnection.check_handshake(header) == self.handshake+1:
                self.handshake += 1
                return 1  # success
            else:
                print('Error in handshake')
                return -1

    def check_handshake(header):
        if header.SYN and header.ACK:
            return 2
        if header.SYN:
            return 1
        if header.ACK:
            return 3

    def send(self, message):
        # confirm connection
        # split message into n sized packets
        # select a rdt scheme to use and implement
        # create header for each packet
        # send packets
        pass

    def receive(self, message):
        # interpret message
        pass

    def close(self):
        pass



if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
