from host import Connection
import socket
from HTTPClient import *
import sys

HOST, PORT = "localhost", 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

con = Connection(sock, (HOST, PORT))

# sock.settimeout(0.1)
if __name__ == "__main__":
    method = sys.argv[1].upper()
    # print(method)
    path = sys.argv[2]
    client1 = HTTPClient(con)
    if method == 'GET':
        response = client1.get(path)
        print(f" FINAL RESPONSE: {response}")
    elif method == 'POST':
        data = sys.argv[3]
        client1.post(path, data)


# con.connect()
# print(con.state)
# con.send('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeesssseeeeeeeeeeeeeeeeeeseeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeesssseeeeeeeeeeeeeeeeeesddddddddddsddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
# con.send('message 2')
# con.send('message 3')
# con.disconnect()
# print(con.state)
