import socket

HOST = '127.0.0.1'
PORT = 9999

class Server:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.listening = True
        
    def listen(self):
        while self.listening:
            print('listening...')
            self.s.listen()
            conn, addr = self.s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
    
server = Server(HOST, PORT)
server.listen()