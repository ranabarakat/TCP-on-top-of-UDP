import hashlib
import math



class TCPHeader():
    def __init__(self, seq_num=0, ack_num=0, SYN=0, ACK=0, FIN=0) -> None:
        self.seq_num = seq_num  # 32 bits
        self.ack_num = ack_num  # 32 bits
        self.SYN = SYN  # 1 bit
        self.ACK = ACK  # 1 bit
        self.FIN = FIN  # 1 bit
        self.checksum = 0

        # if msg != None:
        # self.SYN = int(header[0], 2)
        # self.ACK = int(header[1], 2)
        # self.FIN = int(header[2], 2)
        # self.PID = int(header[3:35], 2)
        # self.seq_num = int(header[35:67], 2)
        # self.ack_num = int(header[67:99], 2)
        # self.checksum = int(header[99:227], 2)

        #self.msg = msg.decode()

        # else:
        #     self.SYN = 0
        #     self.ACK = 0
        #     self.FIN = 0
        #     self.PID = 0
        #     self.seq_num = 0
        #     self.ack_num = 0
        #     self.checksum = 0
    def bits_to_bytes(bits):
        # print('bits: {}'.format(bits))
        # bit_int  = int(bits,2)
        # byte_num1 = math.ceil(bit_int.bit_length()/8)
        # byte_num = 32
        # print('byte_num: {}'.format(byte_num))
        # return bit_int.to_bytes(byte_num, 'big')
        byts = ''.join([chr(int(bits[i:i+8],2)) for i in range(0, len(bits), 8)]).encode()
        # print('bytes: {}'.format(byts))
        return byts
    def set_SYN(self):
        self.SYN = 1

    def set_ACK(self):
        self.ACK = 1

    def set_FIN(self):
        self.FIN = 1

    def set_seq(self, seq):
        self.seq_num = seq
    
    def get_seq(self):
        return self.seq_num

    def set_ack(self, ack):
        self.ack_num = ack

    def set_header(self, msg):
        self.seq_num = int(msg[:32], 2)  # 32 bits
        self.ack_num = int(msg[32:64], 2)  # 32 bits
        self.checksum = int(msg[64:192], 2)  # 128 bits
        self.SYN = int(msg[192], 2)  # 1 bit
        self.ACK = int(msg[193], 2)  # 1 bit
        self.FIN = int(msg[194], 2)  # 1 bit

    def get_header(self):
        # return string representation of header:
        # concatall attributes
        # convert to binary string
        # convert binary string to ascii chars
        # convert ascii chars to string
        bits = '{0:032b}'.format(self.seq_num)
        bits += '{0:032b}'.format(self.ack_num)
        bits += '{0:0128b}'.format(self.checksum)
        bits += '{0:01b}'.format(self.SYN)
        bits += '{0:01b}'.format(self.ACK)
        bits += '{0:01b}'.format(self.FIN)
        # zero padding so that header size = 256 bits
        bits += '{0:061b}'.format(0)
        return TCPHeader.bits_to_bytes(bits)

    def get_payload(self, msg):
        return msg[256:]

    def compute_checksum(self, msg):
        self.checksum = hashlib.md5(msg.encode()).digest()
        return self.checksum