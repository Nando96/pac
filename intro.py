import pygame
from image_manager import ImageManager
from score import ScoreBoard


class SimpleAnimation(pygame.sprite.Sprite):
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
                                             resize=resize).all_images()[0]     # grab first image in detail sheet

            self.image.blit(self.detail_piece, (0, 0))  # combine detail
        else:
            self.detail_piece = None
        self.rect.centerx, self.rect.centery = pos

    def update(self):
        self.image = self.image_manager.next_image()
        if self.detail_piece:
            self.image.blit(self.detail_piece, (0, 0))     # combine detail

    def blit(self):
        self.screen.blit(self.image, self.rect)


class TitleCard(pygame.sprite.Sprite):
    def __init__(self, screen, text,  pos=(0, 0), color=(250,250,250), size=42):
        super().__init__()
        self.screen = screen
        self.text = text
        self.color = color
        self.font = pygame.font.Font('fonts/PAC-FONT.TTF', size)
        self.image = None
        self.rect = None
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

        self.ghost_orange = SimpleAnimation(screen, 'img/Gos.png',
                                            sheet_offsets=[(0, 0, 32, 32), (0, 32, 32, 32)],
                                            pos=(self.title_card.rect.right + self.title_card.rect.width // 2,
                                                 screen.get_height() / 2),
                                            frame_delay=150)

        self.ghost_red = SimpleAnimation(screen, 'img/Gos.png', sheet_offsets=[(0, 32 * 2, 32, 32), (0, 32 * 3, 32, 32)],
                                         pos=(self.title_card.rect.right + self.title_card.rect.width // 2,
                                              screen.get_height() / 2),
                                         frame_delay=150)
        self.ghost_cyan = SimpleAnimation(screen, 'img/Gos.png',
                                          sheet_offsets=[(0, 32 * 4, 32, 32), (0, 32 * 5, 32, 32)],
                                          pos=(self.title_card.rect.right + self.title_card.rect.width // 2,
                                               screen.get_height() / 2),
                                          frame_delay=150)
        self.ghost_pink = SimpleAnimation(screen, 'img/Gos.png',
                                          sheet_offsets=[(0, 32 * 6, 32, 32), (0, 32 * 7, 32, 32)],
                                          pos=(self.title_card.rect.right + self.title_card.rect.width // 2,
                                               screen.get_height() / 2),
                                          frame_delay=150)
        self.pac_man = SimpleAnimation(screen, 'img/Pac.png',
                                          sheet_offsets=[(0, 32 * 0, 32, 32), (0, 32 * 1, 32, 32), (0, 32 * 2, 32, 32), (0, 32 * 3, 32, 32)],
                                          pos=(self.title_card.rect.right + self.title_card.rect.width // 2,
                                               screen.get_height() // 2),
                                          frame_delay=150)
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
        """Update ghost animations in title card"""
        self.ghost.update()

    def blit(self):
        """Blit the components of the ghost intro to the screen"""
        self.title_card.blit()
        self.ghost.blit()


class Intro:
    def __init__(self, screen):
        self.screen = screen
        self.Char_intros = [
            CharIntro(screen, 'pac', 'PacMan'),
            CharIntro(screen, 'red', 'Blinky'),
            CharIntro(screen, 'pink', 'Pinky'),
            CharIntro(screen, 'cyan', 'Inky'),
            CharIntro(screen, 'orange', 'Clyde')
        ]
        self.run = set()
        self.intro_index = 0
        self.last_intro_start = None
        self.intro_time = 3000  # time to display in milliseconds

    def update(self):
        if not self.last_intro_start:
            self.last_intro_start = pygame.time.get_ticks()
        elif abs(self.last_intro_start - pygame.time.get_ticks()) > self.intro_time:
            self.run.add(self.intro_index)
            self.intro_index = (self.intro_index + 1) % len(self.Char_intros)
            self.last_intro_start = pygame.time.get_ticks()
        if self.intro_index in (0, 1) and self.intro_index in self.run:
            self.run.remove(self.intro_index)
        self.Char_intros[self.intro_index].update()

    def blit(self):
        self.Char_intros[self.intro_index].blit()
