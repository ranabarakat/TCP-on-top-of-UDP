from TCP import *


class Connection():
    def __init__(self, sock, dest) -> None:
        self.socket = sock
        self.dest = dest
        self.connected = False
        self.state = 'CLOSED'
        self.packet_to_transmit = 0  # current packet up for transmission
        self.packets = []
        self.received_msg = []
        self.closing = False
        self.socket.settimeout(0.1)
        # self.socket.setblocking(True)
        # self.seq_num = random.randint(0,9999)
        # self.seq_num = 5407
        self.seq_num = 0
        self.ack_num = 1
        self.n = 32  # each packet consists of 32-byte payload + 32-byte header
        self.connection_trials = 5

    def bytes_to_bits(bytes):
        # print(len(bytes))
        # bits = ''.join(['{0:08b}'.format(ord(i)) for i in bytes.decode()])
        bits = ''.join([format(i, '08b') for i in bytes])
        return bits

    def connect(self):
        # create a header with SYN flag only
        self.seq_num += self.n
        header = TCPHeader(seq_num=self.seq_num, ack_num=self.ack_num,
                           SYN=1, ACK=0, FIN=0)
        # header_tmp = ''.join(format(i, '08b')
        #                 for i in header.get_header())  # convert header to binary
        # print('sending: {}'.format(header_tmp))
        self.socket.sendto(header.get_header(), self.dest)
        self.state = 'SYN'

        # try:
        #     received = self.socket.recv(1024)
        #     received = Connection.bytes_to_bits(received)
        # except:
        #     print('timed out')

        # header = TCPHeader()
        # header.set_header(received)
        # if header.ACK == 1 and header.SYN == 1:
        #     self.state = 'SYN-ACK'
        #     self.ack_num = header.seq_num+1
        # else:
        #     return False

        trials = 1
        flag = 0
        try:
            received = self.socket.recv(1024)
            received = Connection.bytes_to_bits(received)
            flag = 1
        except:
            print('timed out')

        while not flag and trials <= self.connection_trials:
            try:
                received = self.socket.recv(1024)
                received = Connection.bytes_to_bits(received)
                flag = 1
                header = TCPHeader()
                header.set_header(received)
                if header.ACK == 1 and header.SYN == 1:
                    self.state = 'SYN-ACK'
                    self.ack_num = header.seq_num+1
                else:
                    return False
            except:
                print("timed out")
                trials += 1

        if not flag:
            return False

        self.seq_num += self.n
        header = TCPHeader(seq_num=self.seq_num, ack_num=self.ack_num,
                           SYN=0, ACK=1, FIN=0)
        self.socket.sendto(header.get_header(), self.dest)
        self.state = 'ACK'
        self.connected = True

        return True

    def accept_connection(self):
        print('Accepting Connection')
        self.ack_num = self.header.seq_num+1
        self.seq_num += self.n
        header = TCPHeader(seq_num=self.seq_num, ack_num=self.ack_num,
                           SYN=1, ACK=1)
        self.socket.sendto(header.get_header(), self.dest)
        self.state = 'SYN-ACK'

        received = self.socket.recv(1024)
        received = Connection.bytes_to_bits(received)
        header = TCPHeader()
        header.set_header(received)
        if header.ACK == 1:
            self.state = 'ACK'
            self.ack_num = header.seq_num + 1
            self.connected = True
            print('Handshake complete')
            return True
        else:
            return False

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
        print('Resetting sent packets')
        self.packet_to_transmit = 0
        self.packets = []
        print('Parsing message: ..')
        payloads = self.parse_msg(message)
        print('Done.')

        if self.connected:
            print('Confirmed connection')
            print('Starting while loop:')
            while len(self.packets) < len(payloads):
                self.seq_num += self.n + len(payloads[self.packet_to_transmit])
                header = TCPHeader(
                    seq_num=self.seq_num, ack_num=self.ack_num, ACK=1)
                packet = header.get_header() + \
                    payloads[self.packet_to_transmit]
                print('Sending packet')
                self.socket.sendto(packet, self.dest)
                print('Done.')
                print('Waiting for ack')
                received = self.socket.recv(1024)
                print('Received message')
                print('Confirming ack')
                header_bits = Connection.bytes_to_bits(received[:32])
                print(header_bits)
                header = TCPHeader()
                header.set_header(header_bits)
                if header.ACK == 1:  # and header.ack_num == self.seq_num+1:
                    print('Confirmed')
                    self.packets.append(packet)
                    self.packet_to_transmit += 1
                    self.ack_num = header.seq_num+1
                    # EDITED LINE
                    # self.seq_num += self.n

    def receive(self, msg=None, buff_size=1024):
        self.message = ''
        # interpret message
        if msg == None:
            received = self.socket.recv(buff_size)
        else:
            received = msg
        header_bits = Connection.bytes_to_bits(received[:32])
        self.header = TCPHeader()
        self.header.set_header(header_bits)

        print('Received: {}'.format(received[32:].decode()))

        if self.header.FIN:
            self.closing = True

        if self.closing:
            self.close()
        elif self.connected:
            print('Connected')
            if self.header.seq_num > self.ack_num:
                print('Message checks out')
                self.received_msg.append(received[32:].decode())
                if len(received) < 64:
                    self.message = ''.join(self.received_msg)
                    self.received_msg = []
                    # print(self.message)
                self.seq_num += self.n
                self.ack_num = self.header.seq_num + 1
                header = TCPHeader(seq_num=self.seq_num, ack_num=self.ack_num,
                                   SYN=0, ACK=1, FIN=0)
                print("ACKNOWLEDGING")
                self.socket.sendto(header.get_header(), self.dest)
            while len(received) == 64 and msg == None:
                received = self.socket.recv(buff_size)
                header_bits = Connection.bytes_to_bits(received[:32])
                self.header = TCPHeader()
                self.header.set_header(header_bits)
                print('Received: {}'.format(received[32:].decode()))
                if self.connected:
                    print('Connected')
            if self.header.seq_num > self.ack_num:
                print('Message checks out')
                self.received_msg.append(received[32:].decode())
                if len(received) < 64:
                    self.message = ''.join(self.received_msg)
                    self.received_msg = []
                    # print(self.message)
                self.seq_num += self.n
                self.ack_num = self.header.seq_num + 1
                header = TCPHeader(seq_num=self.seq_num, ack_num=self.ack_num,
                                   SYN=0, ACK=1, FIN=0)
                print("ACKNOWLEDGING")
                self.socket.sendto(header.get_header(), self.dest)

                # self.send(header.get_header())
            if len(received) < 64:
                return self.message

        elif self.header.SYN:
            self.accept_connection()

        print('Current seq_num: {}'.format(self.seq_num))
        print('Current ack_num: {}'.format(self.ack_num))

    def disconnect(self):
        self.seq_num += self.n
        header = TCPHeader(seq_num=self.seq_num, ack_num=self.ack_num, FIN=1)
        self.socket.sendto(header.get_header(), self.dest)
        self.state = 'FIN'

        # print('Waiting for FIN-ACK')
        received = self.socket.recv(1024)
        received = Connection.bytes_to_bits(received)
        header = TCPHeader()
        header.set_header(received)
        if header.ACK == 1 and header.FIN == 1:
            self.state = 'FIN-ACK'
            self.ack_num = header.seq_num+1

        self.seq_num += self.n
        header = TCPHeader(seq_num=self.seq_num, ack_num=self.ack_num, ACK=1)
        self.socket.sendto(header.get_header(), self.dest)
        self.state = 'CLOSED'
        self.connected = False

    def close(self):
        print('Received FIN, closing connection')
        self.ack_num = self.header.seq_num+1
        self.seq_num += self.n
        header = TCPHeader(seq_num=self.seq_num,
                           ack_num=self.ack_num, ACK=1, FIN=1)
        self.socket.sendto(header.get_header(), self.dest)
        self.state = 'FIN-ACK'

        received = self.socket.recv(1024)
        received = Connection.bytes_to_bits(received)
        header = TCPHeader()
        header.set_header(received)
        print('Received message, confirming ack')
        # print(received)
        # conversion problem still exists
        # TODO
        # fix it
        if header.ACK:
            self.ack_num = header.seq_num+1
            self.state = 'CLOSED'
            self.connected = False
            print('Connection closed')
