class Orchestrator:
    def receive_message(self, sock, length_max_size: int):
        try:
            length_data = self.recv_all(sock, length_max_size).decode()
            length = int(length_data)
            return self.recv_all(sock, length)
        except Exception as ex:
            length, image_part = self._get_actual_length_from_error(ex)
            if not (length is None or image_part is None or length == 0):
                return image_part + self.recv_all(sock, length)

            return None

    def _get_actual_length_from_error(self, exception):
        bad_length: bytes = exception.object
        for i in range(1, len(bad_length)):
            new_length_bytes = bad_length[:len(bad_length) - i]
            try:
                length = int(new_length_bytes)
                image_component = bad_length[len(bad_length) - i:]
                return length, image_component
            except:
                continue
        return None, None

    def send_message(self, sock, message: bytes, length_max_size: int):
        length_string = str(len(message)).rjust(length_max_size, "0")
        sock.sendall(length_string.encode())
        sock.sendall(message)

    def recv_all(self, sock, n):
        final = b""
        received = 0
        while received < n:
            received_data = sock.recv(n - received)
            final += received_data
            received += len(received_data)
        print(b"received: " + final[:5])
        return final