import pygame
from pygame.locals import *
pygame.init()

# shape formats
i_shape = [["....",
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

t_shape = [[".0.",
            "000",
            "..."],
           [".0.",
            ".00",
            ".0."],
           ["...",
            "000",
            ".0."],
           [".0.",
            "00.",
            ".0."]]

shapes = [i_shape, j_shape, l_shape, o_shape, s_shape, z_shape, t_shape]


class Tetromino:
    def __init__(self, shape):
        if shape == 0:
            self.pos = [3, -1]
        elif shape == 3:
            self.pos = [4, 0]
        else:
            self.pos = [3, 0]
        self.shapes = shapes
        self.shape_index = shape
        self.shape = shapes[shape]
        self.state = 0

    def render(self, colors, surface: pygame.Surface):
        for y_i, y in enumerate(self.shape[self.state]):
            for x_i, x in enumerate(y):
                if x == "0":
                    pygame.draw.rect(surface, colors[self.shape_index + 1], (int(self.pos[0] + x_i) * 30, int(self.pos[1] + y_i) * 30, 30, 30))

    def ghost_piece(self, surface, grid):
        test_pos = self.pos.copy()
        while True:
            test_pos[1] += 1
            try:
                if self.detect_collision(grid, test_pos) or test_pos[1] > 18:
                    test_pos[1] -= 1
                    for y_i, y in enumerate(self.shape[self.state]):
                        for x_i, x in enumerate(y):
                            if x == "0":
                                pygame.draw.rect(surface, (100, 100, 100), (int(test_pos[0] + x_i) * 30, int(test_pos[1] + y_i) * 30, 30, 30))
                    break
            except:
                test_pos[1] -= 1
                for y_i, y in enumerate(self.shape[self.state]):
                    for x_i, x in enumerate(y):
                        if x == "0":
                            pygame.draw.rect(surface, (100, 100, 100),
                                             (int(test_pos[0] + x_i) * 30, int(test_pos[1] + y_i) * 30, 30, 30))
                break

    def detect_collision(self, grid, pos):
        try:
            for y_i, y in enumerate(self.shape[self.state]):
                for x_i, x in enumerate(y):
                    if x == "0":
                        if pos[0] + x_i < 0:
                            return True
                        if grid[int(pos[1] + y_i)][int(pos[0] + x_i)] != 0:
                            return True
        except:
            return True
        return False

    def rotate_right(self, grid):
        fail = False
        if self.state <= len(self.shape) - 2:
            self.state += 1
        else:
            self.state = 0

        for y_i, y in enumerate(self.shape[self.state]):
            for x_i, x in enumerate(y):
                if x == "0":
                    if self.pos[0] + x_i < 0 or self.pos[0] + x_i > 9 or self.pos[1] + y_i < 0 or self.pos[1] + y_i > 19:
                        if self.state >= 0:
                            self.state -= 1
                        else:
                            self.state = len(self.shape) - 2
                        fail = True
                        break
            if fail:
                break

        if self.detect_collision(grid, self.pos):
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

        for y_i, y in enumerate(self.shape[self.state]):
            for x_i, x in enumerate(y):
                if x == "0":
                    if self.pos[0] + x_i < 0 or self.pos[0] + x_i > 9 or self.pos[1] + y_i < 0 or self.pos[1] + y_i > 19:
                        if self.state <= len(self.shape) - 2:
                            self.state += 1
                        else:
                            self.state = 0
                        fail = True
                        break
            if fail:
                break

        if self.detect_collision(grid, self.pos):
            if self.state <= len(self.shape) - 2:
                self.state += 1
            else:
                self.state = 0
