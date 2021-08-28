import pygame
from pygame.locals import *
pygame.init()

# shape formats
i_shape = [[".....",
            ".....",
            ".0000"],
           ["....",
            "..0",
            "..0",
            "..0",
            "..0"],
           ["....",
            "....",
            "0000"],
           ["..0",
            "..0",
            "..0",
            "..0"]]

j_shape = [["0..",
            "000"],
           [".00",
            ".0.",
            ".0."],
           ["...",
            "000",
            "..0"],
           [".0",
            ".0",
            "00"]]

l_shape = [["..0",
            "000"],
           [".0.",
            ".0.",
            ".00"],
           ["....",
            "000",
            "0.."],
           ["00",
            ".0",
            ".0"]]

o_shape = [["00",
            "00"]]

s_shape = [[".00",
            "00."],
           [".0.",
            ".00",
            "..0"],
           ["...",
            ".00",
            "00."],
           ["0.",
            "00",
            ".0"]]

z_shape = [["00.",
            ".00"],
           ["..0",
            ".00",
            ".0."],
           ["...",
            "00.",
            ".00"],
           [".0",
            "00",
            "0"]]

t_shape = [["...",
            "000",
            ".0."],
           [".0",
            "00",
            ".0"],
           [".0.",
            "000"],
           [".0.",
            ".00",
            ".0."]]

shapes = [i_shape, j_shape, l_shape, o_shape, s_shape, z_shape, t_shape]

i_offset_data = ((0, 0),
                 (-1, 0),
                 (-1, -1),
                 (0, -1))


class Tetromino:
    def __init__(self, shape):
        self.pos = [0, 0]
        self.shape_index = shape
        self.shape = shapes[shape]
        self.state = 0

    def render(self, colors, surface: pygame.Surface):
        self.pos = pygame.Vector2(self.pos)
        for y_i, y in enumerate(self.shape[self.state]):
            for x_i, x in enumerate(y):
                if x == "0":
                    pygame.draw.rect(surface, colors[self.shape_index + 1], (int(self.pos.x + x_i) * 30, int(self.pos.y + y_i) * 30, 30, 30))

    def detect_collision(self, grid):
        for y_i, y in enumerate(self.shape[self.state]):
            for x_i, x in enumerate(y):
                if x == "0":
                    if grid[int(self.pos[1] + y_i)][int(self.pos[0] + x_i)] != 0:
                        return True
        return False

    def rotate_right(self, grid):
        fail = False
        if self.state <= len(self.shape) - 2:
            self.state += 1
        else:
            self.state = 0
        if self.shape_index == 0:
            self.pos -= pygame.Vector2(i_offset_data[self.state]) - pygame.Vector2(i_offset_data[self.state - 1])

        for y_i, y in enumerate(self.shape[self.state]):
            for x_i, x in enumerate(y):
                if x == "0":
                    if self.pos[0] + x_i < 0 or self.pos[0] + x_i > 9:
                        if self.state >= 0:
                            self.state -= 1
                        else:
                            self.state = len(self.shape) - 2
                        if self.shape_index == 0:
                            self.pos -= pygame.Vector2(i_offset_data[self.state]) - pygame.Vector2(i_offset_data[self.state + 1])
                        fail = True
                        break
            if fail:
                break

        if self.detect_collision(grid):
            if self.state >= 0:
                self.state -= 1
            else:
                self.state = len(self.shape) - 2

    def rotate_left(self, grid):
        fail = False
        if self.state >= 0:
            self.state -= 1
        else:
            self.state = len(self.shape) - 2
        if self.shape_index == 0:
            self.pos -= pygame.Vector2(i_offset_data[self.state]) - pygame.Vector2(i_offset_data[self.state + 1])

        for y_i, y in enumerate(self.shape[self.state]):
            for x_i, x in enumerate(y):
                if x == "0":
                    if self.pos[0] + x_i < 0 or self.pos[0] + x_i > 9:
                        if self.state <= len(self.shape) - 2:
                            self.state += 1
                        else:
                            self.state = 0
                        if self.shape_index == 0:
                            self.pos -= pygame.Vector2(i_offset_data[self.state]) - pygame.Vector2(i_offset_data[self.state - 1])
                        fail = True
                        break
            if fail:
                break

        if self.detect_collision(grid):
            if self.state <= len(self.shape) - 2:
                self.state += 1
            else:
                self.state = 0
