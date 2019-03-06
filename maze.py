import pygame
from numpy import loadtxt
from Tiles import Tile
from fruit import Berry


class Teleporter:
    def __init__(self, block_1, block_2):
        self.block_1 = block_1
        self.block_2 = block_2

    def check_teleport(self, *args):
        for other in args:
            if pygame.Rect.colliderect(self.block_1, other):
                other.x, other.y = (self.block_2.x - self.block_2.width), self.block_2.y
            elif pygame.Rect.colliderect(self.block_2, other):
                other.x, other.y = (self.block_1.x + self.block_1.width), self.block_1.y


class Maze:

    def __init__(self, screen, maze_map_file):
        self.screen = screen

        self.color1 = (0, 250, 0)
        self.color2 = (0, 0, 250)
        self.color3 = (250, 0, 0)
        self.tiles = []
        self.width, self.height = (20, 20)
        self.layout = loadtxt(maze_map_file, dtype=str)
        self.rows, self.cols = self.layout.shape

        self.map_file = maze_map_file
        self.block_size = 20
        self.block_image = pygame.Surface((self.block_size, self.block_size))   # create a block surface
        self.block_image.fill(self.color1)

        self.shield_image = pygame.Surface((self.block_size, self.block_size // 2))     # create a shield surface
        self.shield_image.fill(self.color2)
        self.pellet_image = pygame.Surface((self.block_size // 4, self.block_size // 4))   # create a pellet surface

        pygame.draw.circle(self.pellet_image, self.color3,   # draw pellet onto pellet surface
                           (self.block_size // 8, self.block_size // 8), self.block_size // 8)
        self.ppellet_image = pygame.Surface((self.block_size // 2, self.block_size // 2))  # create a pellet surface
        pygame.draw.circle(self.ppellet_image, self.color1,  # draw power pellet onto pellet surface
                           (self.block_size // 4, self.block_size // 4), self.block_size // 4)
        self.map_lines = self.layout
        self.maze_blocks = pygame.sprite.Group()
        self.shield_blocks = pygame.sprite.Group()
        self.pellets = pygame.sprite.Group()
        self.power_pellets = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.teleport = None
        self.player_spawn = None
        self.ghost_spawn = []
        self.build_maze()

    def pellets_left(self):
        return True if self.pellets or self.power_pellets else False
    def build_maze(self):
        if self.maze_blocks or self.pellets or self.fruits or self.power_pellets or self.shield_blocks:
            self.maze_blocks.empty()
            self.pellets.empty()
            self.power_pellets.empty()
            self.fruits.empty()
            self.shield_blocks.empty()
        if len(self.ghost_spawn) > 0:
            self.ghost_spawn.clear()
        teleport_points = []
        for col in range(self.cols):
            for row in range(self.rows):
                value = self.layout[row][col]
                if value == 'x':
                    pos = (col * self.width, row * self.height)
                    self.maze_blocks.add(Tile(self.width, self.height, pos,
                                               self.block_image))
                elif value == '*':
                    pos = (col * self.width, row * self.height)
                    self.pellets.add(Tile(self.width, self.height, pos, self.pellet_image))
                elif value == 'f':
                    pos = (col * self.width, row * self.height)
                    self.fruits.add(Berry(self.width, self.height, pos))
                elif value == '@':
                    pos = (col * self.width, row * self.height)
                    self.power_pellets.add(Tile(self.width, self.height, pos,
                                                 self.ppellet_image))
                elif value == 's':
                    pos = (col * self.width, row * self.height)
                    self.shield_blocks.add(Tile(self.width, self.height, pos,
                                                 self.shield_image))

                elif value == 'o':
                    self.player_spawn = [(row, col), ((col * self.width) + self.block_size // 2,(row * self.height) + self.block_size // 2)]

                elif value == 'g':
                    pos = (col * self.width, row * self.height)
                    self.ghost_spawn.append(((row, col), pos))
                elif value == 't':
                    pos = (col * self.width, row * self.height)
                    teleport_points.append(pygame.Rect(pos, (self.block_size, self.block_size)))
            if len(teleport_points) == 2:
                self.teleport = Teleporter(teleport_points[0], teleport_points[1])

    def remove_shields(self):
        self.shield_blocks.empty()

    def blit(self):
        self.maze_blocks.draw(self.screen)
        self.pellets.draw(self.screen)
        self.power_pellets.draw(self.screen)
        self.fruits.draw(self.screen)
        self.shield_blocks.draw(self.screen)
