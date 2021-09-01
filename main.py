import pygame
from pygame.locals import *
from time import time
from random import sample
from tetromino import Tetromino
pygame.init()

screen = pygame.display.set_mode((500, 750))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

# generate game icon
icon = pygame.Surface((300, 300))
icon.fill((255, 255, 255))
icon.set_colorkey((255, 255, 255))
pygame.draw.polygon(icon, (200, 0, 255), ((0, 50), (300, 50), (300, 150), (200, 150), (200, 250), (100, 250),
                                          (100, 150), (0, 150)))
pygame.display.set_icon(icon)

# audio
pygame.mixer.music.load("aud/music/Tetris.ogg")
pygame.mixer.music.set_volume(.5)
pygame.mixer.music.play(-1)

# hold
hold = pygame.Surface((77, 77))
hold_rect = hold.get_rect()
pygame.draw.rect(hold, (255, 255, 255), (1, 1, 75, 75), 2)
hold_rect.x = 10
hold_rect.y = 75

# preview
preview = pygame.Surface((77, 252))
preview_rect = preview.get_rect()
pygame.draw.rect(preview, (255, 255, 255), (0, 0, 75, 250), 2)
preview_rect.x = 415
preview_rect.y = 75

# visual grid
display_grid = pygame.Surface((305, 605))
display_grid.fill((0, 0, 0))
display_grid.set_colorkey((0, 0, 0))
grid_colors = [(0, 0, 0), (0, 200, 255), (0, 100, 255), (255, 100, 0), (255, 225, 0), (0, 225, 50), (255, 0, 0),
               (200, 0, 255)]

# text
font = pygame.font.Font("pixel.ttf", 25)
next_t = font.render("Next", True, (255, 255, 255))
next_t_rect = next_t.get_rect()
next_t_rect.centerx = preview_rect.centerx + 1
next_t_rect.y = preview_rect.y - 35
hold_t = font.render("Hold", True, (255, 255, 255))
hold_t_rect = hold_t.get_rect()
hold_t_rect.centerx = hold_rect.centerx + 2
hold_t_rect.y = hold_rect.y - 35


# virtual grid
grid = [[0 for n in range(10)] for i in range(20)]


def generate_bag():
    global bags
    bag = sample([0, 1, 2, 3, 4, 5, 6], 7)
    bags += bag


# general variables
bags = []
generate_bag()
a_t = Tetromino(bags[0])  # active tetromino
bags.pop(0)
fall_timer = 0
lockdown = 0
min_x = 10
max_x = 0
ma_time = 0  # time when a move activation button was pressed
step_time = 0
held = 0
held_get = 0
place_ = False
holding = False
blocked = False
move = False
run = True


def draw_grid_pattern():
    for i in range(21):
        if i == 0:
            pygame.draw.line(display_grid, (255, 255, 255), (0, 0), (300, 0), 2)
        else:
            pygame.draw.line(display_grid, (255, 255, 255), (0, i * 30), (300, i * 30), 2)

    for i in range(11):
        if i == 0:
            pygame.draw.line(display_grid, (255, 255, 255), (0, 0), (0, 600), 2)
        else:
            pygame.draw.line(display_grid, (255, 255, 255), (i * 30, 0), (i * 30, 600), 2)


def update_grid():
    for row_i, row in enumerate(grid):
        for tile_i, tile in enumerate(row):
            pygame.draw.rect(display_grid, grid_colors[tile], (tile_i * 30, row_i * 30, 30, 30))
    a_t.ghost_piece(display_grid, grid)
    a_t.render(grid_colors, display_grid)
    draw_grid_pattern()


def place():
    global a_t, lockdown, holding, fall_timer
    for y_i_p, y_p in enumerate(a_t.shape[a_t.state]):
        for x_i_p, x_p in enumerate(y_p):
            if x_p == "0":
                grid[a_t.pos[1] + y_i_p][a_t.pos[0] + x_i_p] = a_t.shape_index + 1
    lockdown = 0
    holding = False
    fall_timer = 0
    a_t = Tetromino(bags[0])
    bags.pop(0)
    game_over()


def hard_drop():
    while True:
        a_t.pos[1] += 1
        if a_t.detect_collision(grid, a_t.pos):
            a_t.pos[1] -= 1
            place()
            break


def line_clear():
    fail = False
    for line_i, line in enumerate(grid):
        for tile in line:
            if tile == 0:
                fail = True
                break
        if not fail:
            grid.pop(line_i)
            grid.insert(0, [0 for i in range(10)])
        fail = False


def update_preview():
    preview.fill((0, 0, 0))
    pygame.draw.rect(preview, (255, 255, 255), (0, 0, 75, 250), 2)
    # pygame.draw.line(preview, (255, 255, 255), (0, 75), (75, 75), 2)
    for i in range(3):
        for y_i, y in enumerate(a_t.shapes[bags[i]][0]):
            for x_i, x in enumerate(y):
                if x == "0":
                    if 0 != bags[i] != 3:
                        pygame.draw.rect(preview, grid_colors[bags[i] + 1], (x_i * 15 + 16, y_i * 15 + 23 + 83 * i, 15, 15))
                    elif bags[i] == 0:
                        pygame.draw.rect(preview, grid_colors[bags[i] + 1], (x_i * 15 + 8, y_i * 15 + 16 + 83 * i, 15, 15))
                    elif bags[i] == 3:
                        pygame.draw.rect(preview, grid_colors[bags[i] + 1], (x_i * 15 + 23, y_i * 15 + 23 + 83 * i, 15, 15))


def update_hold():
    if held != 0:
        hold.fill((0, 0, 0))
        pygame.draw.rect(hold, (255, 255, 255), (1, 1, 75, 75), 2)
        for y_i, y in enumerate(a_t.shapes[held - 1][0]):
            for x_i, x in enumerate(y):
                if x == "0":
                    if 0 != held - 1 != 3:
                        pygame.draw.rect(hold, grid_colors[held], (x_i * 15 + 16, y_i * 15 + 23, 15, 15))
                    elif held - 1 == 0:
                        pygame.draw.rect(hold, grid_colors[held], (x_i * 15 + 8, y_i * 15 + 16, 15, 15))
                    elif held - 1 == 3:
                        pygame.draw.rect(hold, grid_colors[held], (x_i * 15 + 23, y_i * 15 + 23, 15, 15))


def game_over():
    global run
    if a_t.detect_collision(grid, a_t.pos):
        run = False


while run:
    if fall_timer == 0:
        fall_timer = time()
    if time() - fall_timer >= 1 or (time() - fall_timer / 20 >= 1 and pygame.key.get_pressed()[K_DOWN]) and lockdown == 0:
        a_t.pos[1] += 2
        fall_timer = 0
        if a_t.detect_collision(grid, a_t.pos):
            a_t.pos[1] -= 1
            if lockdown == 0:
                lockdown = time()
            fall_timer = 0
            place_ = True
        if not place_:
            lockdown = 0
            a_t.pos[1] -= 1
        place_ = False
    if (pygame.key.get_pressed()[K_LEFT] or pygame.key.get_pressed()[K_RIGHT]) and time() - ma_time >= 0.3:
        move = True
        if step_time == 0:
            step_time = time()
    else:
        move = False
    min_x = 10
    max_x = 0
    if move and time() - step_time >= .05 and pygame.key.get_pressed()[K_LEFT]:
        step_time = 0
        a_t.pos[0] -= 1
        if a_t.detect_collision(grid, a_t.pos):
            a_t.pos[0] += 1

    if move and time() - step_time >= .05 and pygame.key.get_pressed()[K_RIGHT]:
        step_time = 0
        a_t.pos[0] += 1
        if a_t.detect_collision(grid, a_t.pos):
            a_t.pos[0] -= 1

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False
            if event.key == K_LEFT:
                ma_time = time()
                a_t.pos[0] -= 1
                if a_t.detect_collision(grid, a_t.pos):
                    a_t.pos[0] += 1

            if event.key == K_RIGHT:
                ma_time = time()
                a_t.pos[0] += 1
                if a_t.detect_collision(grid, a_t.pos):
                    a_t.pos[0] -= 1

            if event.key == K_UP:
                hard_drop()

            if event.key == K_x:
                a_t.rotate_right(grid)
            if event.key == K_y:
                a_t.rotate_left(grid)
            if event.key == K_c and not holding:
                lockdown = 0
                if held == 0:
                    held = a_t.shape_index + 1
                    a_t = Tetromino(bags[0])
                    bags.pop(0)
                else:
                    held_get = a_t.shape_index + 1
                    a_t = Tetromino(held - 1)
                    held = held_get
                holding = True
            if event.key == K_SPACE:
                a_t = Tetromino(bags[0])
                bags.pop(0)

    if time() - lockdown >= .5 and lockdown != 0:
        if a_t.detect_collision(grid, [a_t.pos[0], a_t.pos[1] + 1]):
            place()
        else:
            lockdown = 0

    if len(bags) < 3:
        generate_bag()
        print(f"Generated bag {bags[2:]}: {bags}")

    line_clear()
    screen.fill((0, 0, 0))
    update_grid()
    update_preview()
    update_hold()
    screen.blit(display_grid, (100, 75))
    screen.blit(preview, preview_rect)
    screen.blit(hold, hold_rect)
    screen.blit(next_t, next_t_rect)
    screen.blit(hold_t, hold_t_rect)

    pygame.display.update()
    clock.tick(60)
pygame.quit()
