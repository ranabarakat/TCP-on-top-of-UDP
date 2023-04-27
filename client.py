import socket
from TCP import *


HOST, PORT = "localhost", 9999
# data = " ".join(sys.argv[1:])
data = 'hello world@1'

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
sock.sendto(bytes(data + "\n", "utf-8"), (HOST, PORT))
received = str(sock.recv(1024), "utf-8")

print("Sent:     {}".format(data))
print("Received: {}".format(received))

# TODO
# connection.connect()
# connection.send()
# connection.disconnect()

# connect(): start 3 way handshake
