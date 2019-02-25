import pygame
class Tile(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, width, height, pos, screen):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill((200, 200, 200))

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def blitme(self):
        self.screen.blit(self.image, self.rect)