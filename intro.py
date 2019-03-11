from intro_help import *


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
