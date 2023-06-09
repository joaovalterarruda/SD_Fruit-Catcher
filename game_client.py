import pygame
import player10, wall10
import client_stub


# ---------------------
# The grid now is built based on the number of squares in x and y.
# This allows us to associate the size of the space to a matrix or to a dictionary
# that will keep data about each position in the environment.
# Moreover, we now can control the movement of the objects.
# We now separate the control of the environment

class GameUI(object):
    def __init__(self, stub: client_stub.StubClient, grid_size: int = 30):
        dim: tuple = stub.dimension_size()
        self.x_max = dim[0]
        self.y_max = dim[1]
        self.stub = stub

        self.width, self.height = self.x_max * grid_size, self.y_max * grid_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("first game")
        self.clock = pygame.time.Clock()
        # RGB colours
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        # Grid
        self.grid_size = grid_size
        grid_colour = self.black
        # Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(self.white)
        self.screen.blit(self.background, (0, 0))
        self.draw_grid(self.black)
        pygame.display.update()

    # Drawing a square grid
    def draw_grid(self, colour: tuple):
        for x in range(0, self.x_max):
            pygame.draw.line(self.screen, colour, (x * self.grid_size, 0), (x * self.grid_size, self.height))
        for y in range(0, self.y_max):
            pygame.draw.line(self.screen, colour, (0, y * self.grid_size), (self.width, y * self.grid_size))

    def set_players(self):
        self.players = pygame.sprite.LayeredDirty()
        # Test
        # Test
        p_x, p_y = 5, 5
        player = player10.Player(0, "player", p_x, p_y, self.grid_size, self.players)
        self.players.add(player)

    # def set_walls(self, wall_size: int):
    #     self.wl = self.gm.get_obstacles()
    #     # Create Wall (sprites) around world
    #     self.walls = pygame.sprite.Group()
    #     nr_obstacles = self.gm.get_nr_obstacles()
    #     for nr in range(nr_obstacles):
    #         if self.wl[nr] != []:
    #             w_x, w_y = self.wl[nr][1][0], self.wl[nr][1][1]
    #             wall = wall10.Wall(w_x, w_y, self.grid_size, self.walls)
    #             self.walls.add(wall)

    def run(self):
        # Create Sprites
        # self.set_walls(self.grid_size)
        # self.walls.draw(self.screen)
        self.set_players()

        end = False
        # previous_tick = self.gm.get_tick()
        # World is updated every time
        world = dict()
        while end == False:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # send information "disconnected"
                    # if answer is ok, then end is true
                    end = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # send information "disconnected"
                    # if answer is ok, them end is true
                    end = True

            self.players.update(self.stub)
            # self.walls.update()
            rects = self.players.draw(self.screen)
            self.draw_grid(self.black)
            pygame.display.update(rects)
            self.players.clear(self.screen, self.background)
        return True
