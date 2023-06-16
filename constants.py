import logging

SERVER_ADDRESS = '127.0.0.1'
PORT = 8001
# Tipo de mensagens
END = "fim"
TRUE ="True"
FALSE ="False"
X_MAX =       "x max      "
Y_MAX =       "y max      "
ADD_PLAYER =  "add player "
GET_PLAYERS = "get players"
GET_OBST    = "get obst   "
NR_PLAYERS  = "nr players "
NR_OBST     = "nr obst    "
PLAYER_MOV  = "player mov "
START_GAME  = "start game "
UPDATE      = "update     "
MSG_SIZE = 11
N_BYTES = 20
ACCEPT_TIMEOUT = 1
STR_COD = 'utf-8'
LOG_FILE_NAME = "game-server.log"
LOG_LEVEL = logging.DEBUG
NR_CLIENTS = 2