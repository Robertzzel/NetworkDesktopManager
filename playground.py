import pynput


class C:
    A = 2

    def nr(self, nr1, nr2):
        print(nr1, "%" ,nr2)


if __name__ == "__main__":
    print(C.A)
    C.A = 3
    C.nr(*(C.A,C.A))