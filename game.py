import pygame
from tiles import Tile
from numpy import loadtxt

pygame.init()
screen = pygame.display.set_mode((1200, 1200), 0, 32)
width, height = (32, 32)
tiles = []
layout = loadtxt('maze.txt', dtype=str)
rows, cols = layout.shape
for col in range(cols):
    for row in range(rows):
        value = layout[row][col]
        if value != '0':
            pos = (col*width, row*height)
            tiles.append(Tile(width, height, pos, screen))
            print(width, height, pos)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    for tile in tiles:
        tile.blitme()
    pygame.display.flip()
    pygame.display.update()
