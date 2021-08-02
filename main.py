import argparse
import pygame

from grid import Grid

parser = argparse.ArgumentParser(
    description='Conway\'s Game of Life',
    epilog='Pause with Space Key. When paused, reset with R Key'
)

parser.add_argument('--elite', action='store_true',
                    help='enable elite in the game')

args = parser.parse_args()

width, height = size = (1608, 905)

pygame.init()
pygame.display.set_caption('Conway\'s Game Of Life')
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 5

background = (40, 42, 54)

grid = Grid(screen, random=True, elite=args.elite)

running = True
pause = False

while running:

    clock.tick(fps)
    screen.fill(background)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE:
                pause = not pause

            if pause and event.key == pygame.K_r:
                grid.game.reset()

    grid.draw()
    pygame.display.update()

    if not pause:
        grid.game.update()

pygame.quit()
