import numpy as np
import pygame
from time import sleep

DEBUG = 1


def print_debug(arg):
    if DEBUG:
        print(arg)


def swap(a, b):
    a, b = b, a
    return a, b


def selected_colour():
    if selected:
        return (255, 255, 0)
    else:
        return (125, 125, 125)


def update():
    global SCORE
    DISPLAY.fill(colour_map[WHITE])
    for i in range(0, 10):
        for j in range(0, 10):
            rectangle = pygame.Rect(i*WIDTH_STEP, j*HEIGHT_STEP, WIDTH_STEP, HEIGHT_STEP)
            pygame.draw.rect(DISPLAY, colour_map[game_table[i][j]], rectangle)
    selected_rectangle = pygame.Rect(selectedX*WIDTH_STEP, selectedY*HEIGHT_STEP, WIDTH_STEP, HEIGHT_STEP)
    pygame.draw.rect(DISPLAY, selected_colour(), selected_rectangle, 4)

    text = BASICFONT.render(str(SCORE), 1, (255, 165, 0))
    textpos = text.get_rect(centerx=DISPLAY.get_width()/2)
    DISPLAY.blit(text, textpos)

    pygame.display.flip()
    FPSCLOCK.tick(FPS)


def evaluate(SCORE):
    while True:
        score, recheck = update_table()
        SCORE += score
        update()
        if not recheck:
            break
    return SCORE

def update_table():
    retrace_list = []
    score = 0
    recheck = False
    for i in range(0, ROWS):
        matches = 0
        for j in range(0, COLS):
            # potentially unsafe but python should take the easy route out
            if j >= COLS - 1 or game_table[i][j] != game_table[i][j+1]:
                if matches >= 2:
                    retrace_list.append( (i, j, 1, matches) )
                    score += 2**matches
                matches = 0
            else:
                matches += 1

    for j in range(0, COLS):
        matches = 0
        for i in range(0, ROWS):
            if i >= ROWS - 1 or game_table[i][j] != game_table[i+1][j]:
                if matches >= 2:
                    retrace_list.append( (i, j, 0, matches) )
                    score += 2**matches
                matches = 0
            else:
                matches += 1

    if retrace_list:
        recheck = True
    for elem in retrace_list:
        retrace(*elem)

    return score, recheck


def retrace(i, j, axis, matches):
    for k in range(-matches, 0+1):
        if axis:
            game_table[i][j+k] = np.random.choice(colours)
        else:
            game_table[i+k][j] = np.random.choice(colours)

FPS = 30

BLACK = 0
WHITE = 1
BLUE = 2
GREEN = 3
RED = 4

ROWS = 10
COLS = 10

WIDTH = 800
WIDTH_STEP = int(WIDTH/10)
HEIGHT = 600
HEIGHT_STEP = int(HEIGHT/10)

SCORE = 0

UP = pygame.K_UP
DOWN = pygame.K_DOWN
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT
SPACE = pygame.K_SPACE
acceptable_keys = [UP, DOWN, LEFT, RIGHT, SPACE]

colours = [BLACK, WHITE, BLUE, GREEN, RED]
colour_map = {BLACK: (0, 0, 0), WHITE: (255, 255, 255), BLUE: (0, 0, 255),
              GREEN: (0, 255, 0), RED: (255, 0, 0)}

if DEBUG:
    game_table = np.random.choice(colours, ROWS * COLS)
    game_table.resize(ROWS, COLS)
    print_debug(game_table)


pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bijouweled v0.1')
BASICFONT = pygame.font.Font('freesansbold.ttf', 36)

# generate table and draw to screen
game_table = np.random.choice(colours, ROWS * COLS)
game_table.resize(ROWS, COLS)
selected = False
selectedX = 0
selectedY = 0
update()

done = False
while not done:
    SCORE = evaluate(SCORE)
    # register user event
    event = pygame.event.wait()
    # exit
    if event.type == pygame.QUIT:
        done = True
    # process key and act accordingly
    if event.type == pygame.KEYDOWN and event.key in acceptable_keys:
        key = event.key
        if key == SPACE:
            selected = not(selected)
        elif key == UP:
            if selectedY - 1 >= 0:
                SCORE -= 1
                if selected:
                    game_table[selectedX, selectedY], game_table[selectedX, selectedY - 1] = game_table[selectedX, selectedY - 1], game_table[selectedX, selectedY],
                    selected = False
                selectedY -= 1
        elif key == DOWN:
            if selectedY < 9:
                SCORE -= 1
                if selected:
                    game_table[selectedX, selectedY], game_table[selectedX, selectedY + 1] = game_table[selectedX, selectedY + 1], game_table[selectedX, selectedY],
                    selected = False
                selectedY += 1
        elif key == LEFT:
            if selectedX - 1 >= 0:
                SCORE -= 1
                if selected:
                    game_table[selectedX, selectedY], game_table[selectedX - 1, selectedY] = game_table[selectedX - 1, selectedY], game_table[selectedX, selectedY],
                    selected = False
                selectedX -= 1
        elif key == RIGHT:
            if selectedX < 9:
                SCORE -= 1
                if selected:
                    game_table[selectedX, selectedY], game_table[selectedX + 1, selectedY] = game_table[selectedX + 1, selectedY], game_table[selectedX, selectedY],
                    selected = False
                selectedX += 1

        update()

pygame.quit()