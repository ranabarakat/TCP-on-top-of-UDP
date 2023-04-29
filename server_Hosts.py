import socketserver
from TCP import *
from host import Connection

HOST, PORT = "localhost", 9999


class MyUDPHandler(socketserver.BaseRequestHandler):
    connections = []

    def setup(self):
        self.current_connection = None
        for conn in MyUDPHandler.connections:
            if conn.dest == self.client_address:
                self.current_connection = conn

        if self.current_connection==None:
            print('new connection')
            serv = Connection(self.request[1],self.client_address)
            MyUDPHandler.connections.append(serv)
            self.current_connection = serv

        
        

    def handle(self):
        self.msg = self.request[0].strip()
        self.current_connection.receive(self.msg)
