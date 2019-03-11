import pygame
from sys import exit


class Events:
    def __init__(self, runs=False, actions=None):
        self.action_map = {pygame.QUIT: exit, }
        if isinstance(actions, dict):
            self.action_map.update(actions)
        self.runs = runs

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.action_map[event.type]()
            elif event.type in self.action_map:
                try:
                    self.action_map[event.type](event)
                except TypeError:
                    self.action_map[event.type]()
