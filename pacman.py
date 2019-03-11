import pygame
from images import ImageManager


class PacMan(pygame.sprite.Sprite):
    def __init__(self, screen, maze):
        super().__init__()
        self.screen = screen
        self.maze = maze
        self.push = 3
        self.death = ImageManager('img/Pac.png', sheet=True, pos_offsets=[(0, 32 * 16, 32, 32),
                                                                          (0, 32 * 17, 32, 32),
                                                                          (0, 32*18, 32, 32),
                                                                          (0, 32*19, 32, 32),
                                                                          (0, 32*20, 32, 32),
                                                                          (0, 32*21, 32, 32)],
                                  resize=(self.maze.block_size - 4, self.maze.block_size - 4),
                                  animation_delay=150, repeat=False)
        self.up = ImageManager('img/Pac.png', sheet=True, pos_offsets=[(0, 32 * 4, 32, 32),
                                                                       (0, 32 * 5, 32, 32),
                                                                       (0, 32 * 6, 32, 32),
                                                                       (0, 32 * 7, 32, 32)],
                               resize=(self.maze.block_size-4, self.maze.block_size-4))
        self.down = ImageManager('img/Pac.png', sheet=True, pos_offsets=[(0, 32 * 12, 32, 32),
                                                                         (0, 32 * 13, 32, 32),
                                                                         (0, 32 * 14, 32, 32),
                                                                         (0, 32 * 15, 32, 32)],
                                 resize=(self.maze.block_size-4, self.maze.block_size-4))
        self.left = ImageManager('img/Pac.png', sheet=True, pos_offsets=[(0, 32 * 8, 32, 32),
                                                                         (0, 32 * 9, 32, 32),
                                                                         (0, 32 * 10, 32, 32),
                                                                         (0, 32 * 11, 32, 32)],
                                 resize=(self.maze.block_size-4, self.maze.block_size-4))
        self.right = ImageManager('img/Pac.png', sheet=True, pos_offsets=[(0, 0, 32, 32),
                                                                          (0, 32 * 1, 32, 32),
                                                                          (0, 32 * 2, 32, 32),
                                                                          (0, 32 * 3, 32, 32)],
                                  resize=(self.maze.block_size-4, self.maze.block_size-4))

        self.spawn_info = self.maze.player_spawn[1]
        self.tile = self.maze.player_spawn[0]
        self.direction = None
        self.moving = False
        self.image, self.rect = self.right.get_image()
        self.rect.centerx, self.rect.centery = self.spawn_info   # screen coordinates for spawn
        self.dead = False
        self.event_map = {pygame.KEYDOWN: self.action, pygame.KEYUP: self.reset_direction}

    def set_death(self):
        self.dead = True
        self.image, _ = self.death.get_image()

    def revive(self):
        self.dead = False
        self.image, _ = self.right.get_image()
        self.death.image_index = 0

    def reset_position(self):
        self.rect.centerx, self.rect.centery = self.spawn_info  # screen coordinates for spawn

    def reset_direction(self, event):
        if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            self.moving = False

    def action(self, event):
        if event.key == pygame.K_UP:
            self.set_move_up()
        if event.key == pygame.K_DOWN:
            self.set_move_down()
        if event.key == pygame.K_LEFT:
            self.set_move_left()
        if event.key == pygame.K_RIGHT:
            self.set_move_right()

    def set_move_up(self):
        if self.direction != 'u':
            self.direction = 'u'
        self.moving = True

    def set_move_left(self):
        if self.direction != 'l':
            self.direction = 'l'
        self.moving = True

    def set_move_down(self):
        if self.direction != 'd':
            self.direction = 'd'
        self.moving = True

    def set_move_right(self):
        if self.direction != 'r':
            self.direction = 'r'
        self.moving = True

    def push_back(self):
        if self.direction == 'l':
            self.rect.x += self.push
        elif self.direction == 'r':
            self.rect.x -= self.push
        if self.direction == 'u':
            self.rect.y += self.push
        elif self.direction == 'd':
            self.rect.y -= self.push

    def pos_test(self):
        test = self.rect
        if self.direction == 'l':

            test = self.rect.move((-1, 0))
        elif self.direction == 'r':

            test = self.rect.move((+1, 0))
        if self.direction == 'u':

            self.rect.move((0, -1))
        elif self.direction == 'd':

            self.rect.move((0, +1))
        return test

    def is_blocked(self):
        while pygame.sprite.spritecollideany(self, self.maze.maze_blocks):
                self.push_back()

    def collide(self):
        score = 0
        fruit_count = 0
        power = None
        if pygame.sprite.spritecollideany(self, self.maze.pellets):
            pygame.sprite.spritecollideany(self, self.maze.pellets).kill()
            score += 10
        elif pygame.sprite.spritecollideany(self, self.maze.fruits):
            pygame.sprite.spritecollideany(self, self.maze.fruits).kill()
            score += 20
            fruit_count += 1

        elif pygame.sprite.spritecollideany(self, self.maze.power_pellets):
            pygame.sprite.spritecollideany(self, self.maze.power_pellets).kill()
            score += 20
            power = True
        return score, fruit_count, power

    def update(self):
        if not self.dead:
            self.is_blocked()
            if self.direction and self.moving:
                if self.direction == 'u':
                    self.image = self.up.next_image()
                elif self.direction == 'd':
                    self.image = self.down.next_image()
                elif self.direction == 'l':
                    self.image = self.left.next_image()
                elif self.direction == 'r':
                    self.image = self.right.next_image()

                if not self.is_blocked():
                    if self.direction == 'u':
                        self.rect.centery -= 1
                    elif self.direction == 'l':
                        self.rect.centerx -= 1
                    elif self.direction == 'd':
                        self.rect.centery += 1
                    elif self.direction == 'r':
                        self.rect.centerx += 1
        else:
            self.image = self.death.next_image()

    def blit(self):
        self.screen.blit(self.image, self.rect)
