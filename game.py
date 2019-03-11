import pygame
from loop import Events
from ghost import Ghost
from maze import Maze
from score import ScoreController
from menu import Menu, HighScoreScreen
from intro import Intro
from colors import Colors
from pacman import PacMan
from lives_status import Counter


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.music.load('sounds/Pac-Man-Theme-Song.mp3')
        self.screen = pygame.display.set_mode((550, 800))
        pygame.display.set_caption('PacMan Portal')
        self.clock = pygame.time.Clock()

        self.score_keeper = ScoreController(screen=self.screen, sb_pos=((self.screen.get_width() / 5),
                                                                        (self.screen.get_height() * 0.965)),
                                            items_image='img/berry.png', itc_pos=(int(self.screen.get_width() * 0.6),
                                            self.screen.get_height() * 0.965))
        self.maze = Maze(self.screen, 'maze.txt')
        self.life_counter = Counter(screen=self.screen, ct_pos=((self.screen.get_width() // 3),
                                                                      (self.screen.get_height() * 0.965)),
                                          images_size=(self.maze.block_size, self.maze.block_size))
        self.game_over = True
        self.player = PacMan(screen=self.screen, maze=self.maze)
        self.ghosts = pygame.sprite.Group()
        self.ghost_active_interval = 2500
        self.ghosts_to_activate = None
        self.first_ghost = None
        self.other_ghosts = []
        self.enemies()
        self.actions = {pygame.USEREVENT: self.reset_maze}

    def enemies(self):
        types = ['pink', 'cyan', 'red', 'orange']
        index = 0
        while len(self.maze.ghost_spawn) > 0:
            spawn_info = self.maze.ghost_spawn.pop()
            g = Ghost(screen=self.screen, maze=self.maze,
                      info=spawn_info, file=types[index])
            if types[index] == 'ghost-red.png':
                self.first_ghost = g    # red ghost should be first
            else:
                self.other_ghosts.append(g)
            self.ghosts.add(g)
            index = (index + 1) % len(types)

    def reset_maze(self):
        if self.life_counter.lives > 0:
            pygame.mixer.music.stop()
            self.maze.build_maze()
            self.player.reset_position()
            if self.player.dead:
                self.player.revive()
        else:
            self.game_over = True

    def check_player(self):
        n_score, n_fruits, power = self.player.collide()
        self.score_keeper.add_score(n_score, n_fruits)
        if power:
            for g in self.ghosts:
                g.trigger()
        ghost_collide = pygame.sprite.spritecollideany(self.player, self.ghosts)
        if ghost_collide and ghost_collide.kill:
            ghost_collide.set_eaten()
            self.score_keeper.add_score(200)
        elif ghost_collide and not (self.player.dead or ghost_collide.ret):
            self.life_counter.decrement()
            self.player.set_death()
            for g in self.ghosts:
                if g.state.on:
                    g.disable()

    def update_screen(self):
        if not self.player.dead:
            self.screen.fill(Colors().black)
            self.check_player()
            self.maze.blit()
            self.player.update()
            for enemy in self.ghosts:
                enemy.update()
                enemy.blit()
            self.player.blit()
            self.score_keeper.blit()
            self.life_counter.blit()
        elif self.player.dead:
            self.player.update()
            self.player.blit()

        pygame.display.flip()

    def play(self):
        menu = Menu(self.screen)
        hs_screen = HighScoreScreen(self.screen, self.score_keeper)
        intro_seq = Intro(self.screen)
        loop = Events(runs=True, actions={pygame.MOUSEBUTTONDOWN: menu.check})

        while loop.runs:
            self.clock.tick(60)
            loop.check_events()
            self.screen.fill((0, 0, 0))
            if not menu.hs_screen:
                intro_seq.update()
                intro_seq.blit()
                menu.update()
                menu.blit()
            else:
                hs_screen.blit()
                hs_screen.check_done()
            if menu.ready_to_play:
                pygame.mixer.music.stop()
                pygame.mixer.music.load('sounds/waka.wav')
                pygame.mixer.music.play()
                self.play_game()
                menu.ready_to_play = False
                self.score_keeper.save_high_scores()
                hs_screen.prep_images()
                hs_screen.position()
            elif not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
            pygame.display.flip()

    def play_game(self):
        loop = Events(True, {**self.player.event_map, **self.actions})
        self.game_over = False
        if self.player.dead:
            self.player.revive()
            self.score_keeper.reset_level()
            self.life_counter.reset_counter()
            self.reset_maze()

        while loop.runs:
            loop.check_events()
            self.update_screen()
            if self.game_over:
                pygame.mixer.stop()
                self.score_keeper.reset_level()
                loop.runs = False


game = Game()
game.play()
