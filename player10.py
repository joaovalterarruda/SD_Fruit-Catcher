import pygame
# Player 9 is part of the test example 9
import client_stub

# Defining constants for the moves
M_UP = 0
M_RIGHT = 1
M_DOWN = 2
M_LEFT = 3


class Player(pygame.sprite.DirtySprite):
    def __init__(self, number: int, name: str, pos_x: int, pos_y: int, sq_size: int, *groups):
        super().__init__(*groups)
        self.number = number
        self.name = name
        self._direction = -1
        self.image = pygame.image.load('./intro_ball.gif')
        initial_size = self.image.get_size()
        self.sq_size = sq_size
        size_rate = sq_size / initial_size[0]
        self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = pygame.rect.Rect((pos_x * sq_size, pos_y * sq_size), self.image.get_size())

    def get_size(self):
        return self.new_size

    def moveto(self, new_x: int, new_y: int):
        self.rect.x = new_x * self.sq_size
        self.rect.y = new_y * self.sq_size
        # Keep visible
        self.dirty = 1

    def update(self, stub: client_stub.StubClient):
        #        last = self.rect.copy()
        # print("Updating player ", self.name, " with the number ", self.number)
        key = pygame.key.get_pressed()
        new_player_pos = ()
        if key[pygame.K_LEFT]:
            direction = M_LEFT
        elif key[pygame.K_RIGHT]:
            direction = M_RIGHT
        elif key[pygame.K_UP]:
            direction = M_UP
        elif key[pygame.K_DOWN]:
            direction = M_DOWN
        else:
            direction = -1

        if direction != -1:
            self._direction = direction

        if self._direction != -1:
            new_player_pos = stub.move_player(self._direction)

        if new_player_pos:
            self.moveto(new_player_pos[0], new_player_pos[1])
        # Keep visible
        self.dirty = 1
