import client
import socket

HOST, PORT = "localhost", 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(True)

test_client = client.ClientConnection(sock, (HOST,PORT))

print(test_client.state)
test_client.handshake()
print(test_client.state)
test_client.handshake()
print(test_client.state)
test_client.handshake()
print(test_client.state)


test_client.disconnect()
print(test_client.state)
test_client.disconnect()
print(test_client.state)
test_client.disconnect()
print(test_client.state)