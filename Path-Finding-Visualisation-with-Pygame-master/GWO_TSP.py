#
#
# import numpy as np
#
#
# class GreyWolfOptimizer:
#     def __init__(self, distance_matrix, max_iterations, population_size):
#         self.distance_matrix = distance_matrix
#         self.num_cities = len(distance_matrix)
#         self.max_iterations = max_iterations
#         self.population_size = population_size
#
#     def optimize(self, num_cities):
#         alpha_pos = np.zeros(self.num_cities)
#         beta_pos = np.zeros(self.num_cities)
#         delta_pos = np.zeros(self.num_cities)
#         alpha_score = float('inf')
#         beta_score = float('inf')
#         delta_score = float('inf')
#
#         # Khởi tạo quần thể
#         population = np.zeros((self.population_size, self.num_cities), dtype=int)
#         for i in range(self.population_size):
#             population[i, :] = np.random.permutation(self.num_cities)
#             # print(population)
#
#         iteration = 0
#         while iteration < self.max_iterations:
#             for i in range(self.population_size):
#                 # Tính fitness cho mỗi cá thể
#                 fitness = self.calculate_fitness(population[i, :])
#
#                 if fitness < alpha_score:
#                     delta_score = beta_score
#                     delta_pos = beta_pos.copy()
#                     beta_score = alpha_score
#                     beta_pos = alpha_pos.copy()
#                     alpha_score = fitness
#                     alpha_pos = population[i, :].copy()
#                 elif fitness < beta_score:
#                     delta_score = beta_score
#                     delta_pos = beta_pos.copy()
#                     beta_score = fitness
#                     beta_pos = population[i, :].copy()
#                 elif fitness < delta_score:
#                     delta_score = fitness
#                     delta_pos = population[i, :].copy()
#
#             a = 2 - iteration * ((2) / self.max_iterations)
#
#             # Cập nhật vị trí đàn sói
#             for i in range(self.population_size):
#                 for j in range(self.num_cities):
#                     r1 = np.random.rand()
#                     r2 = np.random.rand()
#                     A1 = 2 * a * r1 - a
#                     C1 = 2 * r2
#                     D_alpha = abs(C1 * alpha_pos[j] - population[i, j])
#                     X1 = alpha_pos[j] - A1 * D_alpha
#
#                     r1 = np.random.rand()
#                     r2 = np.random.rand()
#                     A2 = 2 * a * r1 - a
#                     C2 = 2 * r2
#                     D_beta = abs(C2 * beta_pos[j] - population[i, j])
#                     X2 = beta_pos[j] - A2 * D_beta
#
#                     r1 = np.random.rand()
#                     r2 = np.random.rand()
#                     A3 = 2 * a * r1 - a
#                     C3 = 2 * r2
#                     D_delta = abs(C3 * delta_pos[j] - population[i, j])
#                     X3 = delta_pos[j] - A3 * D_delta
#
#                     X1, X2, X3 = round(X1), round(X2), round(X3)
#                     X_tb = round((X1 + X2 + X3)/3)
#                     if X_tb >= num_cities:
#                         X_tb = num_cities - 1
#                     if X_tb < 0:
#                         X_tb = 0
#                     population[i, j] = X_tb
#                     print(X1, X2, X3)
#
#             iteration += 1
#
#         best_solution = alpha_pos.tolist()
#         best_distance = self.calculate_total_distance(best_solution)
#
#         return best_solution, best_distance
#
#     def calculate_fitness(self, solution):
#         return self.calculate_total_distance(solution)
#
#     def calculate_total_distance(self, solution):
#         total_distance = 0.0
#         #print(solution)
#         for i in range(self.num_cities - 1):
#             city1 = solution[i]
#             city2 = solution[i + 1]
#             total_distance += self.distance_matrix[city1, city2]
#         total_distance += self.distance_matrix[solution[-1], solution[0]]
#         return total_distance
#
#
# def GWO(path_value):
#     num_cities = len(path_value)
#     # search_space = (0, 100)
#     max_iterations = round(num_cities * 2)
#     population_size = round(num_cities/2)
#
#     # Generate random distance matrix
#     # distance_matrix = np.random.uniform(search_space[0], search_space[1], size=(num_cities, num_cities))
#     # distance_matrix = (distance_matrix + distance_matrix.T) / 2
#     # np.fill_diagonal(distance_matrix, 0)
#     distance_matrix = path_value
#
#     gwo = GreyWolfOptimizer(distance_matrix, max_iterations, population_size)
#     best_solution, best_distance = gwo.optimize(num_cities)
#
#     # print(distance_matrix)
#     print("Best solution:", best_solution)
#     # print("Best distance:", best_distance)
#     return best_distance


import random
import numpy as np
import math
import itertools


def tsp(distance_matrix):
    num_cities = len(distance_matrix)
    all_cities = set(range(num_cities))
    shortest_path = None
    shortest_distance = float('inf')

    for path in itertools.permutations(all_cities):
        current_distance = 0
        for i in range(num_cities - 1):
            current_distance += distance_matrix[path[i]][path[i+1]]
        current_distance += distance_matrix[path[-1]][path[0]]  # Quay lại điểm bắt đầu

        if current_distance < shortest_distance:
            shortest_distance = current_distance
            shortest_path = path

    return shortest_path, shortest_distance


def generate_random_solution(n):
    solution = list(range(0, n))
    random.shuffle(solution)
    return solution


def calculate_SS(S1, S2):

    # Cách tính 1
    SS = []
    n = len(S1)
    for count in range(n):
        for i in range(n):
            if S1[i] == S2[count] and i != count and [i, count] not in SS:
                SS.append([i, count])
    # SS.sort(key=lambda x: x[1], reverse=False)
    return SS

    # Cách tính 2
    # positions = []
    # for i in range(len(S1)):
    #     if S1[i] != S2[i]:
    #         positions.append((i, S2.index(S1[i])))
    # return positions


def calculate_basic_swap_sequence(SS1, SS2, SS3):
    a = random.random()
    b = random.random()
    c = random.random()

    SS1_sub = SS1[:int(a * len(SS1))]
    SS2_sub = SS2[:int(b * len(SS2))]
    SS3_sub = SS3[:int(c * len(SS3))]

    # print("SS1: ", SS1, "SS2: ", SS2, "SS3: ", SS3)
    SS = []
    for i in range(len(SS1_sub)):
        SS.append(SS1_sub[i])
    for i in range(len(SS2_sub)):
        SS.append(SS2_sub[i])
    for i in range(len(SS3_sub)):
        SS.append(SS3_sub[i])

    # Sắp xếp cặp (i, j) sao cho giá trị tăng dần theo i
    for x in SS:
        if x[0] > x[1]:
            tmp = x[0]
            x[0] = x[1]
            x[1] = tmp

    # Loại bỏ cac giá trị thừa
    seen = []
    SS_last = []
    for element in SS:
        if element not in seen:
            seen.append(element)
            SS_last.append(element)

    return SS_last


def update_solution(Xt, BSS, matx_cost):
    Xt_best = Xt
    Xt_cost = calculate_cost(Xt, matx_cost)
    for swap in BSS:
        position1, position2 = swap
        Xt[position1], Xt[position2] = Xt[position2], Xt[position1]
        tmp_cost = calculate_cost(Xt, matx_cost)
        if tmp_cost < Xt_cost:
            Xt_best = Xt
            Xt_cost = tmp_cost
    return [Xt_best, Xt_cost]


def calculate_cost(Xt, matx_cost):
    distance = 0
    for i in range(len(matx_cost) - 1):
        distance += matx_cost[Xt[i]][Xt[i+1]]
    distance += matx_cost[Xt[-1]][Xt[0]]
    return distance


# Xa = [10, 7, 6, 9, 2, 4, 3, 5, 8, 1]
# Xb = [4, 10, 8, 5, 1, 2, 3, 7, 9, 6]
# Xc = [9, 6, 7, 3, 2, 4, 10, 5, 8, 1]
# Xt = [3, 7, 6, 9, 2, 4, 10, 5, 8, 1]
#
# SS1 = calculate_SS(Xa, Xt)
# SS2 = calculate_SS(Xb, Xt)
# SS3 = calculate_SS(Xc, Xt)
# print(SS1)
# print(SS2)
# print(SS3)
#
# lst = np.random.uniform(20, 50, size=(10, 10))
# lst = (lst + lst.T) / 2
# np.fill_diagonal(lst, 0)
#

# SS = calculate_basic_swap_sequence(SS1, SS2, SS3)
# Xt = update_solution(Xt, SS)
# tmp = calculate_cost(Xt, lst)
# print(Xt)
# print(tmp)


def GWO(path_value):
    matx_cost = path_value
    n = len(path_value)
    # Xa = generate_random_solution(n)
    # costXa = calculate_cost(Xa, path_value)
    # Xb = generate_random_solution(n)
    # costXb = calculate_cost(Xb, path_value)
    # Xc = generate_random_solution(n)
    # costXc = calculate_cost(Xc, path_value)
    # Xt = generate_random_solution(n)
    # costXt = calculate_cost(Xt, path_value)
    lst = []
    for i in range(500):
        X_tmp = generate_random_solution(n)
        costX_tmp = calculate_cost(X_tmp, path_value)
        lst.append([X_tmp, costX_tmp])

    lst.sort(key=lambda x: x[1], reverse=False)
    lstX = [x[0] for x in lst]
    lst_costX = [x[1] for x in lst]
    lst_abc = lstX[:3]
    lst_cost_abc = lst_costX[:3]
    #print(lst_cost_abc)
    lstXt = lstX

    # print(lstX)
    # print(lst_costX)

    Iteration = 100
    #count_stop = 0
    for i in range(Iteration):
        # print(lst_cost_abc[0])
    #while count_stop < 10:
        for j in range(len(lstXt)):
            Xt = lstXt[j]

            SS1 = calculate_SS(lst_abc[0], Xt)
            SS2 = calculate_SS(lst_abc[1], Xt)
            SS3 = calculate_SS(lst_abc[2], Xt)
            SS = calculate_basic_swap_sequence(SS1, SS2, SS3)
            # print("SS: ", SS)

            Xt_costXt_new = update_solution(Xt, SS, matx_cost)
            Xt_new = Xt_costXt_new[0]
            lstXt[j] = Xt_new
            costXt_new = Xt_costXt_new[1]
            # print(costXt_new)
            if costXt_new < lst_cost_abc[0]:
                # count_stop += 1
                lst_abc = [Xt_new] + [lst_abc[0]] + [lst_abc[1]]
                lst_cost_abc = [costXt_new] + [lst_cost_abc[0]] + [lst_cost_abc[1]]
            if costXt_new < lst_cost_abc[1]:
                lst_abc = [lst_abc[0]] + [Xt_new] + [lst_abc[1]]
                lst_cost_abc = [lst_cost_abc[0]] + [costXt_new] + [lst_cost_abc[1]]
            if costXt_new < lst_cost_abc[2]:
                lst_abc = [lst_abc[0]] + [lst_abc[1]] + [Xt_new]
                lst_cost_abc = [lst_cost_abc[0]] + [lst_cost_abc[1]] + [costXt_new]

            # else:
            # count_stop += 1
    # print(count_stop)
    return [lst_abc[0], lst_cost_abc[0]]


def GWO_TSP(path_value):
    # n = len(path_value) * 2
    result = GWO(path_value)
    Xt_min = result[0]
    costXt_min = result[1]

    # for i in range(n):
    #     result = GWO(path_value)
    #     if costXt_min > result[1]:
    #         Xt_min = result[0]
    #         costXt_min = result[1]
    return [Xt_min, costXt_min]


# lst = np.random.uniform(20, 50, size=(10, 10))
# lst = (lst + lst.T) / 2
# np.fill_diagonal(lst, 0)
# for row in lst:
#     print('[', end='')
#     for i, element in enumerate(row):
#         print(element, end='')
#         if i < len(row) - 1:
#             print(', ', end='')
#     print(']')
# lst = [[0, 34,50756334578302, 22.854323573670655, 33.133881472831305, 32.44642041709688, 32.29077171568983, 41.32745363200192, 34.60589997533138, 33.47327581167178, 33.36414353639994],
#        [34.50756334578302, 0.0, 38.78526567957931, 27.14678426375078, 24.976164104481533, 39.88816151428006, 35.75919464567039, 35.344578366931536, 40.08687419857077, 32.961942356847985],
#        [22.854323573670655, 38.78526567957931, 0.0, 45.84955456018835, 24.58090178664591, 35.772531974959925, 41.319011454574905, 27.190815290383252, 31.940434534984426, 39.56307056885795],
#        [33.133881472831305, 27.14678426375078, 45.84955456018835, 0.0, 32.88685893405129, 32.09656022348861, 33.96111295709401, 47.0656728596857, 29.831942693779794, 31.277746354553134],
#        [32.44642041709688, 24.976164104481533, 24.58090178664591, 32.88685893405129, 0.0, 38.457613174525484, 35.93499801770572, 31.71573745206073, 31.490184659670156, 36.00604303147982],
#        [32.29077171568983, 39.88816151428006, 35.772531974959925, 32.09656022348861, 38.457613174525484, 0.0, 30.396645871185164, 35.84222349439915, 36.55583525828927, 25.88385368553901],
#        [41.32745363200192, 35.75919464567039, 41.319011454574905, 33.96111295709401, 35.93499801770572, 30.396645871185164, 0.0, 32.12173391538704, 33.46664896531891, 34.70521173290715],
#        [34.60589997533138, 35.344578366931536, 27.190815290383252, 47.0656728596857, 31.71573745206073, 35.84222349439915, 32.12173391538704, 0.0, 37.16273254233167, 25.19904764705158],
#        [33.47327581167178, 40.08687419857077, 31.940434534984426, 29.831942693779794, 31.490184659670156, 36.55583525828927, 33.46664896531891, 37.16273254233167, 0.0, 23.16907986026424],
#        [33.36414353639994, 32.961942356847985, 39.56307056885795, 31.277746354553134, 36.00604303147982, 25.88385368553901, 34.70521173290715, 25.19904764705158, 23.16907986026424, 0.0]]
#
# result = GWO(lst)
# Xt_min = result[0]
# costXt_min = result[1]
# print(Xt_min)
# print(costXt_min)
#
# for i in range(200):
#     result = GWO(lst)
#     if costXt_min > result[1]:
#         Xt_min = result[0]
#         costXt_min = result[1]
#

# print()
#print(best_Xt)
# ((1, 4, 8, 9, 5, 6, 7, 2, 0, 3), 268.0839087980025)