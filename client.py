import socket
import random
from TCP import *


HOST, PORT = "localhost", 9999
# data = " ".join(sys.argv[1:])
data = 'hello world@1'

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().

#sock.sendto(bytes(data + "\n", "utf-8"), (HOST, PORT))
#received = str(sock.recv(1024), "utf-8")

#print("Sent:     {}".format(data))
#print("Received: {}".format(received))

# TODO
# connection.connect()
# connection.send()
# connection.disconnect()

# connect(): start 3 way handshake


class ClientConnection():
    def __init__(self, sock, dest) -> None:
        self.socket = sock
        self.dest = dest
        self.connected = False
        self.state = 'CLOSED'
        self.recv_seq_num = 0
        self.packet_to_transmit = 0  # current packet up for transmission
        self.packets = []
        self.seq_num = random.randint(0,9999)
        self.n = 32  # each packet consists of 32-byte payload + 32-byte header
    # def create_header(self, message):
        # pass

    def handshake(self):
        # send syn
        # receive syn ack
        # send ack
        # success
        if self.state == 'CLOSED':
            # create a header with SYN flag only
            header = TCPHeader(seq_num=self.seq_num, ack_num=0,
                               SYN=1, ACK=0, FIN=0)
            # self.seq_num += 1
            # header_tmp = ''.join(format(i, '08b')
            #              for i in header.get_header())  # convert header to binary
            # print('sending: {}'.format(header_tmp))
            self.socket.sendto(header.get_header(), self.dest)
            self.state = 'SYN'

        elif self.state == 'SYN':
            received = self.socket.recv(1024)
            received = ''.join(format(i, '08b')
                         for i in received)  # convert header to binary
            header = TCPHeader()
            header.set_header(received)
            if header.ACK == 1 and header.SYN == 1:
                self.state = 'SYN-ACK'
                self.recv_seq_num = header.seq_num
                self.seq_num += 1

        elif self.state == 'SYN-ACK':
            header = TCPHeader(seq_num=self.seq_num, ack_num=self.recv_seq_num+1,
                               SYN=0, ACK=1, FIN=0)
            self.socket.sendto(header.get_header(), self.dest)
            self.state = 'ACK'
            self.seq_num += 1
            # TODO
            # make sure ack was received before setting connnected = true
            self.connected = True

    def parse_msg(self, message):
        # parse message
        payloads = [message[i:i+self.n].encode()
                    for i in range(0, len(message), self.n)]
        return payloads

    def send(self, message):
        # confirm connection
        # split message into n sized packets
        # select a rdt scheme to use and implement
        # create header for each packet
        # send packets
        payloads = self.parse_msg(message)
        if self.connected:
            header = TCPHeader(
                seq_num=self.seq_num, ack_num=self.recv_seq_num+self.n, ACK=1)
            packet = header.get_header() + payloads[self.packet_to_transmit]
            self.packets.append(packet)
            self.socket.sendto(packet, self.dest)
            # self.seq_num += self.n
            # self.packet_to_transmit += 1

    def receive(self):
        # interpret message
        if self.connected:
            received = str(self.socket.recv(1024), "utf-8")
            header = TCPHeader()
            header.set_header(received)
            if header.ACK == 1 and header.ack_num == self.seq_num+self.n:
                self.recv_seq_num = header.seq_num
                self.packet_to_transmit += 1
                self.seq_num += self.n

    def disconnect(self):
        # send fin
        # receive fin ack
        # send ack
        # success
        if self.state == 'ACK':
            header = TCPHeader(seq_num=self.seq_num, ack_num=self.recv_seq_num+self.n, FIN=1)
            # self.seq_num += 1
            self.socket.sendto(header.get_header(), self.dest)
            self.state = 'FIN'

        elif self.state == 'FIN':
            received = str(sock.recv(1024), "utf-8")
            header = TCPHeader()
            header.set_header(received)
            if header.ACK == 1 and header.FIN == 1:
                self.state = 'FIN-ACK'
                self.recv_seq_num = header.seq_num
                self.seq_num += 1
        elif self.state == 'FIN-ACK':
            header = TCPHeader(seq_num=self.seq_num, ack_num=self.recv_seq_num+1,ACK=1)
            self.socket.sendto(header.get_header(), self.dest)
            self.state = 'CLOSED'
            self.connected = False
