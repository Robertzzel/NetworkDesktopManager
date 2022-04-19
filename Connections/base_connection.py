class BaseConnection:
    def receive_message(self, sock, length_max_size: int) -> bytes:
        length = int(sock.recv(length_max_size).decode())
        return self.recv_all(sock, length)

    def send_message(self, sock, message: bytes, length_max_size: int):
        length_string = str(len(message)).rjust(length_max_size, "0")
        sock.sendall(length_string.encode())
        sock.sendall(message)

    def recv_all(self, sock, n):
        final = bytearray()
        received = 0
        while received < n:
            received_data = sock.recv(n - received)
            final += received_data
            received += len(received_data)
        return final