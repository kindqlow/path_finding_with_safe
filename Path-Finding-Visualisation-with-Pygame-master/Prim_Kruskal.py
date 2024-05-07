import time


def kruskal(edges):
    # Hàm tạo cây MST từ tập các cạnh và trọng số
    # edges: [(weight, (vertex1, vertex2)), ...]
    # Trả về danh sách các cạnh trong cây MST

    parent = {}  # Lưu cha của mỗi đỉnh

    def find(v):
        # Hàm tìm cha của đỉnh v
        if parent[v] != v:
            parent[v] = find(parent[v])
        return parent[v]

    def union(v1, v2):
        # Hàm kết hợp hai tập hợp chứa v1 và v2 thành một tập hợp duy nhất
        root1 = find(v1)
        root2 = find(v2)

        if root1 != root2:
            parent[root2] = root1

    # Sắp xếp các cạnh theo trọng số tăng dần
    edges.sort(key=lambda x: x[0])

    mst = []  # Danh sách các cạnh trong cây MST

    for edge in edges:
        weight, (v1, v2) = edge
        if v1 not in parent:
            parent[v1] = v1
        if v2 not in parent:
            parent[v2] = v2

        if find(v1) != find(v2):
            union(v1, v2)
            mst.append(edge)

    return mst

# Tập các cạnh và trọng số
edges = [(13.899494936611664, (8, 11)), (14.31370849898476, (8, 7)), (15.485281374238571, (9, 1)), (15.899494936611664, (10, 9)), (16.556349186104047, (1, 3)), (16.727922061357855, (0, 5)), (18.556349186104047, (2, 8)), (18.656854249492383, (6, 13)), (18.727922061357855, (0, 4)), (18.727922061357855, (4, 2)), (19.31370849898476, (1, 14)), (19.48528137423857, (8, 10)), (20.242640687119287, (9, 6)), (22.82842712474619, (11, 12))]

stat_time = time.time()
mst = kruskal(edges)
end_time = time.time()
time_running = end_time - stat_time
print(time_running)
print(mst)
