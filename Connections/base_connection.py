class BaseConnection:

    def recv_all(self, sock, n):
        final = bytearray()
        received = 0
        while received < n:
            received_data = sock.recv(n - received)
            final += received_data
            received += len(received_data)
        return final