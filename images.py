import pygame


class ImageManager:
    def __init__(self, img, sheet=False, pos_offsets=None,
                 resize=None, keys=None,
                 convert=True, transparency=True,
                 animation_delay=None,
                 repeat=True):
        if not sheet:
            self.images = [pygame.image.load( img)]
        else:
            self.sheet = pygame.image.load(img)
            self.pos_offsets = pos_offsets
            self.images = self.extract_images()
        if resize:
            self.images = [pygame.transform.scale(img, resize) for img in self.images]
        self.rect = self.images[0].get_rect()
        if convert:
            self.images = [img.convert() for img in self.images]
        if transparency:
            for i in self.images:
                i.set_colorkey((0, 0, 0, 0))
        if keys:
            images_dict = dict()
            for k, i in zip(keys, range(len(self.images))):
                images_dict[k] = self.images[i]
            self.images = images_dict
        else:
            self.image_index = 0
        self.animation_delay = animation_delay
        self.time_stamp = pygame.time.get_ticks()
        self.repeat = repeat

    def get_image(self, key=None):
        if isinstance(self.images, list):
            return self.images[self.image_index], self.rect
        else:
            return self.images[key], self.rect

    def all_images(self):
        return self.images

    def next_image(self):

        if not self.repeat and self.image_index + 1 >= len(self.images):
            return self.images[self.image_index]

        if not self.animation_delay:
            self.image_index = (self.image_index + 1) % len(self.images)
        else:
            if abs(self.time_stamp - pygame.time.get_ticks()) > self.animation_delay:
                self.image_index = (self.image_index + 1) % len(self.images)
                self.time_stamp = pygame.time.get_ticks()

        return self.images[self.image_index]

    def extract_images(self):
        result = []
        for rect in self.pos_offsets:
            select = pygame.Rect(rect)
            sub_image = pygame.Surface(select.size).convert(pygame.display.get_surface())
            sub_image.blit(self.sheet, (0, 0), select)
            result.append(sub_image)
        return result
