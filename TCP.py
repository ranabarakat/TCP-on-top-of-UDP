class TCPHeader():
    def __init__(self, header=None) -> None:
        if header != None:
            self.SYN = int(header[0], 2)
            self.ACK = int(header[1], 2)
            self.FIN = int(header[2], 2)
            self.PID = int(header[3:35], 2)
            self.seq_num = int(header[35:67], 2)
            self.ack_num = int(header[67:99], 2)
            self.checksum = int(header[99:227], 2)
        else:
            self.SYN = 0
            self.ACK = 0
            self.FIN = 0
            self.PID = 0
            self.seq_num = 0
            self.ack_num = 0
            self.checksum = 0

    def set_SYN(self):
        self.SYN = 1

    def set_ACK(self):
        self.ACK = 1

    def set_FIN(self):
        self.FIN = 1

    def set_seq(self, seq):
        self.seq_num = seq

    def set_ack(self, ack):
        self.ack_num = ack

    def get_header(self):
        # return string representation of header:
        # concatall attributes
        # convert to binary string
        # convert binary string to ascii chars
        # convert ascii chars to string
        pass


class ClientConnection():
    def __init__(self, src, dest) -> None:
        self.socket = (src, dest)
        self.connected = False

    def connect(self):
        # send syn
        # receive syn ack
        # send ack
        # success
        pass

    def create_header(self, message):
        pass

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

    def disconnect(self):
        # send fin
        # receive fin ack
        # send ack
        # success
        pass


class ServerConnection():
    def __init__(self, src, dest) -> None:
        self.socket = (src, dest)
        # 0 = not done, 1 = stage one done, 2 = stage 2 done, 3 = 3 way handshake complete
        self.handshake = 0
        self.ongoing = False

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Connection) and hash(self.socket) == hash(__value.socket)

    def handle(self, header):
        if self.handshake < 3:
            if Connection.check_handshake(header) == self.handshake+1:
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

    def close(self):
        pass
