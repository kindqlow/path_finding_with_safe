import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (0, 0, 205)

CLOSED1 = (255, 0, 0)
CLOSED2 = (0, 191, 255)
CLOSED3 = (135, 206, 235)
CLOSED4 = (176, 224, 230)

class Spot:
    def __init__(self, row, col, width, total_rows, safe):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.safe = safe

    def get_pos(self):
        return self.row, self.col

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def get_safe(self):
        return self.safe

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self, n):
        if n < 1.5:
            self.color = CLOSED1
        elif n < 4:
            self.color = CLOSED2
        elif n < 8:
            self.color = CLOSED3
        else:
            self.color = CLOSED4

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col - 1])  # Up and left

        if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col + 1])  # up and right

        if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col - 1])  # down and left

        if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][
            self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col + 1])  # down and right

    def __lt__(self, other):
        return False


def get_neighbor(current, grid, total_row = 80):
    lst = []
    row = current.get_row()
    col = current.get_col()
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


def print_map(grid, ROWS):
    lst = [[0 for i in range(ROWS)] for j in range(ROWS)]
    for i in range(ROWS):
        for j in range(ROWS):
            if grid[i][j].is_barrier():
                lst[i][j] = 1
            else:
                lst[i][j] = 0
    for i in range(ROWS):
        for j in range(ROWS):
            print(lst[i][j], end=' ')
        print()


def delta(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


def reconstruct_path(came_from, current, draw):
    lst = []
    while current in came_from:
        current = came_from[current]
        lst.append(current)
        # current.make_path()
        # draw()
    return lst


def reconstruct_path_safe(came_from, open_set_hash, g_score, current, draw, grid):
    while current in came_from:
        tmp_current = current
        current = came_from[current]
        for neighbor in get_neighbor(tmp_current, grid):
            if neighbor in open_set_hash:
                if neighbor.safe > current.safe and g_score[neighbor] <= g_score[current]:
                    current = neighbor
                    print("kkk")
        current.make_path()
        draw()


def draw_path_safe(lst, draw, grid, g_score):
    n = len(lst)
    current = lst[0]
    current.make_path()
    for i in range(1, n-1):
        current = lst[i]
        for neighbor in get_neighbor(lst[i-1], grid):
            if neighbor in get_neighbor(lst[i+1], grid):
                if neighbor.safe > current.safe and g_score[neighbor] <= g_score[current] + 0.5:
                    current = neighbor
                    print("kkk")
                    break
        current.make_path()
        draw()


def safe_zone(draw, grid):
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
        for neighbor in get_neighbor(current, grid):
            if not neighbor.is_closed():
                temp_safe = current.safe + delta(current.get_pos(), neighbor.get_pos())
                if temp_safe < neighbor.safe:
                    neighbor.safe = current.safe + delta(current.get_pos(), neighbor.get_pos())
                    count += 1
                    open_set_hash.add(neighbor)
                    open_set.put((neighbor.safe, count, neighbor))
                    neighbor.make_open()

            if not current.is_barrier():
                current.make_closed(current.safe)
        # draw()
    return False


def algorithm1(draw, grid, start, end, anpha, ROWS):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = g_score[start]

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        if current == end:
            # reconstruct_path_safe(came_from, open_set_hash, g_score, current, draw, grid)
            print_map(grid, ROWS)
            lst = reconstruct_path(came_from, current, draw)
            draw_path_safe(lst, draw, grid, g_score)
            start.make_start()
            end.make_end()
            print("Thuật toán Fast marching")
            print("số nút đã thăm là: " + str(count))
            print("Chi phí tìm đường là: " + str(g_score[end]))
            return True

        for neighbor in get_neighbor(current, grid):
            temp_g_score = g_score[current] + delta(current.get_pos(), neighbor.get_pos())

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = anpha * g_score[neighbor] - (1-anpha) * neighbor.safe
                # if neighbor.safe < 2:
                #     f_score[neighbor] = g_score[neighbor] - neighbor.safe
                # elif neighbor.safe < 5:
                #     f_score[neighbor] = g_score[neighbor] - neighbor.safe / 4
                # else:
                #     f_score[neighbor] = g_score[neighbor] - neighbor.safe / 10
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    neighbor.make_open()
                    open_set_hash.add(neighbor)

        # draw()

        if current != start:
            current.make_closed(3)

    return False


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


def main(win, width):
    ROWS = 80
    safe = 100
    anpha = 0.7
    grid = make_grid(ROWS, width, safe)
    start = None
    end = None
    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    algorithm1(lambda: draw(win, grid, ROWS, width), grid, start, end, anpha, ROWS)
                if event.key == pygame.K_f:
                    safe_zone(lambda: draw(win, grid, ROWS, width), grid)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width, safe)
                if event.key == pygame.K_m:
                    read_map_from_file(grid, ROWS, "map01.txt")
                if event.key == pygame.K_n:
                    read_map_from_file(grid, ROWS, "map02.txt")
                if event.key == pygame.K_b:
                    read_map_from_file(grid, ROWS, "map03.txt")
                if event.key == pygame.K_v:
                    read_map_from_file(grid, ROWS, "map80_1.txt")
                if event.key == pygame.K_l:
                    read_map_from_file(grid, ROWS, "map80_2.txt")
                if event.key == pygame.K_k:
                    read_map_from_file(grid, ROWS, "map80_3.txt")

    pygame.quit()


main(WIN, WIDTH)
