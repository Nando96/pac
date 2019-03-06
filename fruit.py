from Tiles import Tile
from image_manager import ImageManager


class Berry(Tile):
    def __init__(self,width, height,pos):
        img, _ = ImageManager('img/berry.png', resize=(width // 2, height // 2)).get_image()
        super(Berry, self).__init__(width, height, pos, img)
