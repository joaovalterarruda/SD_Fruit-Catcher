from client_stub import StubClient
from client_game import GameUI
import pygame


def main():
    pygame.init()
    stub = StubClient()
    ui = GameUI(stub)
    ui.run()


main()
