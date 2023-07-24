import socket
import threading


class MyRedis:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None


    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(4096)
                print(data)

                if not data:
                    break

            except Exception as e:
                print(f"{e}")

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()


if __name__ == "__main__":
    server = MyRedis('localhost', 6379)
    server.start()
