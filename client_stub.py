import socket
import constants
import json
from typing import Union


class StubClient:

    def __init__(self):
        self.s: socket = socket.socket()
        self.s.connect((constants.SERVER_ADDRESS, constants.PORT))


    def get_obstacles(self) -> dict:
        """
        Protocolo:
        -- Envia tipo de msg 'get obst'
        -- Recebe dimensão do objeto dicionário
        -- Recebe objeto dicionário com todos os obstaculos
        :return:
        """
        msg = constants.GET_OBST
        self.s.send(msg.encode(constants.STR_COD))
        data: bytes = self.s.recv(constants.N_BYTES)
        dim = int.from_bytes(data, byteorder='big', signed=True)
        rec: bytes = self.s.recv(dim)
        obst = json.loads(rec)
        return obst

    def get_nr_obstacles(self):
        msg = constants.NR_OBST
        self.s.send(msg.encode(constants.STR_COD))
        data: bytes = self.s.recv(constants.N_BYTES)
        nr = int.from_bytes(data, byteorder='big', signed=True)
        return nr



    def get_players(self) -> dict:
        """
        Protocolo:
        -- Envia obtype de msg 'get players'
        -- Receber dimensão do objeto dicionário
        -- Recebe objeto dicionário com todos os jogadores
        :return:
        """
        msg = constants.GET_PLAYERS
        self.s.send(msg.encode(constants.STR_COD))
        data: bytes = self.s.recv(constants.N_BYTES)
        dim = int.from_bytes(data, byteorder='big', signed=True)
        rec: bytes = self.s.recv(dim)
        players = json.loads(rec)
        return players

    def get_nr_players(self) -> int:
        msg = constants.NR_PLAYERS
        self.s.send(msg.encode(constants.STR_COD))
        data: bytes = self.s.recv(constants.N_BYTES)
        nr = int.from_bytes(data, byteorder='big', signed=True)
        return nr

    def add_player(self, name: str, x:int, y:int) -> int:
        """
        Protocolo:
        - enviar msg com o nome associado ao pedido 'add player'
        - enviar o nome do jogador
        - receber o número do jogador
        :param name:
        :return:
        """
        msg = constants.ADD_PLAYER
        self.s.send(msg.encode(constants.STR_COD))
        # Send the length of the name and the name
        sz = len(name)
        self.s.send(sz.to_bytes(constants.N_BYTES, byteorder="big", signed=True))
        self.s.send(name.encode(constants.STR_COD))
        self.s.send(x.to_bytes(constants.N_BYTES, byteorder="big", signed=True))
        self.s.send(y.to_bytes(constants.N_BYTES, byteorder="big", signed=True))
        rec: bytes = self.s.recv(constants.N_BYTES)
        number = int.from_bytes(rec, byteorder='big', signed=True)
        return number

    def update(self,type:str, number:int)-> tuple:
        #pass
        msg = constants.UPDATE
        #Atualizado:
        self.s.send(msg.encode(constants.STR_COD))
        self.s.send(number.to_bytes(constants.N_BYTES, byteorder="big", signed=True))
        data: bytes = self.s.recv(constants.N_BYTES)
        dim = int.from_bytes(data, byteorder='big', signed=True)
        rec: bytes = self.s.recv(dim)
        tuple = json.loads(rec)
        # Imprimir o resultado (teste)
        # print("The results of update player nr. ",number)
        return tuple



    def get_dim_game(self) -> tuple:
        """
        Protocolo:
        - enviar msg com nome associado ao pedido max_x e max_y.
        - servidor retorna dois inteiros com essa informação.

        :return:
        """
        msg = constants.X_MAX
        self.s.send(msg.encode(constants.STR_COD))
        data: bytes = self.s.recv(constants.N_BYTES)
        x_max = int.from_bytes(data, byteorder='big', signed=True)
        msg = constants.Y_MAX
        self.s.send(msg.encode(constants.STR_COD))
        data: bytes = self.s.recv(constants.N_BYTES)
        y_max = int.from_bytes(data, byteorder='big', signed=True)
        return (x_max, y_max)

    def start_game(self) -> None:
        """
        Ask server to start the game. Server will return yes when the number of players is 2
        :return:
        """
        msg = constants.START_GAME
        # Test
        print("Message: I want to start the Game ...")
        self.s.send(msg.encode(constants.STR_COD))
        rec: bytes = self.s.recv(constants.N_BYTES)
        res = rec.decode(constants.STR_COD)
        # Test
        print("Starting the Game:", res)
        #return res


    


    #pos = gm.execute(M_UP, "player", self.number)
    def execute(self,mov:int, type:str, player:int) -> tuple:
        """
        Protocolo:
        -- Envia o tipo de msg 'player mov'
        -- Envia o movimento
        -- Envia o nr do jogador
        -- Recebe a nova posição do jogador (túpulo) que é estrutura de dados complexa.
        ----- recebo primeiro a dimensão da estrutura de dados
        ----- recebo a estrutura (tuple)
        :param mov:
        :param type:
        :param player:
        :return: new player position
        """
        msg = constants.PLAYER_MOV
        self.s.send(msg.encode(constants.STR_COD))
        self.s.send(mov.to_bytes(constants.N_BYTES,byteorder="big", signed=True))
        self.s.send(player.to_bytes(constants.N_BYTES, byteorder ="big",signed=True))
        data: bytes = self.s.recv(constants.N_BYTES)
        dim = int.from_bytes(data, byteorder='big', signed=True)
        rec: bytes = self.s.recv(dim)
        tuple = json.loads(rec)
        return tuple

