from TCP import TCPHeader
import socketserver

HOST, PORT = "localhost", 9999

    
class MyUDPHandler(socketserver.BaseRequestHandler):
    state = 'CLOSED'
    def do_header(self):
        header = self.msg[:32]  # take first 29 bytes for header
        self.header1 = ''.join(format(i, '08b')
                         for i in header)  # convert header to binary

        self.header = TCPHeader()
        self.header.set_header(self.header1)

    def handle(self):
        self.msg = self.request[0].strip()
        self.do_header()
        # print('received: {}'.format(self.msg))
        # print('header: {}'.format(self.header1))
        if self.state == 'CLOSED':
            if self.header.SYN:
                seq = self.header.get_seq()
                # create a header with SYN flag only
                header = TCPHeader(seq_num=0, ack_num=seq,
                                    SYN=1, ACK=1, FIN=0)
                # self.seq_num += 1
                socket = self.request[1]
                socket.sendto(header.get_header(), self.client_address)
                # print('sending: {}'.format(header.get_header()))
                self.state = 'SYN-ACK'

        elif self.state == 'SYN-ACK':
            if self.header.SYN:
                self.state = 'ACK'
                # make sure ack was received before setting connnected = true
                self.connected = True
                
                
if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()