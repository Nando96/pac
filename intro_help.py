import pygame
from images import ImageManager
from colors import Colors


class Animate(pygame.sprite.Sprite):
    def __init__(self, screen, sprite_sheet, sheet_offsets, pos=(0, 0), resize=None,
                 detail=None, frame_delay=None):
        super().__init__()
        self.screen = screen
        if not resize:
            resize = (self.screen.get_height() // 10, self.screen.get_height() // 10)
        self.image_manager = ImageManager(sprite_sheet, sheet=True, pos_offsets=sheet_offsets,
                                          resize=resize, animation_delay=frame_delay)

        self.image, self.rect = self.image_manager.get_image()
        if detail:
            self.detail_piece = ImageManager(detail, sheet=True, pos_offsets=sheet_offsets,
                                             resize=resize).all_images()[0]

            self.image.blit(self.detail_piece, (0, 0))
        else:
            self.detail_piece = None
        self.rect.centerx, self.rect.centery = pos

    def update(self):
        self.image = self.image_manager.next_image()
        if self.detail_piece:
            self.image.blit(self.detail_piece, (0, 0))

    def blit(self):
        self.screen.blit(self.image, self.rect)


class TitleCard(pygame.sprite.Sprite):
    def __init__(self, screen, text,  pos=(0, 0), size=50):
        super().__init__()
        self.screen = screen
        self.text = text
        self.color = Colors().white
        self.font = pygame.font.Font('fonts/PAC-FONT.TTF', size)
        self.pos = pos
        self.prep_image()

    def position(self, n_pos=None):
        if not n_pos:
            self.rect.centerx, self.rect.centery = self.pos
        else:
            self.rect.centerx, self.rect.centery = n_pos

    def prep_image(self):
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.position()

    def blit(self):
        self.screen.blit(self.image, self.rect)


class CharIntro:
    def __init__(self, screen, type, name):
        self.screen = screen
        self.title_card = TitleCard(screen, name, pos=(screen.get_width() // 2, screen.get_height() // 2))

        self.ghost_orange = Animate(screen, 'img/Gos.png',
                                            sheet_offsets=[(0, 0, 32, 32), (0, 32, 32, 32)],
                                    pos=(screen.get_width() / 2,
                                         (screen.get_height() / 2 - 120)),
                                    frame_delay=100)

        self.ghost_red = Animate(screen, 'img/Gos.png', sheet_offsets=[(0, 32 * 2, 32, 32), (0, 32 * 3, 32, 32)],
                                 pos=(screen.get_width() / 2,
                                      (screen.get_height() / 2 - 120)),
                                 frame_delay=100)
        self.ghost_cyan = Animate(screen, 'img/Gos.png',
                                          sheet_offsets=[(0, 32 * 4, 32, 32), (0, 32 * 5, 32, 32)],
                                  pos=(screen.get_width() / 2,
                                       (screen.get_height() / 2 - 120)),
                                  frame_delay=100)
        self.ghost_pink = Animate(screen, 'img/Gos.png',
                                          sheet_offsets=[(0, 32 * 6, 32, 32), (0, 32 * 7, 32, 32)],
                                  pos=(screen.get_width() / 2,
                                       (screen.get_height() / 2 - 120)),
                                  frame_delay=100)
        self.pac_man = Animate(screen, 'img/Pac.png',
                                          sheet_offsets=[(0, 32 * 0, 32, 32), (0, 32 * 1, 32, 32), (0, 32 * 2, 32, 32), (0, 32 * 3, 32, 32)],
                                          pos=(screen.get_width() / 2,
                                               (screen.get_height() / 2 - 120)),
                                          frame_delay=100)
        if type == 'red':
            self.ghost = self.ghost_red
        elif type == 'orange':
            self.ghost = self.ghost_orange
        elif type == 'cyan':
            self.ghost = self.ghost_cyan
        elif type == 'pink':
            self.ghost = self.ghost_pink
        else:
            self.ghost = self.pac_man

    def update(self):
        self.ghost.update()

    def blit(self):
        self.title_card.blit()
        self.ghost.blit()
