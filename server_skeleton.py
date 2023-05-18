import socket
import logging
import time

from game_mech import GameMech
import constante


# Está no lado do servidor: Skeleton to user interface (permite ter informação
# de como comunicar com o cliente)
class SkeletonServer:

    def __init__(self, gm_obj: GameMech):
        self.gm = gm_obj
        self.s = socket.socket()
        self.s.bind((constante.ENDERECO_SERVIDOR, constante.PORTO))
        self.s.listen()

    @staticmethod
    def send_int(msg: int, socket_client):
        time.sleep(constante.TIME_TO_SEND)  # da tempo para o cliente começar a escutar
        socket_client.send(msg.to_bytes(constante.N_BYTES, byteorder="big", signed=True))

    @staticmethod
    def send_str(msg: str, socket_client):
        time.sleep(constante.TIME_TO_SEND)  # da tempo para o cliente começar a escutar
        socket_client.send(msg.encode(constante.CODIFICACAO_STR))

    @staticmethod
    def receive_int(socket_client) -> int:
        return int.from_bytes(socket_client.recv(constante.N_BYTES), byteorder="big", signed=True)

    @staticmethod
    def receive_str(socket_client) -> str:
        return socket_client.recv(constante.MSG_SIZE).decode(constante.CODIFICACAO_STR)

    def process_x_max(self, s_c):
        self.send_int(self.gm.x_max, s_c)

    def process_y_max(self, s_c):
        self.send_int(self.gm.y_max, s_c)

    def process_move_player(self, s_c):
        # recebe o número do jogador e direção que quer ir
        msg = self.receive_int(s_c)

        # separa a número do jogador e a direção
        new_player_pos: tuple = self.gm.execute(0, msg)

        # manda a nova posição
        self.send_int(new_player_pos[0], s_c)
        self.send_int(new_player_pos[1], s_c)

    # exemplo de processamento
    # def processa_soma(self,s_c):
    #     dados_recebidos: bytes = s_c.recv(constante.N_BYTES)
    #     # Receber dois inteiros do cliente!
    #
    #     value1 = int.from_bytes(dados_recebidos, byteorder='big', signed=True)
    #     logging.debug("o cliente enviou: \"" + str(value1) + "\"")
    #
    #     dados_recebidos: bytes = s_c.recv(constante.N_BYTES)
    #     value2 = int.from_bytes(dados_recebidos, byteorder='big', signed=True)
    #     logging.debug("o cliente enviou: \"" + str(value2) + "\"")
    #     # Processa a soma
    #     soma = self.gm.add(value1, value2)
    #     # Devolver ao cliente o resultado da soma
    #     s_c.send(soma.to_bytes(constante.N_BYTES, byteorder="big", signed=True))
    #     # AJUDAS
    #     # -- int.from_bytes(dados_recebidos, byteorder='big', signed=True)
    #     # -- to_bytes(constante.N_BYTES, byteorder="big", signed=True)

    def run(self):
        logging.info("a escutar no porto " + str(constante.PORTO))
        socket_client, address = self.s.accept()
        logging.info("o cliente com endereço " + str(address) + " ligou-se!")

        fim = False
        while fim == False:
            msg = self.receive_str(socket_client)
            # logging.debug("o cliente enviou: \"" + msg + "\"")

            if msg == constante.X_MAX:
                self.process_x_max(socket_client)
            elif msg == constante.Y_MAX:
                self.process_y_max(socket_client)
            elif msg == constante.MOVE_PLAYER:
                self.process_move_player(socket_client)
            elif msg == constante.END:
                fim = True

        socket_client.close()
        logging.info("o cliente com endereço o " + str(address) + " desligou-se!")

        self.s.close()


logging.basicConfig(filename=constante.NOME_FICHEIRO_LOG,
                    level=constante.NIVEL_LOG,
                    format='%(asctime)s (%(levelname)s): %(message)s')
