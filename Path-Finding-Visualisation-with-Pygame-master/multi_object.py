import math
import time
from itertools import permutations

from Robot import *
from Map_Grid import *
import numpy as np
from FFT_TSP import *
from TSP_cristofides_2 import *
from fixmap import *
from GWO_TSP import *
from GWO_TSP2 import *
from ACO_TSP import *

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithm")


def reconstruct_path_safe(lst, grid, g_score, min_safe):
    path = []
    n = len(lst)

    path.append(lst[0])
    for i in range(1, n-1):
        current = lst[i]
        for neighbor in get_neighbor(lst[i-1], grid, 200):
            if neighbor in get_neighbor(lst[i+1], grid, 200):
                if current.safe < min_safe and neighbor.safe > current.safe and g_score[neighbor] <= g_score[current] + 0.5:
                    current = neighbor
                    lst[i] = neighbor

        path.append(current)
    return path


def reconstruct_path_smooth(path, grid):
    for i in range(1, len(path) - 1):
        if path[i-1].get_row() == path[i+1].get_row():
            if path[i].get_row() != path[i-1].get_row() and not grid[path[i-1].get_row()][path[i].get_col()].is_barrier():
                path[i] = grid[path[i-1].get_row()][path[i].get_col()]
                #print("aaa")
        elif path[i-1].get_col() == path[i+1].get_col():
            if path[i].get_col() != path[i-1].get_col() and not grid[path[i].get_row()][path[i-1].get_col()].is_barrier():
                path[i] = grid[path[i].get_row()][path[i-1].get_col()]
                #print("bbb")
    return path


def caculate_path(path, path_value, ds, lst_start, grid):
    n = len(ds)
    path_final = []
    path_length = 0
    count = 1
    while count < n:
        lst = reconstruct_path_smooth(path[ds[count - 1]][ds[count]], grid)
        path_final = path_final + lst
        path_length += path_value[ds[count - 1]][ds[count]]
        count += 1
    return path_length


def draw_path_final(path, path_value, ds, lst_start, grid, draw):
    # print(ds)
    n = len(ds)

    path_final = []
    path_length = 0
    count = 1
    #print(ds[count-1])
    while count < n:
        lst = reconstruct_path_smooth(path[ds[count-1]][ds[count]], grid)
        # lst = path[ds[count - 1]][ds[count]]
        # lst = smooth_path(path[ds[count - 1]][ds[count]])
        path_final = path_final + lst
        path_length += path_value[ds[count-1]][ds[count]]
        #print(ds[count])
        count += 1
    result = []
    for item in path_final:
        if item not in result:
            result.append(item)
    path_final = result
    for points in path_final:
        points.make_path()
        # draw()
        time.sleep(0)
    # robot = Robot((lst_start[0].get_x() + 4, lst_start[0].get_y() + 4), "Robot.png", 4)
    # robot.pathRb = path_final
    # while True:
    #     for points in path_final:
    #         robot.draw(WIN)
    #         robot.trail((points.get_x() + 4, points.get_y() + 4), WIN, ORANGE)
    #         pygame.display.update()
    #     time.sleep(30)
    #     break
    lst_start[0].make_start()
    for i in range(1, len(lst_start)):
        lst_start[i].make_end()
    # draw()
    # print("Tổng độ dài quãng đường FFT là: "+ str(round(path_length, 2)))
    print(round(path_length, 2))


def draw_path(lst_start, path, draw):
    n = len(path[0])
    for i in range(n):
        for j in range(n):
            lst = path[i][j]
            for points in lst:
                points.make_path()
    lst_start[0].make_start()
    for i in range(1, len(lst_start)):
        lst_start[i].make_end()
    draw()


def algorithm(draw, grid, lst_start, T_step, T_max):
    edges = []
    n = len(lst_start)
    lst_check = [0 for i in range(n)]
    lst_count = [0 for i in range(n)]
    lst_open_set = [[] for i in range(n)]
    lst_came_from = [{} for i in range(n)]
    lst_g_score = [{} for i in range(n)]
    lst_f_score = [{} for i in range(n)]
    lst_open_set_hash = [{} for i in range(n)]
    path = [[[] for j in range(n)] for i in range(n)]
    path_value = [[0 for j in range(n)] for i in range(n)]
    check_path = [[0 for j in range(n)] for i in range(n)]
    max_count_path = 0
    check_grid = {lst_start[0]}
    for i in range(n):
        lst_count[i] = 0
        lst_open_set[i] = PriorityQueue()
        lst_open_set[i].put((0, lst_count[i], lst_start[i]))
        lst_came_from[i] = {}
        lst_g_score[i] = {spot: float("inf") for row in grid for spot in row}
        lst_g_score[i][lst_start[i]] = 0
        lst_f_score[i] = {spot: float("inf") for row in grid for spot in row}
        lst_f_score[i][lst_start[i]] = lst_g_score[i][lst_start[i]]
        lst_open_set_hash[i] = {lst_start[i]}
        check_grid.add(lst_start[i])
    run = True
    # min_neighbors = 5 #round(math.sqrt(n) * math.log1p(n))
    # min_max_count_path = n*min_neighbors - (min_neighbors * min_neighbors - (n%min_neighbors*(n%min_neighbors)-1))
    while run:
        # print(max_count_path)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        lst_current = [None for i in range(n)]
        for i in range(n):
            lst_current[i] = lst_open_set[i].get()[2]
            for j in range(n):

                if lst_count[0] >= T_max:
                    # print(lst_count[0])
                    if check_path_valid(fix_path_map(path, path_value) + [edges]):
                        return fix_path_map(path, path_value) + [edges]
                    else:
                        T_max += T_step
                if i != j and (lst_current[i] in lst_open_set_hash[j]) and check_path[i][j] == 0:
                    lst_check[i] += 1
                    lst_check[j] += 1
                    path_temp1 = [lst_current[i]] + reconstruct_path(lst_came_from[i], lst_current[i])
                    path_temp2 = [lst_current[i]] + reconstruct_path(lst_came_from[j], lst_current[i])
                    path_safe1 = reconstruct_path_safe(path_temp1, grid, lst_g_score[i], min_safe=1.5)
                    # path_safe1 = reconstruct_path_safe(path_safe1, grid, lst_g_score[i], min_safe=2.5)
                    path_safe2 = reconstruct_path_safe(path_temp2, grid, lst_g_score[j], min_safe=1.5)
                    # path_safe2 = reconstruct_path_safe(path_safe2, grid, lst_g_score[j], min_safe=2.5)
                    path_safe1.reverse()
                    path[i][j] = path_safe1 + path_safe2
                    temp_path = path[i][j]
                    temp_path.reverse()
                    path[j][i] = temp_path
                    check_path[i][j] = check_path[j][i] = 1
                    path_value[i][j] = path_value[j][i] = lst_g_score[i][lst_current[i]] + lst_g_score[j][lst_current[i]]
                    edges.append((path_value[i][j], (i, j)))
                    max_count_path += 2
                    if max_count_path >= n*(n-1):
                        # sum_edge = 0
                        # for p in lst_check:
                        #     sum_edge += p
                        # print(lst_check)
                        # print(sum_edge/((n-1)*n))
                        return fix_path_map(path, path_value) + [edges]
            for neighbor in lst_current[i].neighbors:
                temp_g_score = lst_g_score[i][lst_current[i]] + delta(lst_current[i].get_pos(), neighbor.get_pos())

                if temp_g_score < lst_g_score[i][neighbor]:
                    lst_came_from[i][neighbor] = lst_current[i]
                    lst_g_score[i][neighbor] = temp_g_score
                    lst_f_score[i][neighbor] = lst_g_score[i][neighbor]
                    if neighbor.safe >= 1.5 and neighbor not in lst_open_set_hash[i]:  # and neighbor not in check_grid:
                        lst_count[i] += 1
                        lst_open_set[i].put((lst_f_score[i][neighbor], lst_count[i], neighbor))
                        neighbor.make_open(i)
                        lst_open_set_hash[i].add(neighbor)
                        # check_grid.add(neighbor)
                    else:
                        neighbor.make_open(i)
        # if lst_count[0] % 20 == 0:
        #     draw()
        for i in range(n):
            if lst_current[i] not in lst_start:
                lst_current[i].make_closed(i)
    return [path, path_value]


def algorithm2(draw, grid, lst_start, T_step, T_max):
    edges = []
    n = len(lst_start)
    lst_check = [0 for i in range(n)]
    lst_count = [0 for i in range(n)]
    lst_open_set = [[] for i in range(n)]
    lst_came_from = [{} for i in range(n)]
    lst_g_score = [{} for i in range(n)]
    lst_f_score = [{} for i in range(n)]
    lst_open_set_hash = [{} for i in range(n)]
    path = [[[] for j in range(n)] for i in range(n)]
    path_value = [[0 for j in range(n)] for i in range(n)]
    check_path = [[0 for j in range(n)] for i in range(n)]
    max_count_path = 0
    check_grid = {lst_start[0]}
    for i in range(n):
        lst_count[i] = 0
        lst_open_set[i] = PriorityQueue()
        lst_open_set[i].put((0, lst_count[i], lst_start[i]))
        lst_came_from[i] = {}
        lst_g_score[i] = {spot: float("inf") for row in grid for spot in row}
        lst_g_score[i][lst_start[i]] = 0
        lst_f_score[i] = {spot: float("inf") for row in grid for spot in row}
        lst_f_score[i][lst_start[i]] = lst_g_score[i][lst_start[i]]
        lst_open_set_hash[i] = {lst_start[i]}
        check_grid.add(lst_start[i])
    run = True
    # min_neighbors = 5 #round(math.sqrt(n) * math.log1p(n))
    # min_max_count_path = n*min_neighbors - (min_neighbors * min_neighbors - (n%min_neighbors*(n%min_neighbors)-1))
    while run:
        # print(max_count_path)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        lst_current = [None for i in range(n)]
        for i in range(n):
            lst_current[i] = lst_open_set[i].get()[2]
            for j in range(n):

                if lst_count[0] >= T_max:
                    # print(lst_count[0])
                    if check_path_valid(fix_path_map(path, path_value) + [edges]):
                        return fix_path_map(path, path_value) + [edges]
                    else:
                        T_max += T_step
                if i != j and (lst_current[i] in lst_open_set_hash[j]) and check_path[i][j] == 0:
                    lst_check[i] += 1
                    lst_check[j] += 1
                    path_temp1 = [lst_current[i]] + reconstruct_path(lst_came_from[i], lst_current[i])
                    path_temp2 = [lst_current[i]] + reconstruct_path(lst_came_from[j], lst_current[i])
                    path_safe1 = reconstruct_path_safe(path_temp1, grid, lst_g_score[i], min_safe=1.5)
                    # path_safe1 = reconstruct_path_safe(path_safe1, grid, lst_g_score[i], min_safe=2.5)
                    path_safe2 = reconstruct_path_safe(path_temp2, grid, lst_g_score[j], min_safe=1.5)
                    # path_safe2 = reconstruct_path_safe(path_safe2, grid, lst_g_score[j], min_safe=2.5)
                    path_safe1.reverse()
                    path[i][j] = path_safe1 + path_safe2
                    temp_path = path[i][j]
                    temp_path.reverse()
                    path[j][i] = temp_path
                    check_path[i][j] = check_path[j][i] = 1
                    path_value[i][j] = path_value[j][i] = lst_g_score[i][lst_current[i]] + lst_g_score[j][lst_current[i]]
                    edges.append((path_value[i][j], (i, j)))
                    max_count_path += 2
                    if max_count_path >= n*(n-1):
                        # sum_edge = 0
                        # for p in lst_check:
                        #     sum_edge += p
                        # print(lst_check)
                        # print(sum_edge/((n-1)*n))
                        return fix_path_map(path, path_value) + [edges]
            for neighbor in lst_current[i].neighbors:
                temp_g_score = lst_g_score[i][lst_current[i]] + delta(lst_current[i].get_pos(), neighbor.get_pos())

                if temp_g_score < lst_g_score[i][neighbor]:
                    lst_came_from[i][neighbor] = lst_current[i]
                    lst_g_score[i][neighbor] = temp_g_score
                    lst_f_score[i][neighbor] = lst_g_score[i][neighbor]
                    if neighbor.safe >= 1.5 and neighbor not in lst_open_set_hash[i]:  # and neighbor not in check_grid:
                        lst_count[i] += 1
                        lst_open_set[i].put((lst_f_score[i][neighbor], lst_count[i], neighbor))
                        neighbor.make_open(i)
                        lst_open_set_hash[i].add(neighbor)
                        # check_grid.add(neighbor)
                    else:
                        neighbor.make_open(i)
        # if lst_count[0] % 20 == 0:
        #     draw()
        for i in range(n):
            if lst_current[i] not in lst_start:
                lst_current[i].make_closed(i)
    return [path, path_value]


def main(win, width):
    choose = 0
    rows = 200
    count_test = 0
    safe = float("inf")
    filemap = "map_IN2D/IN2D_17.txt"
    grid = make_grid(rows, width, safe)
    start = None
    end = None
    end2 = None
    end3 = None
    end4 = None
    end5 = None
    end6 = None
    end7 = None
    end8 = None
    end9 = None
    end10 = None
    end11 = None
    end12 = None
    end13 = None
    end14 = None
    end15 = None
    lst_start = []
    run = True
    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                    lst_start.append(start)

                elif not end and spot != start:
                    end = spot
                    end.make_end()
                    lst_start.append(end)

                elif not end2 and spot != start and spot != end:
                    end2 = spot
                    end2.make_end()
                    lst_start.append(end2)

                elif not end3 and spot != start and spot != end:
                    end3 = spot
                    end3.make_end()
                    lst_start.append(end3)

                elif not end4 and spot != start and spot != end:
                    end4 = spot
                    end4.make_end()
                    lst_start.append(end4)

                elif not end5 and spot != start and spot != end:
                    end5 = spot
                    end5.make_end()
                    lst_start.append(end5)

                elif not end6 and spot != start and spot != end:
                    end6 = spot
                    end6.make_end()
                    lst_start.append(end6)

                elif not end7 and spot != start and spot != end:
                    end7 = spot
                    end7.make_end()
                    lst_start.append(end7)

                elif not end8 and spot != start and spot != end:
                    end8 = spot
                    end8.make_end()
                    lst_start.append(end8)

                elif not end9 and spot != start and spot != end:
                    end9 = spot
                    end9.make_end()
                    lst_start.append(end9)

                elif not end10 and spot != start and spot != end:
                    end10 = spot
                    end10.make_end()
                    lst_start.append(end10)

                elif not end11 and spot != start and spot != end:
                    end11 = spot
                    end11.make_end()
                    lst_start.append(end11)

                elif not end12 and spot != start and spot != end:
                    end12 = spot
                    end12.make_end()
                    lst_start.append(end12)

                elif not end13 and spot != start and spot != end:
                    end13 = spot
                    end13.make_end()
                    lst_start.append(end13)

                elif not end14 and spot != start and spot != end:
                    end14 = spot
                    end14.make_end()
                    lst_start.append(end14)

                elif not end15 and spot != start and spot != end:
                    end15 = spot
                    end15.make_end()
                    lst_start.append(end15)

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
                elif spot == end2:
                    end2 = None

            # run
            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_e:
                #     lst_start = read_map_from_file2(grid, rows, "square402.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.59)
                #     T_max = 160000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                # if event.key == pygame.K_r:
                #     lst_start = read_map_from_file2(grid, rows, "square401.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.59)
                #     T_max = 160000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                # if event.key == pygame.K_t:
                #     lst_start = read_map_from_file2(grid, rows, "square400.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.59)
                #     T_max = 160000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                if event.key == pygame.K_1:
                    choose = 1
                if event.key == pygame.K_2:
                    choose = 0
                if event.key == pygame.K_8:
                    gen_random_map(filemap, 54)
                if event.key == pygame.K_9:
                    # filemap = "map_IN2D/IN2D_01.txt"
                    # gen_random_map(filemap, 58)
                    data = read_map_from_file2(grid, rows, filemap)
                    lst_start = data[0]
                    start = lst_start[0]
                    end = lst_start[1]
                    # T_step = 200
                    # print(n, len(lst_start), T_max)
                # if event.key == pygame.K_w:
                #     lst_start = read_map_from_file2(grid, rows, "map200_RD2.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.45)
                #     T_max = 40000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                # if event.key == pygame.K_p:
                #     lst_start = read_map_from_file2(grid, rows, "map_unknow/map200mix.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log2(len(lst_start)+1)) * (1 - 0.25)
                #     T_max = 40000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                # if event.key == pygame.K_u:
                #     lst_start = read_map_from_file2(grid, rows, "map_unknow/obstacle95.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.92)
                #     T_max = 40000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                # if event.key == pygame.K_i:
                #     lst_start = read_map_from_file2(grid, rows, "map_unknow/obstacle85.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.8)
                #     T_max = 40000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                # if event.key == pygame.K_o:
                #     lst_start = read_map_from_file2(grid, rows, "map_unknow/warehouse4.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.36)
                #     T_max = 40000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                #     # print(len(lst_start))
                # if event.key == pygame.K_a:
                #     lst_start = read_map_from_file2(grid, rows, "map_unknow/warehouse3.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.28)
                #     T_max = 40000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                # if event.key == pygame.K_s:
                #     lst_start = read_map_from_file2(grid, rows, "map_unknow/mixed2002.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.251)
                #     T_max = 40000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                # if event.key == pygame.K_d:
                #     lst_start = read_map_from_file2(grid, rows, "map_unknow/mixed200.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.25)
                #     T_max = 40000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                # if event.key == pygame.K_y:
                #     lst_start = read_map_from_file2(grid, rows, "map_unknow/map200_00.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.17)
                #     T_max = 40000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                # if event.key == pygame.K_q:
                #     lst_start = read_map_from_file2(grid, rows, "map_unknow/map200_RD.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.22)
                #     T_max = 10000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                # if event.key == pygame.K_g:
                #     lst_start = read_map_from_file2(grid, rows, "map_unknow/obstacle90.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.82)
                #     T_max = 10000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                # if event.key == pygame.K_h:
                #     lst_start = read_map_from_file2(grid, rows, "map_unknow/obstacle80.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.87)
                #     T_max = 10000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                # if event.key == pygame.K_j:
                #     lst_start = read_map_from_file2(grid, rows, "map_unknow/warehouse1.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.4)
                #     T_max = 10000 / n
                #     min_neighbors = math.sqrt(len(lst_start)) + 1
                # if event.key == pygame.K_k:
                #     lst_start = read_map_from_file2(grid, rows, "map_unknow/warehouse2.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.62)
                #     T_max = 10000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                # if event.key == pygame.K_v:
                #     lst_start = read_map_from_file2(grid, rows, "map_unknow/map104_00.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.62)
                #     T_max = 10000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                # if event.key == pygame.K_b:
                #     lst_start = read_map_from_file2(grid, rows, "map_unknow/map103_00.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.62)
                #     T_max = 10000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                # if event.key == pygame.K_n:
                #     lst_start = read_map_from_file2(grid, rows, "map_unknow/map102_00.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.36)
                #     T_max = 10000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                # if event.key == pygame.K_m:
                #     lst_start = read_map_from_file2(grid, rows, "map_unknow/map101_00.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.41)
                #     T_max = 10000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                # if event.key == pygame.K_l:
                #     lst_start = read_map_from_file2(grid, rows, "map_unknow/map100_00.txt")
                #     start = lst_start[0]
                #     end = lst_start[1]
                #     n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)+1)) * (1 - 0.17)
                #     T_max = 10000 / n
                #     min_neighbors = math.sqrt(len(lst_start))
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    if choose == 0:
                        count_test += 1
                        print("new test: " + str(count_test))
                        T_max = 500
                        T_step = 200
                        start_time = time.time()
                        temp_path = algorithm(lambda: draw(win, grid, rows, width), grid, lst_start, T_step, T_max)
                        path = temp_path[0]
                        path_value = temp_path[1]
                        edges = temp_path[2]

                        path_value = np.array(path_value)
                        # print(path_value)

                        # start_time = time.time()
                        c = CRIST(path_value)
                        ds = c.ans(edges)
                        ds = sort_ds(ds)
                        # print("Số điểm đi là: ", len(ds) - 1)
                        end_time = time.time()
                        time_running = end_time - start_time
                        # print("Thời gian chạy là: ", time_running)
                        print(round(time_running, 4))
                        draw_path_final(path, path_value, ds, lst_start, grid, lambda: draw(win, grid, rows, width))
                        safety = calculate_safety(path)
                        # print("Độ an toàn trung bình FFT là: ", safety)
                        print(round(safety, 2))

                        # start_time3 = time.time()
                        # GWO_value2 = run_GWO(path_value)
                        # end_time3 = time.time()
                        # time_running3 = end_time3 - start_time3

                        # start_time4 = time.time()
                        # aco = ACO(50, 200, 1.0, 20.0, 0.5, 10, 2)
                        # graph = Graph(path_value, len(path_value))
                        # aco_value = aco.solve(graph)
                        # end_time4 = time.time()
                        # time_running4 = end_time4 - start_time4

                        # aco2 = ACO(50, 100, 1.0, 20.0, 0.5, 10, 2)
                        # graph2 = Graph(path_value, len(path_value))
                        # aco_value2 = aco2.solve(graph2)

                        # print("Thời gian chạy ACO là: ", time_running4)
                        #print(aco_value[0])
                        # print("Độ dài quãng đường ACO là: ", aco_value[1])

                        # print("Độ dài quãng đường ACO2 là: ", aco_value2[1])


                        # print("Thời gian chạy GWO2 là: ", time_running3)
                        # # print(GWO_value[0])
                        # print("Độ dài quãng đường GWO2 là: ", GWO_value2[1])

                        # safety = calculate_safety(GWO_value[0])
                        # print("Độ an toàn trung bình GWO là: ", safety)
                        # print(path_value)

                if choose == 1:
                    T_max = 40000
                    T_step = 0
                    start_time = time.time()
                    temp_path = algorithm2(lambda: draw(win, grid, rows, width), grid, lst_start, T_step, T_max)
                    path = temp_path[0]
                    path_value = temp_path[1]
                    edges = temp_path[2]
                    path_value = np.array(path_value)
                    c = CRIST(path_value)
                    ds = c.ans(edges)
                    ds = sort_ds(ds)
                    end_time = time.time()
                    time_running = end_time - start_time
                    # print("Thời gian chạy là: ", time_running)
                    print(round(time_running, 2))
                    draw_path_final(path, path_value, ds, lst_start, grid, lambda: draw(win, grid, rows, width))
                    safety = calculate_safety(path)
                    # print("Độ an toàn trung bình FFT là: ", safety)
                    print(round(safety, 2))
                    break

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    end2 = None
                    end3 = None
                    end4 = None
                    end5 = None
                    end6 = None
                    end7 = None
                    end8 = None
                    end9 = None
                    end10 = None
                    end11 = None
                    end12 = None
                    end13 = None
                    end14 = None
                    end15 = None
                    lst_start = []
                    grid = make_grid(rows, width, safe)

                if event.key == pygame.K_f:
                    safe_zone(lambda: draw(win, grid, rows, width), rows, grid)
            # end

    pygame.quit()
'''
            # run to find n_max
            filemap = "map_IN2D/IN2D_02.txt"
            gen_random_map(filemap, 53)
            lst_start = read_map_from_file2(grid, rows, filemap)
            start = lst_start[0]
            end = lst_start[1]
            n = math.sqrt(len(lst_start)) * (math.log10(len(lst_start)) + 1) * (1 - 0.36)
            n_min = round(n / 2)
            n_max = round(n * 2)
            n_run = n_max
            safe_best = 0
            runtime_best = 0
            path_lenght_best = 0
            while n_run >= n_min:
                gen_random_map(filemap, 53)
                lst_start = read_map_from_file2(grid, rows, filemap)
                start = lst_start[0]
                end = lst_start[1]
                T_max = 40000 / n
                min_neighbors = math.sqrt(len(lst_start))
                start_time = time.time()
                temp_path = algorithm(lambda: draw(win, grid, rows, width), grid, lst_start, T_max, min_neighbors)
                path = temp_path[0]
                path_value = temp_path[1]
                edges = temp_path[2]
                path_value = np.array(path_value)
                c = CRIST(path_value)
                # ds = c.ans(edges)
                # ds = sort_ds(ds)
                safety = calculate_safety(path)
                # print("Độ an toàn trung bình là: ", safety)
                end_time = time.time()
                time_running = end_time - start_time
                # print("Thời gian chạy là: ", time_running)
                path_lenght = caculate_path(path, path_value, ds, lst_start, grid)

                if path_lenght < 10000 or n_run == n_min:
                    safe_best = safety
                    runtime_best = time_running
                    path_lenght_best = path_lenght
                    print("Kết quả tối ưu là:", n_run, path_lenght_best, runtime_best, safe_best)
                    break
                start = None
                end = None
                lst_start = []
                grid = make_grid(rows, width, safe)
                n_run -= 1
            # end while
'''



main(WIN, WIDTH)
