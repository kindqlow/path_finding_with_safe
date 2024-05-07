from Spot import *
import math
from queue import PriorityQueue
import numpy as np
from scipy.signal import convolve2d
from scipy.interpolate import interp1d


def fix_path_map(path, path_value):
    n = len(path_value)
    for i in range(n):
        for j in range(n):
            if j != i and path_value[i][j] < 1:
                path_value[i][j] = path_value[j][i] = 10000
            # else:
            #     path_value[i][j] = path_value[i][j]
    return [path, path_value]


def sort_ds(ds):
    lst1 = []
    lst2 = []
    if ds[0] == 0:
        return ds
    for i in range(len(ds)):
        if ds[i] != 0:
            lst2.append(ds[i])
        if ds[i] == 0 and len(lst2) > 0:
            lst1 = ds[i:] + lst2[1:] + [ds[i]]
            break
    return lst1


def delta(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


def get_neighbor(current, grid, total_row):
    lst = []
    row = current.get_row()
    col = current.get_col()
    total_row = 200
    if row < total_row - 1 and not grid[row + 1][col].is_barrier():  # Down
        lst.append(grid[row + 1][col])

    if row > 0 and not grid[row - 1][col].is_barrier():  # UP
        lst.append(grid[row - 1][col])

    if col < total_row - 1 and not grid[row][col + 1].is_barrier():  # RIGHT
        lst.append(grid[row][col + 1])

    if col > 0 and not grid[row][col - 1].is_barrier():  # LEFT
        lst.append(grid[row][col - 1])

    if row > 0 and col > 0 and not grid[row - 1][col - 1].is_barrier():
        lst.append(grid[row - 1][col - 1])  # Up and left

    if row > 0 and col < total_row - 1 and not grid[row - 1][col + 1].is_barrier():
        lst.append(grid[row - 1][col + 1])  # up and right

    if row < total_row - 1 and col > 0 and not grid[row + 1][col - 1].is_barrier():
        lst.append(grid[row + 1][col - 1])  # down and left

    if row < total_row - 1 and col < total_row - 1 and not grid[row + 1][col + 1].is_barrier():
        lst.append(grid[row + 1][col + 1])  # down and right

    return lst


def read_map_from_file(grid, ROWS, filename):
    with open(filename, 'r') as f:
        lst = []
        for line in f:
            row = list(map(int, line.split()))
            lst.append(row)
        for i in range(ROWS):
            for j in range(ROWS):
                if lst[i][j] == 1:
                    spot = grid[i][j]
                    spot.make_barrier()

        f.close()


def read_map_from_file2(grid, ROWS, filename):
    start = None
    lst_end = []
    tmp = 0
    with open(filename, 'r') as f:
        lst = []
        for line in f:
            row = list(map(int, line.split()))
            lst.append(row)
        for i in range(ROWS):
            for j in range(ROWS):
                if lst[i][j] == 1:
                    spot = grid[i][j]
                    spot.make_barrier()
                    tmp+=1
                elif lst[i][j] == 3:
                    spot = grid[i][j]
                    spot.make_start()
                    start = spot
                elif lst[i][j] == 2:
                    spot = grid[i][j]
                    spot.make_end()
                    lst_end.append(spot)
        f.close()
    return [[start] + lst_end, tmp]


def print_map(grid, rows):
    lst = [[0 for i in range(rows)] for j in range(rows)]
    for i in range(rows):
        for j in range(rows):
            if grid[i][j].is_barrier():
                lst[i][j] = 1
            else:
                lst[i][j] = 0
    for i in range(rows):
        for j in range(rows):
            print(lst[i][j], end=' ')
        print()


def print_path_value(path_value):
    n = len(path_value[0])
    for i in range(n):
        for j in range(n):
            print(round(path_value[i][j], 2), end=' ')
        print()


def make_grid(rows, width, safe):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows, safe)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    # draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def safe_zone(draw, rows, grid):
    count = 0
    open_set = PriorityQueue()
    for rows in grid:
        for spot in rows:
            if spot.is_barrier():
                open_set_hash = {spot}

    for rows in grid:
        for spot in rows:
            if spot.is_barrier():
                spot.safe = 0
                open_set.put((0, count, spot))
                open_set_hash.add(spot)
                count += 1

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        for neighbor in get_neighbor(current, grid, rows):
            if not neighbor.is_closed_safe():
                temp_safe = current.safe + delta(current.get_pos(), neighbor.get_pos())
                if temp_safe < neighbor.safe:
                    neighbor.safe = current.safe + delta(current.get_pos(), neighbor.get_pos())
                    count += 1
                    open_set_hash.add(neighbor)
                    open_set.put((neighbor.safe, count, neighbor))
                    neighbor.make_open_safe()

            if not current.is_barrier():
                current.make_closed_safe(current.safe)
        # draw()
