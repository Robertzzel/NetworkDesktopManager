import pynput


def oc(x, y, button, pressed):
    print(f"clicked: {x}, {y}, {button}, {pressed}")


if __name__ == "__main__":
    with pynput.mouse.Listener(on_click=oc) as listener:
        listener.join()
    print("sal")