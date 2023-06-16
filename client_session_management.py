from threading import Thread
import game_mech
import constants
import json
import logging
#Shared added
import shared

class ClientSession(Thread):

    def __init__(self, socket_client: int, shr: shared.Shared, gm: game_mech.GameMech):
        """
        Constructs a thread to hold a session with the client
        :param shared_state: The server's state shared by threads
        :param client_socket: The client's socket
        """
        Thread.__init__(self)
        # Shared...
        self._shared = shr
        self.socket_client = socket_client
        self.gm = gm

    def process_x_max(self,s_c):
        x = self.gm.x_max
        s_c.send(x.to_bytes(constants.N_BYTES,byteorder= "big", signed=True))

    def process_y_max(self,s_c):
        y = self.gm.y_max
        s_c.send(y.to_bytes(constants.N_BYTES,byteorder= "big", signed=True))

    def process_add_player(self, s_c):
        """
        Adiciona jogador com nome e posição
        :param s_c:
        :return:
        """
        logging.debug("O cliente define o jogador")
        ln: bytes = s_c.recv(constants.N_BYTES)
        nm: bytes = s_c.recv(int.from_bytes(ln, byteorder='big', signed=True))
        name = nm.decode(constants.STR_COD)
        xb: bytes = s_c.recv(constants.N_BYTES)
        x = int.from_bytes(xb, byteorder='big', signed=True)
        yb: bytes = s_c.recv(constants.N_BYTES)
        y = int.from_bytes(yb, byteorder='big', signed=True)
        # Testing for player name and its position
        print("The name of player:", name)
        print("Position of player (x,y)=(",x,",",y,")")
        number = self.gm.add_player(name,x,y)
        self._shared.add_client(s_c)
        self._shared.control_nr_clients()
        s_c.send(number.to_bytes(constants.N_BYTES,byteorder="big", signed=True))


    def process_get_obst(self, s_c):
        ob = self.gm.obstacles
        msg = json.dumps(ob)
        dim = len(msg)
        s_c.send(dim.to_bytes(constants.N_BYTES,byteorder= "big", signed=True))
        s_c.send(msg.encode(constants.STR_COD))

    def process_get_nr_obst(self, s_c):
        nr_ob = self.gm.nr_obstacles
        s_c.send(nr_ob.to_bytes(constants.N_BYTES,byteorder= "big", signed=True))


    def process_get_players(self, s_c):
        pl = self.gm.players
        msg = json.dumps(pl)
        dim = len(msg)
        print("Dimension of the get players message:",dim)
        print("Message:",msg)
        s_c.send(dim.to_bytes(constants.N_BYTES,byteorder= "big", signed=True))
        s_c.send(msg.encode(constants.STR_COD))

    def process_get_nr_players(self, s_c):
        nr_pl = self.gm.nr_players
        s_c.send(nr_pl.to_bytes(constants.N_BYTES,byteorder= "big", signed=True))

    def process_player_mov(self, s_c):
        data: bytes = s_c.recv(constants.N_BYTES)
        mov = int.from_bytes(data, byteorder='big', signed=True)
        data: bytes = s_c.recv(constants.N_BYTES)
        nr_player = int.from_bytes(data, byteorder='big', signed=True)
        pos = self.gm.execute(mov,"player",nr_player)
        msg = json.dumps(pos)
        dim = len(msg)
        s_c.send(dim.to_bytes(constants.N_BYTES,byteorder= "big", signed=True))
        s_c.send(msg.encode(constants.STR_COD))

    def process_start_game(self, s_c):
        logging.debug("O client pretende inciar o jogo")
        self._shared._clients_control.acquire()
        logging.debug("O client vai iniciar o jogo")

        # Returning 'yes'
        value = constants.TRUE
        s_c.send(value.encode(constants.STR_COD))


    def process_update(self,s_c):
        logging.debug("O client pede um update")
        pl: bytes = s_c.recv(constants.N_BYTES)
        number = int.from_bytes(pl, byteorder='big', signed=True)
        #Atualizar
        #pos = self.gm.get_player_pos("player", number)
        pos = self.gm.players[number][1]
        msg = json.dumps(pos)
        # Get the size of serialized data
        size = len(msg)
        s_c.send(size.to_bytes(constants.N_BYTES, byteorder="big", signed=True))
        # Test
        #  print("New position sent to client:",msg)
        s_c.send(msg.encode(constants.STR_COD))



    def dispatch_request(self, socket_client) -> bool:
        """
        :return:
        """
        lr = False
        data_rcv: bytes = socket_client.recv(constants.MSG_SIZE)
        data_str = data_rcv.decode(constants.STR_COD)
        # logging.debug("o cliente enviou: \"" + data_str + "\"")
        if data_str == constants.X_MAX:
            self.process_x_max(socket_client)
        elif data_str == constants.Y_MAX:
            self.process_y_max(socket_client)
        elif data_str == constants.ADD_PLAYER:
            self.process_add_player(socket_client)
        elif data_str == constants.GET_PLAYERS:
            self.process_get_players(socket_client)
        elif data_str == constants.NR_PLAYERS:
            self.process_get_nr_players(socket_client)
        elif data_str == constants.GET_OBST:
            self.process_get_obst(socket_client)
        elif data_str == constants.NR_OBST:
            self.process_get_nr_obst(socket_client)
        elif data_str == constants.PLAYER_MOV:
            self.process_player_mov(socket_client)
        # Start the game....
        elif data_str == constants.START_GAME:
            self.process_start_game(socket_client)
        elif data_str == constants.UPDATE:
            self.process_update(socket_client)
        elif data_str == constants.END:
            lr = True
        return lr

    def run(self):
        """Maintains a session with the client, following the established protocol"""
        #logging.debug("Client " + str(client.peer_addr) + " just connected")
        last_request = False
        while not last_request:
            last_request = self.dispatch_request(self.socket_client)
        logging.debug("Client " + str(self.socket_client.peer_addr) + " disconnected")
        # Sared stuff
        #self._shared_state.remove_client(self._client_connection)
        #self._shared_state.concurrent_clients.release()
