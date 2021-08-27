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

main_offset_data = (((0, 0), (0, 0), (0, 0), (0, 0), (0, 0)),
                    ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2)),
                    ((0, 0), (0, 0), (0, 0), (0, 0), (0, 0)),
                    ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)))

i_offset_data = (((0, 0), (-1, 0), (2, 0), (-1, 0), (2, 0)),
                 ((-1, 0), (0, 0), (0, 0), (0, -1), (0, 2)),
                 ((-1, -1), (1, -1), (-2, -1), (1, 0), (-2, 0)),
                 ((0, -1), (0, -1), (0, -1), (0, 1), (0, -2)))


class Tetromino:
    def __init__(self, shape):
        self.pos = [0, 0]
        self.shape_index = shape
        self.shape = shapes[shape]
        self.state = 0
        self.rotation_success = False
        if self.shape_index == 0:
            self.offset_data = i_offset_data
        else:
            self.offset_data = main_offset_data

    def render(self, colors, surface: pygame.Surface):
        self.pos = pygame.Vector2(self.pos)
        for y_i, y in enumerate(self.shape[self.state]):
            for x_i, x in enumerate(y):
                if x == "0":
                    pygame.draw.rect(surface, colors[self.shape_index + 1], (int(self.pos.x + x_i) * 30, int(self.pos.y + y_i) * 30, 30, 30))

    def rotate_right(self, grid):
        error = False
        passed = False
        pass_test = 0
        for test_i, test in enumerate(self.offset_data):
            error = False
            for y_i, y in enumerate(self.shape[self.state + 1] if self.state < len(self.shape) - 1 else self.shape[0]):
                if error:
                    break
                for x_i, x in enumerate(y):
                    if x == "0":
                        try:
                            if grid[int(self.pos[1] + y_i + (test[self.state][1] - test[self.state + 1][1]))][int(self.pos[0] + x_i + (test[self.state][0] - test[self.state + 1][0]))] == 0:
                                continue
                            else:
                                error = True
                                break
                        except:
                            error = True
                            break
            if not error:
                passed = True
                pass_test = test_i
                break
        if passed:
            self.pos += pygame.Vector2(pygame.Vector2(main_offset_data[pass_test][self.state]) - pygame.Vector2(main_offset_data[pass_test][self.state + 1]))
            if self.state <= len(self.shape) - 2:
                self.state += 1
            else:
                self.state = 0

        # if self.state <= len(self.shape) - 2:
        #     self.state += 1
        # else:
        #     self.state = 0
        # if self.shape_index == 0:
        #     self.pos -= pygame.Vector2(i_offset_data[self.state][0]) - pygame.Vector2(i_offset_data[self.state - 1][0])
        # else:
        #     self.pos -= pygame.Vector2(main_offset_data[self.state][0]) - pygame.Vector2(main_offset_data[self.state - 1][0])

    def rotate_left(self, grid):
        error = False
        passed = False
        pass_test = 0
        for test_i, test in enumerate(self.offset_data):
            error = False
            for y_i, y in enumerate(self.shape[self.state - 1] if self.state > 0 else self.shape[-1]):
                if error:
                    break
                for x_i, x in enumerate(y):
                    if x == "0":
                        try:
                            if grid[int(self.pos[1] + y_i + (test[self.state][1] - test[self.state - 1][1]))][int(self.pos[0] + x_i + (test[self.state][0] - test[self.state - 1][0]))] == 0:
                                continue
                            else:
                                error = True
                                break
                        except:
                            error = True
                            break
            if not error:
                passed = True
                pass_test = test_i
                break
        if passed:
            self.pos += pygame.Vector2(pygame.Vector2(main_offset_data[pass_test][self.state]) - pygame.Vector2(
                main_offset_data[pass_test][self.state - 1]))
            if self.state > 0:
                self.state -= 1
            else:
                self.state = len(self.shape) - 1
        # if self.state >= 0:
        #     self.state -= 1
        # else:
        #     self.state = len(self.shape) - 2
        # if self.shape_index == 0:
        #     self.pos -= pygame.Vector2(i_offset_data[self.state][0]) - pygame.Vector2(i_offset_data[self.state + 1][0])
        # else:
        #     self.pos -= pygame.Vector2(main_offset_data[self.state][0]) - pygame.Vector2(main_offset_data[self.state + 1][0])
