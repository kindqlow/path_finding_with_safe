import numpy as np
import sys
import math
from Map_Grid import *
from TSP_cristofides_2 import *


# nhánh cận chay
def tsp(distance_matrix):
    num_cities = len(distance_matrix)
    visited = [False] * num_cities  # Danh sách kiểm tra các thành phố đã được thăm
    path = [0]  # Đường đi bắt đầu từ điểm 0
    min_cost = math.inf  # Giá trị lớn nhất để so sánh và cập nhật chi phí nhỏ nhất
    best_path = []  # Danh sách các điểm đi qua trong chu trình ngắn nhất

    def calculate_cost():
        # Tính toán chi phí của đường đi hiện tại
        cost = 0
        for i in range(len(path) - 1):
            cost += distance_matrix[path[i]][path[i+1]]
        cost += distance_matrix[path[-1]][path[0]]  # Cộng chi phí trở lại điểm ban đầu
        return cost

    def backtrack(curr_city, cost):
        nonlocal min_cost
        nonlocal best_path

        if len(path) == num_cities:  # Nếu đã đi qua tất cả các thành phố
            if distance_matrix[curr_city][0] != 0:  # Kiểm tra có thể quay trở lại điểm ban đầu
                cost += distance_matrix[curr_city][0]  # Cộng chi phí trở lại điểm ban đầu
                if cost < min_cost:  # Nếu chi phí nhỏ hơn chi phí nhỏ nhất hiện tại
                    min_cost = cost
                    best_path = path.copy()
            return

        for next_city in range(num_cities):
            if not visited[next_city] and distance_matrix[curr_city][next_city] != 0:
                # Thăm thành phố tiếp theo nếu chưa được thăm và có đường đi hợp lệ
                visited[next_city] = True
                path.append(next_city)
                backtrack(next_city, cost + distance_matrix[curr_city][next_city])
                # Quay lui và thử các thành phố khác
                visited[next_city] = False
                path.pop()

    visited[0] = True  # Đánh dấu điểm đầu tiên đã được thăm
    backtrack(0, 0)  # Bắt đầu từ điểm đầu tiên
    best_path.append(0)  # Thêm điểm ban đầu vào cuối danh sách để tạo chu trình
    return best_path


# nhánh cận hiệu quả
def efficient_branching(distance_matrix):
    num_cities = distance_matrix.shape[0]
    visited = [False] * num_cities
    visited[0] = True
    current_path = [0]
    min_cost = np.inf
    optimal_path = None

    def branch_and_bound(current_city, current_cost, depth):
        nonlocal min_cost, optimal_path

        if depth == num_cities - 1:
            total_cost = current_cost + distance_matrix[current_city, 0]
            if total_cost < min_cost:
                min_cost = total_cost
                optimal_path = current_path[:]
                optimal_path.append(0)
            return

        for next_city in range(1, num_cities):
            if not visited[next_city] and distance_matrix[current_city, next_city] < 200:
                current_cost += distance_matrix[current_city, next_city]
                if current_cost < min_cost:
                    visited[next_city] = True
                    current_path.append(next_city)
                    branch_and_bound(next_city, current_cost, depth + 1)
                    current_path.pop()
                    visited[next_city] = False
                current_cost -= distance_matrix[current_city, next_city]

    branch_and_bound(0, 0, 0)

    return optimal_path


def check_fast_marching_tsp(lst_check, T, T_max, min_neighbors):
    n = len(lst_check)
    for i in range(n):
        if lst_check[i] < min_neighbors and T >= T_max:
            T_max += 40000/(len(lst_check)**2)
            # T_max += 100
            return False
    return True


def check_path_valid(paths):
    path_value = paths[1]
    edges = paths[2]
    c = CRIST(path_value)
    ds = c.ans(edges)

    # Tính toán độ dài đường đi
    n = len(ds)
    path_length = 0
    count = 1
    while count < n:
        path_length += path_value[ds[count - 1]][ds[count]]
        count += 1
    # Kiểm tra đường đi hợp lệ
    if path_length < 10000:
        return True
    else:
        # print(path_length)
        return False


# Cristofides
def tsp_cristofides(dist_matrix):
    #print(dist_matrix)
    num_cities = len(dist_matrix)

    # Step 1: Create the minimum spanning tree (MST)
    mst = create_mst(dist_matrix)
    # print("MST: ")
    # print(mst)

    # Step 2: Find the odd-degree vertices in the MST
    odd_vertices = find_odd_vertices(mst)
    # print("Tập đỉnh có số cạnh lẻ")
    # print(odd_vertices)

    # Step 3: Create a minimum spanning tree of the odd-degree vertices
    odd_vertices_mst = create_odd_vertices_mst(dist_matrix, odd_vertices)
    # print("MST với các đỉnh có số cạnh lẻ")
    # print(odd_vertices_mst)

    # Step 4: Merge the MST and the odd vertices MST
    combined_mst = merge_msts(mst, odd_vertices_mst)
    # print("Cây kết hợp")
    # print(combined_mst)

    # Step 5: Find an Eulerian tour in the combined MST
    eulerian_tour = find_eulerian_tour(combined_mst)
    print("Chu trình Eulerian: ")
    print(eulerian_tour)

    # Step 6: Find a Hamiltonian tour by removing duplicate cities from the Eulerian tour
    hamiltonian_tour = find_hamiltonian_tour(eulerian_tour)

    return hamiltonian_tour


def create_mst(dist_matrix):
    num_vertices = len(dist_matrix)

    mst = np.zeros_like(dist_matrix)

    visited = [False] * num_vertices
    key = [sys.maxsize] * num_vertices
    parent = [-1] * num_vertices

    key[0] = 0
    parent[0] = -1

    for _ in range(num_vertices):
        min_key = sys.maxsize
        min_vertex = -1

        for v in range(num_vertices):
            if not visited[v] and key[v] < min_key:
                min_key = key[v]
                min_vertex = v

        visited[min_vertex] = True

        for v in range(num_vertices):
            if (
                    not visited[v]
                    and dist_matrix[min_vertex][v] < key[v]
            ):
                parent[v] = min_vertex
                key[v] = dist_matrix[min_vertex][v]

    for v in range(1, num_vertices):
        mst[parent[v]][v] = dist_matrix[parent[v]][v]
        mst[v][parent[v]] = dist_matrix[parent[v]][v]

    return mst


def find_odd_vertices(mst):
    degrees = np.sum(mst > 0, axis=0)
    odd_vertices = [v for v, degree in enumerate(degrees) if degree % 2 != 0]
    return odd_vertices


def create_odd_vertices_mst(dist_matrix, odd_vertices):
    num_vertices = len(dist_matrix)
    num_odd_vertices = len(odd_vertices)

    odd_vertices_mst = np.zeros_like(dist_matrix)

    for i in range(num_odd_vertices):
        min_dist = sys.maxsize
        min_vertex = -1

        for j in range(num_odd_vertices):
            if i != j and dist_matrix[odd_vertices[i]][odd_vertices[j]] < min_dist:
                min_dist = dist_matrix[odd_vertices[i]][odd_vertices[j]]
                min_vertex = odd_vertices[j]

        odd_vertices_mst[odd_vertices[i]][min_vertex] = min_dist
        odd_vertices_mst[min_vertex][odd_vertices[i]] = min_dist

    return odd_vertices_mst


def merge_msts(mst1, mst2):
    return np.maximum(mst1, mst2)


def find_eulerian_tour(graph):
    num_vertices = len(graph)
    eulerian_tour = []
    current_vertex = 0

    while True:
        eulerian_tour.append(current_vertex)
        unvisited_edges = np.nonzero(graph[current_vertex])[0]

        if len(unvisited_edges) == 0:
            break

        next_vertex = unvisited_edges[0]
        graph[current_vertex][next_vertex] = 0
        graph[next_vertex][current_vertex] = 0
        current_vertex = next_vertex

    return eulerian_tour


def reconstruct_path(came_from, current):
    lst = []
    while current in came_from:
        current = came_from[current]
        lst.append(current)
    return lst


def find_hamiltonian_tour(eulerian_tour):
    visited = set()
    hamiltonian_tour = []

    for vertex in eulerian_tour:
        if vertex not in visited:
            visited.add(vertex)
            hamiltonian_tour.append(vertex)

    hamiltonian_tour.append(hamiltonian_tour[0])  # Go back to the starting city
    return hamiltonian_tour


# Fast marching đơn lẻ
def fast_marching(grid, start, end):
    lst = []
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
            lst = reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return lst

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + delta(current.get_pos(), neighbor.get_pos())

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = g_score[neighbor]
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    neighbor.make_open()
                    open_set_hash.add(neighbor)
                else:
                    neighbor.make_open()

        # draw()

        if current != start:
            current.make_closed()

    return lst


def calculate_safety(path):
    num = 0
    safety = 0
    medium_safety = 0
    lst = path[0][1]
    # print(path[1])

    for point in lst:
        if point.get_safe() > 1000:
            safety += 0
        else:
            safety += point.get_safe()
        num += 1

    if num != 0:
        medium_safety = safety/num
    return medium_safety
