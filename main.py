import argparse
import pygame

from grid import Grid

parser = argparse.ArgumentParser(
    description='Conway\'s Game of Life',
    epilog='Pause with Space Key. When paused, reset with R Key, draw with left'
           'mouse button and erase with right mouse button'
)

parser.add_argument('--elite', action='store_true',
                    help='enable elite in the game')

parser.add_argument('--random', action='store_true',
                    help='start the game in a random state')

parser.add_argument('--fullscreen', action='store_true',
                    help='start the game in fullscreen mode')

args = parser.parse_args()

width, height = size = (600, 400)

pygame.init()
pygame.display.set_caption('Conway\'s Game Of Life')

if args.fullscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
fps = 20

background = (40, 42, 54)
screen.fill(background)

grid = Grid(screen, random=args.random, elite=args.elite)
grid.draw()
pygame.display.update()

# The first stands for drawing state, the second, for erasing state
mouse_state = [False, False]

running = True
pause = True

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
                grid.reset()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_state[0] = True
                mouse_state[1] = False
            
            if event.button == 3:
                mouse_state[1] = True
                mouse_state[0] = False

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_state[0] = False

            if event.button == 3:
                mouse_state[1] = False

    if pause:
        if any(mouse_state):
            grid.handle_mouse(pygame.mouse.get_pos(), mouse_state)
    else:
        grid.draw()
        pygame.display.update()
        grid.game.update()

pygame.quit()
