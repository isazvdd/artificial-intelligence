import os
import re
import math


class Graph:
    def __init__(self, nodes=[], edges=[]):
        self.nodes = nodes
        self.edges = edges
        self.infos = {}
        self.adjacency = {}
        self.distances = {}

    def add_node(self, node, info=""):
        if node not in self.nodes:
            self.nodes.append(node)
        if len(info) > 0:
            self.infos[node] = info

    def add_edge(self, edge, info=""):
        (a, b) = edge
        self.add_node(a)
        self.add_node(b)

        if edge not in self.edges:
            self.edges.append(edge)
        if len(info) > 0:
            self.infos[edge] = info

    def create_adjacency(self):
        self.adjacency = {}

        for node in self.nodes:
            self.adjacency[node] = {}

        for a, b, weight in self.edges:
            if weight.isdigit():
                self.adjacency[a][b] = int(weight)
                self.adjacency[b][a] = int(weight)
            else:
                self.adjacency[a][b] = 0
                self.adjacency[b][a] = 0

    def heuristic(self, node_a, node_b):
        pattern = r"^\(([0-9]+),([0-9]+)\)$"
        node_a = int(node_a)
        if node_a in self.infos:
            info = self.infos[node_a]
        else:
            raise KeyError(f"Nó {node_a} não possui informações.")
        ans = re.fullmatch(pattern, info)
        x1, y1 = [int(i) for i in ans.groups()]
        node_b = int(node_b)
        if node_b in self.infos:
            info = self.infos[node_b]
        else:
            raise KeyError(f"Nó {node_b} não possui informações.")
        ans = re.fullmatch(pattern, info)
        x2, y2 = [int(i) for i in ans.groups()]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def remove_nearest(self, memory, goal):
        return memory.pop(0)

    def insert_ordered(self, memory, node, goal):
        if node not in memory:
            self.distances[node] = self.heuristic(node, goal)
            memory.insert(0, node)
            for i in range(1, len(memory)):
                if self.distances[memory[i]] < self.distances[node]:
                    memory[i - 1], memory[i] = memory[i], memory[i - 1]
                else:
                    return True
            return True
        return False

    def dfs(self, start, goal):
        visited = {}
        origin = {}
        for node in self.nodes:
            visited[node] = False
            origin[node] = None
        origin[start] = start

        stack = [start]
        while stack:
            node_a = stack.pop()
            if not visited[node_a]:
                visited[node_a] = True
                for node_b in self.adjacency[node_a]:
                    if not visited[node_b]:
                        stack.append(node_b)
                        origin[node_b] = node_a
                    if node_b == goal:
                        return origin

        return origin

    def bfs(self, start, goal):
        visited = {}
        origin = {}
        for node in self.nodes:
            visited[node] = False
            origin[node] = None
        origin[start] = start

        queue = [start]
        while queue:
            node_a = queue.pop(0)
            if not visited[node_a]:
                visited[node_a] = True
                for node_b in self.adjacency[node_a]:
                    if not visited[node_b]:
                        queue.append(node_b)
                        origin[node_b] = node_a
                    if node_b == goal:
                        return origin

        return origin

    def astar(self, start, goal):
        f_scores = {}
        g_scores = {}
        came_from = {}

        for node in self.nodes:
            f_scores[node] = float('inf')
            g_scores[node] = float('inf')
            came_from[node] = None

        f_scores[start] = self.heuristic(start, goal)
        g_scores[start] = 0

        open_set = [start]

        while open_set:
            current = self.remove_nearest(open_set, goal)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.adjacency[current]:
                tentative_g_score = g_scores[current] + 1

                if tentative_g_score < g_scores[neighbor]:
                    came_from[neighbor] = current
                    g_scores[neighbor] = tentative_g_score
                    f_scores[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    self.insert_ordered(open_set, neighbor, goal)

        return None

    def reconstruct_path(self, came_from, current):
        path = []
        while current is not None:
            path.insert(0, current)
            current = came_from[current]
        return path


def read_tgf(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    nodes = {}
    edges = []

    for line in lines:
        line = line.strip()
        if line == "#":
            break
        node_id, node_label = line.split()
        nodes[node_id] = node_label

    for line in lines[len(nodes) + 2:]:
        line = line.strip()
        if line == "#":
            continue
        node_a, node_b, weight = line.split()
        edges.append((node_a, node_b, weight))

    return Graph(nodes, edges)


def main():
    filename = "complete.tgf"
    complete_graph_tgf = read_tgf(filename)

    start_node = "1"
    goal_node = "4"

    if start_node not in complete_graph_tgf.nodes:
        print(f"Nó inicial {start_node} não está presente no grafo.")
        return

    if goal_node not in complete_graph_tgf.nodes:
        print(f"Nó objetivo {goal_node} não está presente no grafo.")
        return

    complete_graph_tgf.create_adjacency()

    dfs_solution = complete_graph_tgf.dfs(start_node, goal_node)
    dfs_path = get_path(dfs_solution, start_node, goal_node)
    print("Solução utilizando DFS:")
    print(dfs_path)

    bfs_solution = complete_graph_tgf.bfs(start_node, goal_node)
    bfs_path = get_path(bfs_solution, start_node, goal_node)
    print("Solução utilizando BFS:")
    print(bfs_path)

    astar_solution = complete_graph_tgf.astar(start_node, goal_node)
    if astar_solution:
        astar_path = get_path(astar_solution, start_node, goal_node)
        print("Solução utilizando A*:")
        print(astar_path)
    else:
        print("Não foi possível encontrar uma solução utilizando A*.")


def get_path(solution, start, goal):
    path = []
    current = goal

    while current != start:
        path.insert(0, current)
        current = solution[current]

    path.insert(0, start)
    return path


if __name__ == "__main__":
    main()
