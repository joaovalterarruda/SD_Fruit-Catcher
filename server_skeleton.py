import socket
import logging
import game_mech
import constants
import client_session_management
from typing import Union

# Adicionar o shared
import shared

class SkeletonServer:

    def __init__(self, gm: game_mech.GameMech):
        self.gm = gm
        self.s = socket.socket()
        self.s.bind((constants.SERVER_ADDRESS, constants.PORT))
        self.s.listen()
        #------------------------------------------
        # Added timeout
        self.s.settimeout(constants.ACCEPT_TIMEOUT)
        #------------------------------------------
        self.keep_running = True
        # Shared
        self.shared = shared.Shared()


    def accept(self) -> Union['Socket', None]:
        """
        A new definition of accept() to provide a return if a timeout occurs.
        """
        try:
            client_connection, address = self.s.accept()
            logging.info("o cliente com endereço " + str(address) + " ligou-se!")

            return client_connection
        except socket.timeout:
            return None




    def run(self):
        logging.info("a escutar no porto " + str(constants.PORT))
        while self.keep_running:
            socket_client = self.accept()
            if socket_client is not None:
                # Add client
                # self._state.add_client(socket_client)
                client_session_management.ClientSession(socket_client, self.shared, self.gm).start()

        self.s.close()


logging.basicConfig(filename=constants.LOG_FILE_NAME,
                    level=constants.LOG_LEVEL,
                    format='%(asctime)s (%(levelname)s): %(message)s')