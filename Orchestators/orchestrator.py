class Orchestrator:
    def receive_message(self, sock, length_max_size: int) -> bytes:
        try:
            length_data = sock.recv(length_max_size).decode()
            length = int(length_data)
            return self.recv_all(sock, length)
        except Exception as ex:
            bad_length: bytes = length_data
            length = None
            image_component = b''
            for i in range(1, len(bad_length)):
                new_length_bytes = bad_length[:len(bad_length) - i]
                try:
                    length = int(new_length_bytes)
                except:
                    continue

                image_component += bad_length[len(bad_length) - i:]
                return self.recv_all(sock, length)
            raise Exception("Really bad transmission")

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