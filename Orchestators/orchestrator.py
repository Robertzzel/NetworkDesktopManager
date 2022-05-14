from zmq.sugar import Socket


class Orchestrator:
    async def receive_object(self, sock: Socket):
        try:
            return await sock.recv_pyobj()
        except Exception as ex:
            return None

    async def receive(self, sock: Socket):
        try:
            return await sock.recv()
        except Exception as ex:
            return None

    async def receive_string(self, sock: Socket):
        try:
            return await sock.recv_string()
        except Exception as ex:
            return None

    @staticmethod
    def create_file(filepath):
        import os

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.exists(filepath):
            with open(filepath, 'w'):
                pass
