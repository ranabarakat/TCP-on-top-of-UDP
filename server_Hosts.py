import socketserver
from TCP import *
from host import Connection
from HTTPServer import *

HOST, PORT = "localhost", 9999


class MyUDPHandler(socketserver.BaseRequestHandler):
    connections = []
    http_server = HTTPServer((HOST, PORT), "HTTP_files")

    def setup(self):
        self.current_connection = None
        for conn in MyUDPHandler.connections:
            if conn.dest == self.client_address:
                self.current_connection = conn

        if self.current_connection == None:
            print('new connection')
            serv = Connection(self.request[1], self.client_address)
            MyUDPHandler.connections.append(serv)
            self.current_connection = serv

    def handle(self):
        self.msg = self.request[0].strip()

        request = self.current_connection.receive(self.msg)

        if request is not None:
            print("server received client request")
            response = self.http_server.respond(request)
            print(response)

            self.current_connection.send(response)
            print("server sent client response")

        # print(f"x  {response}")
        # self.current_connection.receive(response.encode())

        # self.current_connection.send(response)
