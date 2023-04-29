import socketserver
import server

HOST, PORT = "localhost", 9999

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), server.MyUDPHandler) as server:
        server.serve_forever()