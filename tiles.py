from pygame.sprite import Sprite
from pygame import Rect


class Block(Sprite):
    def __init__(self, w, h, pos, image):
        Sprite.__init__(self)
        x, y = pos
        self.rect = Rect(x, y, w, h)
        self.image = image
