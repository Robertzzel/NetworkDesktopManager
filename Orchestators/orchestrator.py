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
