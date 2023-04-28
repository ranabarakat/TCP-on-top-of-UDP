import socketserver
from TCP import *
import random

HOST, PORT = "localhost", 9999


class MyUDPHandler(socketserver.BaseRequestHandler):
    connections = []
    current_connection = None

    def setup(self):
        i = 0
        for conn in MyUDPHandler.connections:
            if conn.socket == self.request[1]:
                MyUDPHandler.current_connection = conn
                i+=1
        if i == len(MyUDPHandler.connections):
            serv = ServerConnection(self.request[1],self.client_address)
            MyUDPHandler.connections.append(serv)
            MyUDPHandler.current_connection = serv

        
        

    def handle(self):
        self.msg = self.request[0].strip()
        MyUDPHandler.current_connection.receive(self.msg)
        # self.current_connection.handshake(self.header)
        # self.split_header_contents()
        # CHECK WHICH CONNECTION
        # socket = self.request[1]
        # print("{}, {} wrote:".format(self.client_address[0],self.client_address[1]))
        # print('current object counter: {}'.format(self.counter))
        # print(data)
        # socket.sendto(data.upper(), self.client_address)


class ServerConnection():
    
    def __init__(self, sock,client) -> None:
        self.socket = sock
        self.client_address=client
        self.connected = False
        self.state = 'CLOSED'
        self.recv_seq_num = 0
        self.packet_to_transmit = 0  # current packet up for transmission
        self.packets = []
        self.seq_num = random.randint(0, 9999)
        self.n = 32  # each packet consists of 32-byte payload + 32-byte header
        self.payload_bits = None
        self.header_bits = None
        self.closing = False


    # def __eq__(self, __value: object) -> bool:
    #     return isinstance(__value, ServerConnection) and hash(self.socket) == hash(__value.socket)

    # def check_handshake(header):
    #     if header.SYN and header.ACK:
    #         return 2
    #     if header.SYN:
    #         return 1
    #     if header.ACK:
    #         return 3
        
    def handshake(self):
        if self.state == 'CLOSED':
            # received = self.socket.recv(1024)
            if self.header.SYN:
                header = TCPHeader(seq_num=self.seq_num, ack_num=self.recv_seq_num+1,
                                SYN=1, ACK=1)
                self.socket.sendto(header.get_header(), self.client_address)
                self.state = 'SYN-ACK'

        elif self.state == 'SYN-ACK':
            if self.header.ACK:
                self.state = 'CONNECTED'
                self.seq_num += 1
                self.connected = True


    def send(self, message):
        # confirm connection
        # split message into n sized packets
        # select a rdt scheme to use and implement
        # create header for each packet
        # send packets
        pass

    def receive(self, message):
        # interpret message
        header = message[:32]  # take first 29 bytes for header
        self.header_bits = ''.join(format(i, '08b') for i in header)  # convert header to binary
        self.payload_bits = ''.join(format(i, '08b') for i in message[32:])
        self.header = TCPHeader()
        self.header.set_header(self.header_bits)
        self.recv_seq_num = self.header.seq_num
        # self.n = len(message[32:])

        if self.header.FIN:
            self.closing = True

        if not self.connected :
            self.handshake()

        elif self.closing:
            self.close()

        else:
            if self.header.ACK == 1 and self.header.ack_num == self.seq_num+self.n:
                self.recv_seq_num = self.header.seq_num
                self.packet_to_transmit += 1
                self.seq_num += self.n


    def close(self):
        # receive fin
        # send fin ack
        # receive ack
        # success
        if self.state == 'CONNECTED':
           if self.header.FIN:
                header = TCPHeader(seq_num=self.seq_num, ack_num=self.recv_seq_num+1, ACK=1, FIN=1)
                self.socket.sendto(header.get_header(), self.client_address)
                self.state = 'FIN-ACK'

        elif self.state == 'FIN-ACK':
            if self.header.ACK:
                self.state = 'CLOSED'
                self.connected = False



if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
