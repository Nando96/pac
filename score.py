import json
import pygame
from colors import Colors


class ScoreBoard:

    def __init__(self, screen, pos=(0, 0)):
        self.screen = screen
        self.score = 0
        self.color = Colors().white
        self.font = pygame.font.Font('fonts/Lumberjack-Regular.ttf', 32)
        self.prep_image()
        self.pos = pos
        self.position()

    def position(self):
        self.rect.centerx, self.rect.centery = self.pos

    def prep_image(self):
        score_str = str(self.score)
        self.image = self.font.render(score_str, True, self.color)
        self.rect = self.image.get_rect()

    def reset(self):
        self.score = 0
        self.prep_image()
        self.position()

    def update(self, n_score):
        self.score += n_score
        self.prep_image()
        self.position()

    def blit(self):
        self.screen.blit(self.image, self.rect)


class ItemCounter:
    def __init__(self, screen, image_name, pos=(0, 0)):
        self.screen = screen
        self.counter = 0
        self.item_image = pygame.image.load(image_name)
        self.item_rect = self.item_image.get_rect()
        self.font = pygame.font.Font('fonts/Lumberjack-Regular.ttf', 36)
        self.color = (250, 250, 250)
        self.text_image = None
        self.text_rect = None
        self.pos = pos
        self.prep_image()

    def add_items(self, n_items):
        self.counter += n_items
        self.prep_image()

    def reset_items(self):
        self.counter = 0
        self.prep_image()

    def prep_image(self):
        text = str(self.counter) + ' X '
        self.text_image = self.font.render(text, True, self.color)
        self.text_rect = self.text_image.get_rect()
        self.position()

    def position(self):
        self.text_rect.centerx, self.text_rect.centery = self.pos
        x_offset = int(self.text_rect.width * 1.25)
        self.item_rect.centerx, self.item_rect.centery = self.pos[0] + x_offset, self.pos[1]

    def blit(self):
        self.screen.blit(self.text_image, self.text_rect)
        self.screen.blit(self.item_image, self.item_rect)


class ScoreController:
    def __init__(self, screen, items_image, sb_pos=(0, 0), itc_pos=(0, 0)):
        self.score = 0
        self.level = 1
        self.high_scores = []
        self.scoreboard = ScoreBoard(screen, sb_pos)
        self.item_counter = ItemCounter(screen=screen, pos=itc_pos, image_name=items_image)
        self.init_high_scores()

    def increment_level(self, up=1):
        self.level += up

    def init_high_scores(self):
        try:
            with open('score_data.json', 'r') as file:
                self.high_scores = json.load(file)
                self.high_scores.sort(reverse=True)
        except (FileNotFoundError, ValueError, EOFError, json.JSONDecodeError) as e:
            print(e)
            self.high_scores = [0, 0, 0, 0, 0]

    def save_high_scores(self):
        for i in range(len(self.high_scores)):
            if self.score >= self.high_scores[i]:
                self.high_scores[i] = self.score
                break
        with open('score_data.json', 'w') as file:
            json.dump(self.high_scores, file)

    def reset_level(self):
        self.level = 1
        self.scoreboard.reset()
        self.item_counter.reset_items()

    def add_score(self, score, items=None):
        self.scoreboard.update(score)
        self.score = self.scoreboard.score
        if items:
            self.item_counter.add_items(items)

    def blit(self):
        self.scoreboard.blit()
        self.item_counter.blit()