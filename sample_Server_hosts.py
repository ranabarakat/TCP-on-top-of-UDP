import socketserver
import server_Hosts

HOST, PORT = "localhost", 9999

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), server_Hosts.MyUDPHandler) as server:
        server.serve_forever()