import socket
import time

import constante


# Stub do lado do cliente: como comunicar com o servidor...

class StubClient:

    def __init__(self):
        self.s: socket = socket.socket()
        self.s.connect((constante.ENDERECO_SERVIDOR, constante.PORTO))

    def send_int(self, msg: int):
        time.sleep(constante.TIME_TO_SEND)  # da tempo para o servidor começar a escutar
        self.s.send(msg.to_bytes(constante.N_BYTES, byteorder="big", signed=True))

    def send_str(self, msg: str):
        time.sleep(constante.TIME_TO_SEND)  # da tempo para o servidor começar a escutar
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

    def receive_int(self) -> int:
        return int.from_bytes(self.s.recv(constante.N_BYTES), byteorder="big", signed=True)

    def receive_str(self) -> str:
        return self.s.recv(constante.MSG_SIZE).decode(constante.CODIFICACAO_STR)

    def dimension_size(self):
        self.send_str(constante.X_MAX)
        x_max = self.receive_int()

        self.send_str(constante.Y_MAX)
        y_max = self.receive_int()

        return x_max, y_max

    def move_player(self, direction: int) -> tuple:
        self.send_str(constante.MOVE_PLAYER)
        self.send_int(direction)

        # recebe x e recebe y
        return self.receive_int(), self.receive_int()

    # exemplo de pedido
    # def add(self, value1: int, value2: int) -> Union[int, None]:
    #
    #     msg = constante.SOMA
    #     self.s.send(msg.encode(constante.CODIFICACAO_STR))
    #     self.s.send(value1.to_bytes(constante.N_BYTES, byteorder="big", signed=True))
    #     self.s.send(value2.to_bytes(constante.N_BYTES, byteorder="big", signed=True))
    #     dados_recebidos: bytes = self.s.recv(constante.N_BYTES)
    #     return int.from_bytes(dados_recebidos, byteorder='big', signed=True)
    #     #if msg != constante.END:
    #     #    dados_recebidos: bytes = self.s.recv(constante.TAMANHO_MENSAGEM)
    #     #    return dados_recebidos.decode(constante.CODIFICACAO_STR)
    #     #else:
    #     #    self.s.close()
