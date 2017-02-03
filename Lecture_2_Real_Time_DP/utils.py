import time
import os

green = lambda x: '\x1b[32m{}\x1b[0m'.format(x)
blue = lambda x: '\x1b[34m{}\x1b[0m'.format(x)
red = lambda x: '\x1b[31m{}\x1b[0m'.format(x)


def print_grid(grid):
    string = ""
    for row in grid:
        for cell in row:
            if cell == 'O':
                cell = cell.replace(cell, green(cell))
            elif cell == 'S' or cell == 'E':
                cell = cell.replace(cell, blue(cell))
            elif cell == 'P':
                cell = cell.replace(cell, red(cell))
            string += cell + ' '
        string += '\n'
    os.system('clear')
    print string


def get_start_and_end_states(grid):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 'S':
                start = (i, j)
            elif cell == 'E':
                end = (i, j)
    return start, end
