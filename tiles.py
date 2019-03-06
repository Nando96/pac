from pygame.sprite import Sprite
from pygame import Rect


class Tile(Sprite):
    def __init__(self, width, height, pos, image):
        Sprite.__init__(self)
        x, y = pos
        self.rect = Rect(x, y, width, height)
        self.image = image
