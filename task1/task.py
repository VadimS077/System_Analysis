import argparse
from typing import List, Tuple


def main(s: str, e: str) -> Tuple[
    List[List[bool]],
    List[List[bool]], 
    List[List[bool]],
    List[List[bool]],
    List[List[bool]]
]:
    edges = []
    nodes = set()

    lines = s.strip().split('\n')
    for line in lines:
        if line:
            parts = line.split(',')
            if len(parts) == 2:
                start, end = parts[0].strip(), parts[1].strip()
                edges.append((start, end))
                nodes.add(start)
                nodes.add(end)

    node_list = sorted(nodes, key=lambda x: int(x))
    node_index = {node: idx for idx, node in enumerate(node_list)}
    n = len(node_list)

    # 1. Матрица родитель-потомок
    parent_child = [[False] * n for _ in range(n)]
    for start, end in edges:
        parent_child[node_index[start]][node_index[end]] = True

    # 2. Матрица прямого доминирования
    direct_dominance = [[False] * n for _ in range(n)]

    def get_all_descendants(node, visited=None):
        if visited is None:
            visited = set()
        descendants = set()
        for start, end in edges:
            if start == node and end not in visited:
                descendants.add(end)
                visited.add(end)
                descendants.update(get_all_descendants(end, visited))
        return descendants

    for node in node_list:
        descendants = get_all_descendants(node)
        for desc in descendants:
            direct_dominance[node_index[node]][node_index[desc]] = True

    # 3. Матрица непрямого доминирования
    indirect_dominance = [[False] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            indirect_dominance[i][j] = direct_dominance[i][j]
        indirect_dominance[i][i] = True

    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(n):
                if indirect_dominance[i][j]:
                    for k in range(n):
                        if indirect_dominance[j][k] and not indirect_dominance[i][k]:
                            indirect_dominance[i][k] = True
                            changed = True

    # 4. Матрица предшествования
    precedence = [[False] * n for _ in range(n)]

    def dfs_order(node, visited=None, order=None):
        if visited is None:
            visited = set()
        if order is None:
            order = []

        if node not in visited:
            visited.add(node)
            order.append(node)

            children = []
            for start, end in edges:
                if start == node:
                    children.append(end)
            for child in sorted(children, key=lambda x: int(x)):
                dfs_order(child, visited, order)
        return order

    traversal_order = dfs_order(e)

    for i in range(len(traversal_order)):
        for j in range(i + 1, len(traversal_order)):
            precedence[node_index[traversal_order[i]]][node_index[traversal_order[j]]] = True

    # 5. Матрица следования
    following = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            following[i][j] = precedence[j][i]

    return (
        parent_child,
        direct_dominance,
        indirect_dominance, 
        precedence,
        following
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('csv_path')
    parser.add_argument('root', type=str)

    args = parser.parse_args()

    with open(args.csv_path, "r") as f:
        input_str = f.read()

    result = main(input_str, args.root)

    nodes = set()
    lines = input_str.strip().split('\n')
    for line in lines:
        if line:
            parts = line.split(',')
            if len(parts) == 2:
                nodes.add(parts[0].strip())
                nodes.add(parts[1].strip())

    nodes = sorted(nodes, key=lambda x: int(x))

    relations = [
        "Родитель-потомок",
        "Прямое доминирование", 
        "Непрямое доминирование",
        "Предшествование",
        "Следование"
    ]

    for i, (name, matrix) in enumerate(zip(relations, result)):
        print(f"\n{name}:")
        print("   " + "  ".join(nodes))
        for j, row in enumerate(matrix):
            print(f"{nodes[j]} " + "  ".join("1" if val else "0" for val in row)) 