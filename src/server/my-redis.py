import socket
import threading

from src.resp.deserializer import decode_resp_to_message
from src.resp.serializer import encode_message_to_resp


class MyRedis:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(4096)

                if not data:
                    break

                string_data = data.decode()
                message = decode_resp_to_message(string_data)
                command = message[0]

                if command.lower() == "ping":
                    response = encode_message_to_resp("pong")
                    client_socket.send(bytes(response, 'UTF-8'))

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
