from tiles import Block
from images import ImageManager


class Berry(Block):
    def __init__(self, w, h, pos):
        img, _ = ImageManager('img/berry.png', resize=(w // 2, h // 2)).get_image()
        super(Berry, self).__init__(w, h, pos, img)
