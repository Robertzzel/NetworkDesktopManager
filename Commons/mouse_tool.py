from pynput.mouse import Listener


class MouseTool:
    @staticmethod
    def listen_for_clicks(on_move, on_click):
        with Listener(on_move=on_move, on_click=on_click) as listener:
            listener.join()