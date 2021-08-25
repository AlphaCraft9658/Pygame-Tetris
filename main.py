import pygame
from pygame.locals import *
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

# visual grid
display_grid = pygame.Surface((305, 605))
display_grid.fill((0, 0, 0))
display_grid.set_colorkey((0, 0, 0))
grid_colors = [(0, 0, 0), (0, 200, 255), (0, 100, 255), (255, 100, 0), (255, 225, 0), (0, 225, 50), (255, 0, 0),
               (200, 0, 255)]

# virtual grid
grid = [[0 for n in range(10)] for i in range(20)]

bags = []


def draw_grid_pattern():
    for i in range(21):
        if i == 0:
            pygame.draw.line(display_grid, (255, 255, 255), (0, 0), (300, 0), 3)
        else:
            pygame.draw.line(display_grid, (255, 255, 255), (0, i * 30), (300, i * 30), 3)

    for i in range(11):
        if i == 0:
            pygame.draw.line(display_grid, (255, 255, 255), (0, 0), (0, 600), 2)
        else:
            pygame.draw.line(display_grid, (255, 255, 255), (i * 30, 0), (i * 30, 600), 2)


def update_grid():
    for row_i, row in enumerate(grid):
        for tile_i, tile in enumerate(row):
            pygame.draw.rect(display_grid, grid_colors[tile], (tile_i * 30, row_i * 30, 30, 30))
    test_tetromino.render(grid_colors, display_grid)
    draw_grid_pattern()


def generate_bag():
    bags.append(sample([1, 2, 3, 4, 5, 6, 7], 7))


test_tetromino = Tetromino(0)
test_tetromino.pos = [3, 3]
min_x = 10
max_x = 0
run = True
while run:
    min_x = 10
    max_x = 0
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                test_tetromino.pos[0] -= 1
                for y_i, y in enumerate(test_tetromino.shape[test_tetromino.state]):
                    for x_i, x in enumerate(y):
                        if x_i < min_x and x == "0":
                            min_x = x_i
                            if test_tetromino.pos[0] + x_i < 0:
                                test_tetromino.pos[0] += 1
                # if test_tetromino.pos[0] > 0:
                #     test_tetromino.pos[0] -= 1
            if event.key == K_RIGHT:
                test_tetromino.pos[0] += 1
                for y_i, y in enumerate(test_tetromino.shape[test_tetromino.state]):
                    for x_i, x in enumerate(y):
                        if x_i > max_x and x == "0":
                            max_x = x_i
                            if test_tetromino.pos[0] + x_i > 9:
                                test_tetromino.pos[0] -= 1
                # test_tetromino.pos[0] += 1
            if event.key == K_e:
                test_tetromino.rotate_right(grid)
            if event.key == K_q:
                test_tetromino.rotate_left(grid)
            if event.key == K_SPACE:
                if test_tetromino.shape_index == 6:
                    test_tetromino = Tetromino(0)
                else:
                    test_tetromino = Tetromino(test_tetromino.shape_index + 1)
                test_tetromino.pos = [3, 3]
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if pygame.key.get_pressed()[K_LCTRL] and pygame.key.get_pressed()[K_LSHIFT]:
                    if 50 <= event.pos[0] <= 350 and 75 <= event.pos[1] <= 675:
                        if (event.pos[1] - 75) // 30 <= 20 and (event.pos[0] - 50) // 30 <= 10:
                            if grid[(event.pos[1] - 75) // 30][(event.pos[0] - 50) // 30] < 7:
                                grid[(event.pos[1] - 75) // 30][(event.pos[0] - 50) // 30] += 1
                            else:
                                grid[(event.pos[1] - 75) // 30][(event.pos[0] - 50) // 30] = 0

    screen.fill((0, 0, 0))
    screen.blit(display_grid, (50, 75))
    update_grid()

    if pygame.mouse.get_pressed(3)[2]:
        if pygame.key.get_pressed()[K_LCTRL] and pygame.key.get_pressed()[K_LSHIFT]:
            if 50 <= pygame.mouse.get_pos()[0] <= 350 and 75 <= pygame.mouse.get_pos()[1] <= 675:
                if (pygame.mouse.get_pos()[1] - 75) // 30 <= 20 and (pygame.mouse.get_pos()[0] - 50) // 30 <= 10:
                    grid[(pygame.mouse.get_pos()[1] - 75) // 30][(pygame.mouse.get_pos()[0] - 50) // 30] = 0

    # color palette on the side of the screen
    pygame.draw.rect(screen, grid_colors[0], (0, 100, 50, 50))
    pygame.draw.rect(screen, grid_colors[1], (0, 150, 50, 50))
    pygame.draw.rect(screen, grid_colors[2], (0, 200, 50, 50))
    pygame.draw.rect(screen, grid_colors[3], (0, 250, 50, 50))
    pygame.draw.rect(screen, grid_colors[4], (0, 300, 50, 50))
    pygame.draw.rect(screen, grid_colors[5], (0, 350, 50, 50))
    pygame.draw.rect(screen, grid_colors[6], (0, 400, 50, 50))
    pygame.draw.rect(screen, grid_colors[7], (0, 450, 50, 50))

    pygame.display.update()
    clock.tick(60)
pygame.quit()
