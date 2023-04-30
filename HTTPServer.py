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
        request_parts = request.split('\\r\\n')

        part1 = request_parts[0].split(' ')
        # print(part1)
        self.method = part1[0]
        self.url = self.directory + "/" + part1[1]
        self.protocol = part1[2] if len(part1) > 2 else 'HTTP/1.1'
        self.data = " " + request_parts[1] if len(request_parts) > 1 else None
        # print(self.data)

    def respond(self, request):
        self.parse_request(request)
        response = self.protocol + ' '
        # print('here')
        if self.method == "GET":
            try:
                with open(self.url, "r") as f:
                    self.data = f.read()
                self.status_code = "200 OK"

            except:
                self.status_code = "404 NOT FOUND"

            if self.data == None:
                self.data = ''
            if os.path.splitext(self.url)[1] == '.html':
                self.content_type = "Content-Type: text/html\r\n\r\n"
            else:
                self.content_type = "Content-Type: text/plain\r\n\r\n"
            response += self.status_code + HTTPServer.CRLF + \
                self.content_type+self.data
        elif self.method == "POST":
            if os.path.isfile(self.url):
                self.status_code = "200 OK"
                # print(f" HEREEEE{self.data}")
            else:
                self.status_code = "201 CREATED"

            with open(self.url, "a+") as f:
                f.write(self.data)
                f.seek(0)
                self.data_to_send = f.read()
                assert self.data_to_send.endswith(self.data)
            # print(f" HEREEEE2{self.data_to_send}")

            response += self.status_code + HTTPServer.CRLF + \
                "Content-Type: text/plain\r\n\r\n"+self.data_to_send
        else:
            response += "400 Bad Request\r\nContent-Type: text/plain\r\n\r\nInvalid Request!"
            # print(response)

        return response
