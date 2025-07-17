import heapq
import math
import networkx as nx
from itertools import combinations

class Graph:
    def __init__(self):
        self.edges = {}  # adjacency list
        self.hospitals = {}  # positions of hospitals

    def add_edge(self, node1, node2, weight):
        if node1 not in self.edges:
            self.edges[node1] = []
        if node2 not in self.edges:
            self.edges[node2] = []
        self.edges[node1].append((node2, weight))
        self.edges[node2].append((node1, weight))

    def add_hospital(self, hospital, position):
        self.hospitals[hospital] = position

    def heuristic(self, node, goal):
        """Euclidean distance as the heuristic."""
        x1, y1 = self.hospitals[node]
        x2, y2 = self.hospitals[goal]
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def a_star(self, start, goal):
        """A* search algorithm."""
        pq = []  # Priority queue
        heapq.heappush(pq, (0, start))
        came_from = {}
        cost_so_far = {start: 0}

        while pq:
            _, current = heapq.heappop(pq)

            if current == goal:
                # Reconstruct the path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1], cost_so_far[goal]

            for neighbor, weight in self.edges.get(current, []):
                new_cost = cost_so_far[current] + weight
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, goal)
                    heapq.heappush(pq, (priority, neighbor))
                    came_from[neighbor] = current

        return None, float('inf')  # No path found

# Setup graph with hospitals and edges
def setup_hospitals():
    graph = Graph()
    hospital_positions = {
        "RSUD Bhakti Dharma Husada": (1, 11),
        "National Hospital Surabaya": (5, 7),
        "RSIA Cempaka Putih Permata": (7, 4),
        "RSIA Kendangsari Surabaya": (11, 4),
        "Rumah Sakit Islam Surabaya Jemursari": (10, 4),
        "RS Bhayangkara Surabaya H.S Samsoeri Mertojoso": (9, 4),
        "RSU. Bhakti Rahayu Surabaya": (8, 5),
        "RSPAL dr RAMELAN SURABAYA": (11, 5),
        "RS UBAYA": (14, 5),
        "Rumah Sakit Islam Surabaya": (10, 5.5),
        "Mayapada Hospital Surabaya (MHSB)": (9, 6),
        "Rumah Sakit Katolik St. Vincentius a Paulo": (10, 6.5),
        "Rumah Sakit William Booth Surabaya": (10.5, 6.5),
        "Rumah Sakit Darmo": (11, 7),
        "Rumah Sakit Umum Siloam Surabaya": (12, 8),
        "RSUD Dr. Soetomo": (13, 9),
        "RS Husada Utama": (12.5, 9.5),
        "Rumah Sakit Adi Husada Undaan": (11.5, 10.5),
        "Rumah Sakit PHC Surabaya": (11.5, 15),
        "Mitra Keluarga": (6, 10)
    }

    for hospital, position in hospital_positions.items():
        graph.add_hospital(hospital, position)

    for node1, node2 in combinations(hospital_positions.keys(), 2):
        x1, y1 = hospital_positions[node1]
        x2, y2 = hospital_positions[node2]
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        graph.add_edge(node1, node2, distance)

    return graph
