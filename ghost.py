from pygame import time, sysfont
from pygame.sprite import Sprite
from image_manager import ImageManager


class Ghost(Sprite):

    def __init__(self, screen, maze, target, spawn_info, ghost_file):
        super().__init__()
        self.screen = screen
        self.maze = maze
        self.target = target

        self.killable = ImageManager('img/Gos.png', sheet=True, pos_offsets=[(0, 32 * 8, 32, 32), (0, 32*9, 32, 32)],
                                        resize=(self.maze.block_size, self.maze.block_size),
                                        animation_delay=150)

        self.ghost_orange = ImageManager('img/Gos.png', sheet=True, pos_offsets=[(0, 32 * 0, 32, 32), (0, 32*1, 32, 32)],
                                        resize=(self.maze.block_size, self.maze.block_size),
                                        animation_delay=250)
        self.ghost_red = ImageManager('img/Gos.png', sheet=True, pos_offsets=[(0, 32*2, 32, 32), (0, 32*3, 32, 32)],
                                         resize=(self.maze.block_size, self.maze.block_size),
                                         animation_delay=250)
        self.ghost_cyan = ImageManager('img/Gos.png', sheet=True, pos_offsets=[(0, 32*4, 32, 32), (0, 32*5, 32, 32)],
                                         resize=(self.maze.block_size, self.maze.block_size),
                                         animation_delay=250)
        self.ghost_pink = ImageManager('img/Gos.png', sheet=True, pos_offsets=[(0, 32*6, 32, 32), (0, 32*7, 32, 32)],
                                         resize=(self.maze.block_size, self.maze.block_size),
                                         animation_delay=250)

        self.norm_images = self.ghost_red
        if ghost_file == 'orange':
            self.norm_images = self.ghost_orange
        elif ghost_file == 'cyan':
            self.norm_images = self.ghost_cyan
        elif ghost_file == 'pink':
            self.norm_images = self.ghost_pink
        self.score_font = sysfont.SysFont(None, 22)
        self.score_image = None
        self.image, self.rect = self.norm_images.get_image()
        self.return_tile = spawn_info[0]    # spawn tile
        self.eaten_time = None   # timestamp for being eaten
        self.start_pos = spawn_info[1]
        self.reset_position()
        self.state = {'enabled': False, 'blue': False, 'return': False}
        self.blue_interval = 5000   # 5 second time limit for blue status
        self.blue_start = None  # timestamp for blue status start




    def reset_position(self):
        """Hard reset the ghost position back to its original location"""
        self.rect.left, self.rect.top = self.start_pos


    def set_eaten(self):
        self.state['return'] = True
        self.state['blue'] = False
        self.tile = (self.get_nearest_row(), self.get_nearest_col())
        self.image = self.score_font.render('200', True, (255, 255, 255))
        self.eaten_time = time.get_ticks()



    def begin_blue_state(self):
        """Switch the ghost to its blue state"""
        if not self.state['return']:
            self.state['blue'] = True
            self.image, _ = self.killable.get_image()
            self.blue_start = time.get_ticks()





    def get_nearest_col(self):
        """Get the current column location on the maze map"""
        return (self.rect.left - (self.screen.get_width() // 5)) // self.maze.block_size

    def get_nearest_row(self):
        """Get the current row location on the maze map"""
        return (self.rect.top - (self.screen.get_height() // 12)) // self.maze.block_size



    def enable(self):
        self.state['enabled'] = True


    def killable_stop(self, resume_audio=True):
        """Revert back from blue state"""
        self.state['blue'] = False
        self.state['return'] = False
        self.image, _ = self.norm_images.get_image()




    def update_normal(self):
        self.image = self.norm_images.next_image()

    def update_blue(self):
        """Update logic for blue state"""
        self.image = self.killable.next_image()

        if abs(self.blue_start - time.get_ticks()) > self.blue_interval:
            self.killable_stop()



    def update(self):
        """Update the ghost position"""
        if self.state['enabled']:
            if not self.state['blue']:
                self.update_normal()
            elif self.state['blue']:
                self.update_blue()


    def blit(self):
        """Blit ghost image to the screen"""
        self.screen.blit(self.image, self.rect)
