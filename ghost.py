import pygame
from pygame.sprite import Sprite
from images import ImageManager
from colors import Colors


class Ghost(Sprite):

    def __init__(self, screen, maze, info, file):
        super().__init__()
        self.screen = screen
        self.maze = maze

        self.kill_able = ImageManager('img/Gos.png', sheet=True, pos_offsets=[(0, 32 * 8, 32, 32), (0, 32*9, 32, 32)],
                                    resize=(self.maze.block_size, self.maze.block_size),
                                     animation_delay=150)

        self.orange = ImageManager('img/Gos.png', sheet=True, pos_offsets=[(0, 32 * 0, 32, 32), (0, 32*1, 32, 32)],
                                        resize=(self.maze.block_size, self.maze.block_size),
                                        animation_delay=250)
        self.red = ImageManager('img/Gos.png', sheet=True, pos_offsets=[(0, 32*2, 32, 32), (0, 32*3, 32, 32)],
                                         resize=(self.maze.block_size, self.maze.block_size),
                                         animation_delay=250)
        self.cyan = ImageManager('img/Gos.png', sheet=True, pos_offsets=[(0, 32*4, 32, 32), (0, 32*5, 32, 32)],
                                         resize=(self.maze.block_size, self.maze.block_size),
                                         animation_delay=250)
        self.pink = ImageManager('img/Gos.png', sheet=True, pos_offsets=[(0, 32*6, 32, 32), (0, 32*7, 32, 32)],
                                         resize=(self.maze.block_size, self.maze.block_size),
                                         animation_delay=250)

        self.images = self.red
        if file == 'orange':
            self.images = self.orange
        elif file == 'cyan':
            self.images = self.cyan
        elif file == 'pink':
            self.images = self.pink

        self.score_font = pygame.font.Font('fonts/Lumberjack-Regular.ttf', 18)
        self.score_image = None
        self.image, self.rect = self.images.get_image()
        self.return_tile = info[0]
        self.eaten_time = None
        self.start_pos = info[1]
        self.reset_position()

        self.on = False
        self.kill = False
        self.ret = False

    def reset_position(self):
        self.rect.left, self.rect.top = self.start_pos

    def set_eaten(self):
        self.ret = True
        self.kill = False
        self.image = self.score_font.render('200', True, Colors().white)

    def trigger(self):
        if not self.ret:
            self.kill = True
            self.image, _ = self.kill_able.get_image()

    def enable(self):
        self.on = True

    def update_normal(self):
        self.image = self.images.next_image()

    def update_blue(self):
        self.image = self.kill_able.next_image()

    def update(self):
        if self.on:
            if not self.kill:
                self.update_normal()
            else:
                self.update_blue()

    def blit(self):
        self.screen.blit(self.image, self.rect)

