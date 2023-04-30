import host
import socketserver
import server_Hosts
import os


class HTTPServer:
    HTTP_STATUS_CODES = {
        200: " OK",
        201: " CREATED",
        404: " NOT FOUND",
        400: " BAD REQUEST"
    }
    HTTP_METHODS = ["GET", "POST"]
    CRLF = '\r\n'

    def __init__(self, address, directory):
        self.address = address
        self.method = None
        self.url = None
        self.protocol = 'HTTP/1.1'
        self.data = None
        self.directory = directory
        # with socketserver.UDPServer(self.address, server_Hosts.MyUDPHandler) as server:
        #     server.serve_forever()

    def parse_request(self, request):
        # request = str(request)
        request_parts = request.split('\r\n')
        part1 = request_parts[0].split(' ')
        self.method = part1[0]
        self.url = self.directory + "/" + part1[1]
        self.protocol = part1[2] if len(part1) > 2 else 'HTTP/1.1'
        self.data = " " + request_parts[1] if len(request_parts) > 1 else None

    def respond(self, request):
        response = self.protocol + ' '
        self.parse_request(request)
        # print('here')
        if self.method == "GET":
            try:
                with open(self.url, "r") as f:
                    self.data = f.read()
                self.status_code = "200 OK"

            except:
                self.status_code = "404 NOT FOUND"

            response += self.status_code + HTTPServer.CRLF + \
                "Content-Type: text/plain\r\n\r\n"+self.data
            # print(response)
        elif self.method == "POST":
            if os.path.isfile(self.url):
                self.status_code = "200 OK"
            else:
                self.status_code = "201 CREATED"

            with open(self.url, "a+") as f:
                f.write(self.data)
                self.data = f.read()

            response += self.status_code + HTTPServer.CRLF + \
                "Content-Type: text/plain\r\n\r\n"+self.data
        else:
            response += "400 Bad Request\r\nContent-Type: text/plain\r\n\r\nInvalid Request!"
            # print(response)

        return response
