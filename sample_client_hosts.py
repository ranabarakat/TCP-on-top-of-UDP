from host import Connection
import socket

HOST, PORT = "localhost", 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

con = Connection(sock, (HOST, PORT))

con.connect()
print(con.state)
con.send('abcde')
con.disconnect()
print(con.state)


