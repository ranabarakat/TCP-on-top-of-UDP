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
        self.connection_trials = 3

    def bytes_to_bits(bytes):
        # print(len(bytes))
        # bits = ''.join(['{0:08b}'.format(ord(i)) for i in bytes.decode()])
        bits = ''.join([format(i, '08b') for i in bytes])
        return bits
    
    def confirm_checksum(self, msg):
        header_bits = Connection.bytes_to_bits(msg[:32])
        checksum = int(header_bits[64:192], 2)
        header_bits = header_bits[:64] + '{0:0128b}'.format(0) + header_bits[192:]
        message = TCPHeader.bits_to_bytes(header_bits) + msg[32:]
        computed_checksum = int.from_bytes(hashlib.md5(message).digest())
        # print('Message checksum: {}'.format(checksum))
        # print('Computed checksum: {}'.format(computed_checksum))
        return checksum == computed_checksum
        

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
            received_orig = self.socket.recv(1024)
            received = Connection.bytes_to_bits(received_orig)
            flag = 1
            if self.confirm_checksum(received_orig):
                print('Checksum confirmed')
            else:
                raise Exception('Checksum check failed')
        except:
            if not flag:
                print('Timed out')
            else:
                flag = 0

        while not flag and trials <= self.connection_trials:
            try:
                received_orig = self.socket.recv(1024)
                received = Connection.bytes_to_bits(received_orig)
                flag = 1
                if self.confirm_checksum(received_orig):
                    print('Checksum confirmed')
                else:
                    raise Exception('Checksum check failed')
                header = TCPHeader()
                header.set_header(received)
                if header.ACK == 1 and header.SYN == 1:
                    self.state = 'SYN-ACK'
                    self.ack_num = header.seq_num+1
                else:
                    return False
            except:
                if not flag:
                    print('Timed out')
                else:
                    flag = 0
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

        trials = 1
        flag = 0
        try:
            received_orig = self.socket.recv(1024)
            received = Connection.bytes_to_bits(received_orig)
            flag = 1
            if self.confirm_checksum(received_orig):
                print('Checksum confirmed')
            else:
                raise Exception('Checksum check failed')
            header = TCPHeader()
            header.set_header(received)
            if header.ACK == 1:
                self.state = 'ACK'
                self.ack_num = header.seq_num + 1
                self.connected = True
                print('Handshake complete')
        except:
            if not flag:
                print('Timed out')
            else:
                print('Checksum check failed')
                flag = 0
        while not flag and trials <= self.connection_trials:
            try:
                received_orig = self.socket.recv(1024)
                received = Connection.bytes_to_bits(received_orig)
                flag = 1
                if self.confirm_checksum(received_orig):
                    print('Checksum confirmed')
                else:
                    raise Exception('Checksum check failed')
                header = TCPHeader()
                header.set_header(received)
                print('receiving ack')
                if header.ACK == 1:
                    self.state = 'ACK'
                    print('alo')
                    self.ack_num = header.seq_num + 1
                    self.connected = True
                    print('Handshake complete')
            except:
                if not flag:
                    print('Timed out')
                else:
                    flag = 0
                    trials += 1
        if flag:       
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
        self.msg_len = len(message)
        # print(f"MESSAGE LENGTH: {self.msg_len}")
        print('Resetting sent packets')
        self.packet_to_transmit = 0
        self.packets = []
        print('Parsing message: ..')
        payloads = self.parse_msg(message)
        # print(payloads[0])
        print('Done.')

        if self.connected:
            print('Confirmed connection')
            print('Starting while loop:')
            while len(self.packets) < len(payloads):
                self.seq_num += self.n + len(payloads[self.packet_to_transmit])
                # print(f"PAYLOAD: {payloads[self.packet_to_transmit]} ")
                header = TCPHeader(
                    seq_num=self.seq_num, ack_num=self.ack_num, ACK=1, length=self.msg_len)
                # print(len(header.get_header()))
                packet = header.get_header(payloads[self.packet_to_transmit]) + \
                    payloads[self.packet_to_transmit]
                print('Sending packet')
                # print(f"message=== {packet}")
                self.socket.sendto(packet, self.dest)
                print('Done.')
                print('Waiting for ack')
                received = self.socket.recv(1024)
                print('Received message')
                print('Confirming ack')
                header_bits = Connection.bytes_to_bits(received[:32])
                # print(header_bits)
                header = TCPHeader()
                header.set_header(header_bits)
                if header.ACK == 1 and header.ack_num == self.seq_num+1:
                    print('Confirmed')
                    self.packets.append(packet)
                    self.packet_to_transmit += 1
                    self.ack_num = header.seq_num+1
                    # EDITED LINE
                    # self.seq_num += self.n
                else:
                    self.seq_num -= self.n + \
                        len(payloads[self.packet_to_transmit])

    def parse(self):
        ret = False
        if self.header.seq_num > self.ack_num:
            print('Message checks out')
            self.received_msg.append(self.received[32:].decode())

            self.received_msgg = ''.join(i for i in self.received_msg)
            # print(len(self.received_msgg))
            # print(self.received_msg)
            # print(self.recv_msg_len)

            if len(self.received_msgg) == self.recv_msg_len:
                self.message = ''.join(self.received_msg)
                self.received_msg = []
                ret = True
            self.seq_num += self.n
            self.ack_num = self.header.seq_num + 1
            header = TCPHeader(seq_num=self.seq_num, ack_num=self.ack_num,
                               SYN=0, ACK=1, FIN=0)
            print("ACKNOWLEDGING")
            self.socket.sendto(header.get_header(), self.dest)
            return ret

    def receive(self, msg=None, buff_size=1024):
        self.message = ''
        # interpret message
        if msg == None:
            trials = 1
            flag = 0
            try:
                self.received = self.socket.recv(buff_size)
                flag = 1
                if self.confirm_checksum(self.received):
                    print('Checksum confirmed')
                else:
                    raise Exception('Checksum check failed')
                
            except:
                if not flag:
                    print('Timed out')
                else:
                    print('Checksum check failed')
                    flag = 0
            while not flag and trials <= self.connection_trials:
                try:
                    self.received = self.socket.recv(buff_size)
                    flag = 1
                    if self.confirm_checksum(self.received):
                        print('Checksum confirmed')
                    else:
                        raise Exception('Checksum check failed')
                    
                except:
                    if not flag:
                        print('Timed out')
                    else:
                        flag = 0
                        trials += 1
            if not flag:
                return False
        else:
            self.received = msg

            # print(f"HELL {len(self.received[32:].decode())}")
        if self.confirm_checksum(self.received):
            print('Checksum confirmed')
        else:
            print('Checksum check failed')
        header_bits = Connection.bytes_to_bits(self.received[:32])
        self.header = TCPHeader()
        self.header.set_header(header_bits)
        self.recv_msg_len = self.header.msg_len
        # print(f"NOOOO {self.recv_msg_len}")

        # print('Received: {}'.format(self.received[32:].decode()))

        if self.header.FIN:
            self.closing = True

        if self.closing:
            self.close()
        elif self.connected:
            print('Connected')
            done = self.parse()
            while not done:
                trials = 1
                flag = 0
                try:
                    self.received = self.socket.recv(buff_size)
                    flag = 1
                    if self.confirm_checksum(self.received):
                        print('Checksum confirmed')
                    else:
                        raise Exception('Checksum check failed')
                except:
                    if not flag:
                        print('Timed out')
                    else:
                        print('Checksum check failed')
                        flag = 0
                while not flag and trials <= self.connection_trials:
                    try:
                        self.received = self.socket.recv(buff_size)
                        flag = 1
                        if self.confirm_checksum(self.received):
                            print('Checksum confirmed')
                        else:
                            raise Exception('Checksum check failed')
                    except:
                        if not flag:
                            print('Timed out')
                        else:
                            flag = 0
                            trials += 1
                if not flag:
                    return False
                if self.confirm_checksum(self.received):
                    print('Checksum confirmed')
                else:
                    print('Checksum check failed')
                header_bits = Connection.bytes_to_bits(self.received[:32])
                self.header = TCPHeader()
                self.header.set_header(header_bits)
                # self.recv_msg_len = self.header.msg_len

                # print('Received: {}'.format(self.received[32:].decode()))
                if self.connected:
                    # print('Connected')
                    done = self.parse()

                # self.send(header.get_header())

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
        flag = 0
        trials = 1
        try:
            received_orig = self.socket.recv(1024)
            received = Connection.bytes_to_bits(received_orig)
            flag = 1
            if self.confirm_checksum(received_orig):
                print('Checksum confirmed')
            else:
                raise Exception('Checksum check failed')
            header = TCPHeader()
            header.set_header(received)
            if header.ACK == 1 and header.FIN == 1:
                self.state = 'FIN-ACK'
                self.ack_num = header.seq_num+1
        except:
            if not flag:
                print('Timed out')
            else:
                print('Checksum check failed')
                flag = 0
        while not flag and trials <= self.connection_trials:
            try:
                received_orig = self.socket.recv(1024)
                received = Connection.bytes_to_bits(received_orig)
                flag = 1
                if self.confirm_checksum(received_orig):
                    print('Checksum confirmed')
                else:
                    raise Exception('Checksum check failed')
                header = TCPHeader()
                header.set_header(received)
                if header.ACK == 1 and header.FIN == 1:
                    self.state = 'FIN-ACK'
                    self.ack_num = header.seq_num+1
            except:
                if not flag:
                    print('Timed out')
                else:
                    flag = 0
                    trials += 1
        if not flag:
            return False

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
        
        flag = 0
        trials = 1
        try:
            received_orig = self.socket.recv(1024)
            received = Connection.bytes_to_bits(received_orig)
            flag = 1
            if self.confirm_checksum(received_orig):
                print('Checksum confirmed')
            else:
                raise Exception('Checksum check failed')
            header = TCPHeader()
            header.set_header(received)
            print('Received message, confirming ack')
            if header.ACK:
                self.ack_num = header.seq_num+1
                self.state = 'CLOSED'
                self.connected = False
                print('Connection closed')
        except:
            if not flag:
                print('Timed out')
            else:
                print('Checksum check failed')
                flag = 0
        while not flag and trials <= self.connection_trials:
            try:
                received_orig = self.socket.recv(1024)
                received = Connection.bytes_to_bits(received_orig)
                flag = 1
                if self.confirm_checksum(received_orig):
                    print('Checksum confirmed')
                else:
                    raise Exception('Checksum check failed')
                header = TCPHeader()
                header.set_header(received)
                print('Received message, confirming ack')
                if header.ACK:
                    self.ack_num = header.seq_num+1
                    self.state = 'CLOSED'
                    self.connected = False
                    print('Connection closed')
            except:
                if not flag:
                    print('Timed out')
                else:
                    flag = 0
                    trials += 1
        
