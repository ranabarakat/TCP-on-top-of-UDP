

CRLF = '\r\n'


class HTTPClient:
    def __init__(self, connection):
        self.conn = connection
        self.conn.connect()

    def request(self, method, path, data=None):
        if data:
            request = method + " " + path + " HTTP/1.1\r\n" + data
        else:
            request = method + " " + path + " HTTP/1.1\r\n"
        # if data:
        #     request += "Content-Length: {}\r\n".format(len(data))
        # request += "\r\n"
        # if data:
        #     request += data
        # self.sock.send(request.encode('utf-8'))
        self.conn.send(request)
        print("client request is sent")
        # _ = self.conn.receive()
        response = self.conn.receive()

        print("client response is received")

        self.conn.disconnect()
        # print(response)
        return response
        # status_code = int(response.split()[1])
        # if status_code == 200:
        #     return response.split("\r\n\r\n")[1]
        # elif status_code == 201:
        #     return "Post Created!"
        # elif status_code == 400:
        #     return "Invalid Request!"
        # else:
        #     return "Unknown Error!"

    def get(self, path):
        return self.request("GET", path)

    def post(self, path, data=None):
        return self.request("POST", path, data)
