def main(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    edges = []
    max_vertex_label = 0

    for line in lines:
        parts = [p for p in line.split(',')]
        if len(parts) != 2:
            continue
        try:
            u = int(parts[0])
            v = int(parts[1])
        except ValueError:
            continue
        edges.append((u, v))
        if u > max_vertex_label:
            max_vertex_label = u
        if v > max_vertex_label:
            max_vertex_label = v

    size = max_vertex_label
    matrix = [[0 for _ in range(size)] for _ in range(size)]

    for u, v in edges:
        matrix[u - 1][v - 1] = 1

    for row in matrix:
        print(' '.join(str(x) for x in row))



import sys
import os

input_path = ''
if len(sys.argv) > 1:
    input_path = sys.argv[1]

main(input_path)
