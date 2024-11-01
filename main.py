# import pygame
# import math
# from queue import PriorityQueue
#
# WIDTH = 800
# WIN = pygame.display.set_mode((WIDTH, WIDTH))
# pygame.display.set_caption("A* Path Finding Algorithm")
#
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 255, 0)
# YELLOW = (255, 255, 0)
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# PURPLE = (128, 0, 128)
# ORANGE = (255, 165, 0)
# GREY = (128, 128, 128)
# TURQUOISE = (64, 224, 208)
#
#
# class Spot:
#     def __init__(self, row, col, width, total_rows):
#         self.row = row
#         self.col = col
#         self.x = row * width
#         self.y = col * width
#         self.color = WHITE
#         self.neighbors = []
#         self.width = width
#         self.total_rows = total_rows
#
#     def get_pos(self):
#         return self.row, self.col
#
#     def get_real_pos(self):
#         gap = WIDTH // 50
#         x = gap * self.row + 8  # để đường thẳng nằm giữa ô vuông
#         y = gap * self.col + 8
#         return x, y
#
#     def is_closed(self):
#         return self.color == RED
#
#     def is_open(self):
#         return self.color == GREEN
#
#     def is_barrier(self):
#         return self.color == BLACK
#
#     def is_start(self):
#         return self.color == ORANGE
#
#     def is_end(self):
#         return self.color == TURQUOISE
#
#     def reset(self):
#         self.color = WHITE
#
#     def make_start(self):
#         self.color = ORANGE
#
#     def make_closed(self):
#         self.color = RED
#
#     def make_open(self):
#         self.color = GREEN
#
#     def make_barrier(self):
#         self.color = BLACK
#
#     def make_end(self):
#         self.color = TURQUOISE
#
#     def make_path(self):
#         self.color = PURPLE
#
#     def draw(self, win):
#         pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
#
#     def update_neighbors(self, grid):
#         self.neighbors = []
#         if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
#             self.neighbors.append(grid[self.row + 1][self.col])
#
#         if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
#             self.neighbors.append(grid[self.row - 1][self.col])
#
#         if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
#             self.neighbors.append(grid[self.row][self.col + 1])
#
#         if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
#             self.neighbors.append(grid[self.row][self.col - 1])
#
#         if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_barrier():
#             self.neighbors.append(grid[self.row - 1][self.col - 1])  # Up and left
#
#         if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][self.col + 1].is_barrier():
#             self.neighbors.append(grid[self.row - 1][self.col + 1])  # up and right
#
#         if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].is_barrier():
#             self.neighbors.append(grid[self.row + 1][self.col - 1])  # down and left
#
#         if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][
#             self.col + 1].is_barrier():
#             self.neighbors.append(grid[self.row + 1][self.col + 1])  # down and right
#
#     def __lt__(self, other):
#         return False
#
#
# class Robot:
#     def __init__(self, startPos, robotImg, width):
#
#         self.x, self.y = startPos
#         self.theta = 0
#         self.width = width
#         self.vr = 15  # right velocity
#         self.vl = 15  # left velocity
#         self.u = (self.vl + self.vr)/2  # linear velocity
#         self.W = 0  # angular velocity
#         self.a = 15  # width of robot
#         self.trail_set = []
#         self.dt = 0  # time step
#         self.pathRb = []
#         self.img = pygame.image.load(robotImg)
#         self.img = pygame.transform.scale(self.img, (width, width))
#         self.rotated = self.img
#         self.rect = self.rotated.get_rect(center=(self.x, self.y))
#
#     def move(self, event=None):
#
#         self.x += ((self.vl + self.vr)/2)*math.cos(self.theta)*self.dt
#         self.y += ((self.vl + self.vr)/2)*math.sin(self.theta)*self.dt
#         self.theta += (self.vr - self.vl)/self.width*self.dt
#
#         if self.theta >= math.pi * 2 or self.theta <= -2*math.pi:
#             self.theta = 0
#
#         self.rotated = pygame.transform.rotozoom(
#             self.img, math.degrees(-self.theta), 1)
#         self.rect = self.rotated.get_rect(center=(self.x, self.y))
#
#         self.following()
#
#     def following(self):
#         target = self.pathRb[0]
#         delta_x = target[0] - self.x
#         delta_y = target[1] - self.y
#
#         self.W = (-1/self.a) * math.sin(self.theta) * delta_x + \
#             (1/self.a) * math.cos(self.theta)*delta_y
#         # print(self.W)
#
#         self.vr = self.u + (self.W * self.width)/2
#         self.vl = self.u - (self.W * self.width)/2
#         if self.dist((self.x, self.y), target) <= 10:
#             self.pathRb.pop(0)
#
#     def dist(self, point1, point2):
#         (x1, y1) = point1
#         (x2, y2) = point2
#         x1 = float(x1)
#         x2 = float(x2)
#         y1 = float(y1)
#         y2 = float(y2)
#
#         px = (x1 - x2) ** 2
#         py = (y1 - y2) ** 2
#         distance = (px + py) ** 0.5
#         return distance
#
#     def draw(self, map):
#         map.blit(self.rotated, self.rect)
#
#     def trail(self, pos, map, color):
#         for i in range(0, len(self.trail_set) - 1):
#             pygame.draw.line(map, color, (self.trail_set[i][0], self.trail_set[i][1]),
#                              (self.trail_set[i+1][0], self.trail_set[i+1][1]), 3)
#         self.trail_set.append(pos)
#
#
# def h(p1, p2):
#     x1, y1 = p1
#     x2, y2 = p2
#     return abs(x1 - x2) + abs(y1 - y2)
#
#
# def reconstruct_path(came_from, current, draw):
#     lst = []
#     while current in came_from:
#         current = came_from[current]
#         lst.append(current.get_real_pos())
#     return lst
#
#
# def algorithm(draw, grid, start, end):
#     path = []
#     count = 0
#     open_set = PriorityQueue()
#     open_set.put((0, count, start))
#     came_from = {}
#     g_score = {spot: float("inf") for row in grid for spot in row}
#     g_score[start] = 0
#     f_score = {spot: float("inf") for row in grid for spot in row}
#     f_score[start] = h(start.get_pos(), end.get_pos())
#
#     open_set_hash = {start}
#
#     while not open_set.empty():
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#
#         current = open_set.get()[2]
#         open_set_hash.remove(current)
#
#         if current == end:
#             path = reconstruct_path(came_from, end, draw)
#             return path
#         for neighbor in current.neighbors:
#             temp_g_score = g_score[current] + 1
#
#             if temp_g_score < g_score[neighbor]:
#                 came_from[neighbor] = current
#                 g_score[neighbor] = temp_g_score
#                 f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
#                 if neighbor not in open_set_hash:
#                     count += 1
#                     open_set.put((f_score[neighbor], count, neighbor))
#                     open_set_hash.add(neighbor)
#                     neighbor.make_open()
#
#         # draw()
#
#         if current != start:
#             current.make_closed()
#
#     return path
#
#
# def make_grid(rows, width):
#     grid = []
#     gap = width // rows
#     for i in range(rows):
#         grid.append([])
#         for j in range(rows):
#             spot = Spot(i, j, gap, rows)
#             grid[i].append(spot)
#
#     return grid
#
#
# def draw_grid(win, rows, width):
#     gap = width // rows
#     for i in range(rows):
#         pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
#         for j in range(rows):
#             pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
#
#
# def draw(win, grid, rows, width):
#     win.fill(WHITE)
#
#     for row in grid:
#         for spot in row:
#             spot.draw(win)
#
#     draw_grid(win, rows, width)
#     pygame.display.update()
#
#
# def get_clicked_pos(pos, rows, width):
#     gap = width // rows
#     y, x = pos
#
#     row = y // gap
#     col = x // gap
#
#     return row, col
#
#
# def main(win, width):
#     ROWS = 50
#     grid = make_grid(ROWS, width)
#
#     start = None
#     end = None
#
#     run = True
#     while run:
#         draw(win, grid, ROWS, width)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#
#             if pygame.mouse.get_pressed()[0]:  # LEFT
#                 pos = pygame.mouse.get_pos()
#                 row, col = get_clicked_pos(pos, ROWS, width)
#                 spot = grid[row][col]
#                 if not start and spot != end:
#                     start = spot
#                     start.make_start()
#
#                 elif not end and spot != start:
#                     end = spot
#                     end.make_end()
#
#                 elif spot != end and spot != start:
#                     spot.make_barrier()
#
#             elif pygame.mouse.get_pressed()[2]:  # RIGHT
#                 pos = pygame.mouse.get_pos()
#                 row, col = get_clicked_pos(pos, ROWS, width)
#                 spot = grid[row][col]
#                 spot.reset()
#                 if spot == start:
#                     start = None
#                 elif spot == end:
#                     end = None
#
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE and start and end:
#                     for row in grid:
#                         for spot in row:
#                             spot.update_neighbors(grid)
#
#                     time_set = 0
#
#                     path = algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
#                     robot = Robot(start.get_real_pos(), "Robot.png", 16)
#                     for i in range(len(path) - 1):
#                         lasttime = pygame.time.get_ticks()
#                         robot.pathRb.append(path[i])
#                     j = 0
#                     while robot.dist((robot.x, robot.y), path[j]) > 10:
#                         for event in pygame.event.get():
#                             if event.type == pygame.QUIT:
#                                 pygame.quit()
#                         robot.dt = (pygame.time.get_ticks() - lasttime) / 1000
#                         time_set += robot.dt
#
#                         lasttime = pygame.time.get_ticks()
#                         print("kkk")
#                         robot.move()
#                         robot.draw(win)
#                         robot.trail((robot.x, robot.y), win, PURPLE)
#                         pygame.display.update()
#                         j += 1
#                     start.make_start()
#                     end.make_end()
#
#
#
#                 if event.key == pygame.K_c:
#                     start = None
#                     end = None
#                     grid = make_grid(ROWS, width)
#
#     pygame.quit()
#
#
# main(WIN, WIDTH)


# def fix_map(filename):
#     with open(filename, 'r') as f:
#         lst = []
#         for line in f:
#             row = list(map(int, line.split()))
#             lst.append(row)
#
#         n = 200 - len(lst[0])
#
#         if n < 200:
#             a = 0
#             b = 0
#             a = n//2
#             if n % 2 == 0:
#                 b = a
#             else:
#                 b = a + 1
#             front_lst = []
#             end_lst = []
#             for i in range(a):
#                 front_lst.append(1)
#             for i in range(b):
#                 end_lst.append(1)
#             for j in range(200):
#                 lst[j] = front_lst + lst[j] + end_lst
#
#     with open('IN2D_01.txt', 'w') as f:
#         for row in lst:
#             line = ' '.join(map(str, row))
#             f.write(line + '\n')
#     f.close()
#
#
# file_name = "IN2D_01.txt"
# fix_map(file_name)

import random


def check_neighbor(i, j, lst):
    n = len(lst)
    if lst[i][j] == 0:
        if lst[i - 1][j] + lst[i + 1][j] + lst[i][j - 1] + lst[i][j + 1] + lst[i - 1][j - 1] + lst[i - 1][j + 1] + lst[i + 1][j - 1] + lst[i + 1][j + 1] == 0:
            return True
    return False


def thay_doi_ma_tran(matrix, m):
    n = len(matrix)
    lst = [row.copy() for row in matrix]  # Tạo bản sao của ma trận để không ảnh hưởng đến ma trận gốc

    zeros = []  # Danh các điểm chứa bit 0
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            if check_neighbor(i, j, lst):
                zeros.append((i, j))

    random.shuffle(zeros)  # Xáo trộn danh sách các điểm 0
    count = 0
    while count < m:
        x, y = zeros[count]
        lst[x][y] = 2  # Thay thế điểm 0 bằng điểm 2
        count += 1

    return lst


def read_map_from_file(filename):
    with open(filename, 'r') as f:
        lst = []
        for line in f:
            row = list(map(int, line.split()))
            for i in range(len(row)):
                if row[i] > 1:
                    row[i] = 0
            lst.append(row)
    f.close()
    return lst


def write_map_to_file(filename, lst):
    with open(filename, 'w') as f:
        for row in lst:
            line = ' '.join(map(str, row))
            f.write(line + '\n')
    f.close()


def gen_random_map(filename, n_point):
    matrix = read_map_from_file(filename)
    updated_matrix = thay_doi_ma_tran(matrix, n_point)
    write_map_to_file(filename, updated_matrix)


def fix_map(filename):
    n_max = 200
    with open(filename, 'r') as f:
        lst = []
        for line in f:
            row = list(map(int, line.split()))
            lst.append(row)

        # Thiếu chiều rộng
        n = n_max - len(lst[0])
        if n > 0:
            a = 0
            b = 0
            a = n//2
            if n % 2 == 0:
                b = a
            else:
                b = a + 1
            front_lst = []
            end_lst = []
            for i in range(a):
                front_lst.append(1)
            for i in range(b):
                end_lst.append(1)
            for j in range(n_max):
                lst[j] = front_lst + lst[j] + end_lst

        # Thiếu chiều dài
        m = n_max - len(lst)
        if m > 0:
            a = 0
            b = 0
            a = m//2
            if m % 2 == 0:
                b = a
            else:
                b = a + 1
            front_lst = []
            end_lst = []
            lst_tmp = []
            for i in range(n_max):
                lst_tmp.append(1)
            for i in range(a):
                front_lst.append(lst_tmp)
            for i in range(b):
                end_lst.append(lst_tmp)

            lst = front_lst + lst + end_lst

        # Chỉnh biên về 1
        for i in range(n_max):
            if lst[i][0] == 0:
                lst[i][0] = 1
            if lst[i][1] == 0:
                lst[i][1] = 1
            if lst[i][n_max-1] == 0:
                lst[i][n_max-1] = 1
            if lst[i][n_max-2] == 0:
                lst[i][n_max-2] = 1
            if lst[0][i] == 0:
                lst[0][i] = 1
            if lst[1][i] == 0:
                lst[1][i] = 1
            if lst[n_max-1][i] == 0:
                lst[n_max-1][i] = 1
            if lst[n_max-2][i] == 0:
                lst[n_max-2][i] = 1

    with open(filename, 'w') as f:
        for row in lst:
            line = ' '.join(map(str, row))
            f.write(line + '\n')
    f.close()


filename = "IN2D_01.txt"
fix_map(filename)
n_point = 30
gen_random_map(filename, n_point)

import numpy as np
import matplotlib.pyplot as plt


# def write_data_gen_to_file(filename, data):
#     file = open(filename, "a")
#     file.write("S3\n")
#     for value in data:
#         file.write(str(round(value, 3)) + " ")
#         file.write("\n")
#     file.close()
#
# # Thiết lập thông số của hai phân phối chuẩn
# loc1, scale1, size1 = 7.27, 0.47, 30
# loc2, scale2, size2 = 6.95, 0.68, 30
# loc3, scale3, size3 = 7.67, 0.43, 30
# loc4, scale4, size4 = 6.59, 0.35, 30
# # loc5, scale5, size5 = 1, 0.5, 30
#
# # Sinh dữ liệu từ phân phối chuẩn
# data1 = np.random.normal(loc1, scale1, size1)
# data2 = np.random.normal(loc2, scale2, size2)
# data3 = np.random.normal(loc3, scale3, size3)
# data4 = np.random.normal(loc4, scale4, size4)
# # data5 = np.random.normal(loc5, scale5, size5)
#
# # Ghi dữ liệu vào file
# write_data_gen_to_file('Data_gen.txt', data1)
# write_data_gen_to_file('Data_gen.txt', data2)
# write_data_gen_to_file('Data_gen.txt', data3)
# write_data_gen_to_file('Data_gen.txt', data4)
# # write_data_gen_to_file('Data_gen.txt', data5)
#
# # Vẽ biểu đồ Boxplot
# plt.boxplot([data1, data2, data3, data4], labels=['Data 1', 'Data 2', 'Data 3', 'Data 4'])
#
# # Thiết lập tiêu đề và nhãn
# plt.title('Boxplot of Two Normal Distributions')
# plt.ylabel('Values')
#
# # Hiển thị biểu đồ
# plt.show()
