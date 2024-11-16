from constants import *


class MD5:

    def __init__(self):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.T = T
        self.s = s

    @staticmethod
    def __left_rotate(n, b): return ((n << b) | (n >> (32 - b))) & 0xffffffff
    @staticmethod
    def __fun_f(x: int, y: int, z: int) -> int: return (x & y) | (~x & z)
    @staticmethod
    def __fun_g(x: int, y: int, z: int) -> int: return (x & z) | (~z & y)
    @staticmethod
    def __fun_h(x: int, y: int, z: int) -> int: return x ^ y ^ z
    @staticmethod
    def __fun_i(x: int, y: int, z: int) -> int: return y ^ (~z | x)

    @staticmethod
    def _line_preparation(message: str) -> bytearray:

        # Перевод в байты
        message = bytearray(message.encode('ascii'))
        length = (8 * len(message)) & 0xFFFFFFFFFFFFFFFF

        # После сообщения добавляется один бит 1 (в шестнадцатеричном виде 0x80)
        message.append(0x80)

        # Дополняется до блока из 512 битов (если остается меньше)
        while len(message) % 64 != 56:
            message.append(0x00)

        message.extend(length.to_bytes(8, byteorder='little'))

        return message

    def _main_cycle(self, message: bytearray) -> tuple[int, int, int, int]:

        A = self.A
        B = self.B
        C = self.C
        D = self.D

        for i in range(0, len(message), 64):

            X = [int.from_bytes(message[i:i+4], byteorder='little') for i in range(i, i+64, 4)]

            A_, B_, C_, D_ = A, B, C, D

            # Main loop
            for j in range(64):
                if j < 16:
                    F = self.__fun_f(B, C, D)
                    F_index = j
                elif j < 32:
                    F = self.__fun_g(B, C, D)
                    F_index = (5 * j + 1) % 16
                elif j < 48:
                    F = self.__fun_h(B, C, D)
                    F_index = (3 * j + 5) % 16
                else:
                    F = self.__fun_i(B, C, D)
                    F_index = (7 * j) % 16

                d_temp = D
                D = C
                C = B
                B = B + self.__left_rotate((A + F + T[j] + X[F_index]) & 0xFFFFFFFF, s[j])
                A = d_temp

            # Update state
            A = (A + A_) & 0xFFFFFFFF
            B = (B + B_) & 0xFFFFFFFF
            C = (C + C_) & 0xFFFFFFFF
            D = (D + D_) & 0xFFFFFFFF

        return A, B, C, D

    @staticmethod
    def __output(A: int, B: int, C: int, D: int) -> str:

        result = bytearray(A.to_bytes(4, byteorder='little'))
        result.extend(B.to_bytes(4, byteorder='little'))
        result.extend(C.to_bytes(4, byteorder='little'))
        result.extend(D.to_bytes(4, byteorder='little'))

        return result.hex()

    def md5(self, message: str):

        # Преобразуем строку и дополним её по правилам
        msg_bytearray: bytearray = self._line_preparation(message=message)

        # Запускаем циклы
        self.A, self.B, self.C, self.D = self._main_cycle(message=msg_bytearray)

        # Выводим хэш в шестнадцатеричном виде
        return self.__output(
            A=self.A,
            B=self.B,
            C=self.C,
            D=self.D,
        )








