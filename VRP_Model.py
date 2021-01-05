import random
import math


class Model:

    def __init__(self):
        self.all_nodes = []  # All the nodes that are included in the model plus the depot
        self.service_locations = []  # All the locations that have to be served
        self.time_matrix = []  # Time Matrix created from the distance matrix and the node type.
        self.capacity = 3000  # Capacity of the Vehicles measured in kg (3tn).

    def BuildModel(self):
        depot = Node(0, 0, 0, 50, 50)
        self.all_nodes.append(depot)
        random.seed(1)
        number_of_service_points = 200

        for i in range(0, number_of_service_points):  # Creation of the service locations
            id = i + 1
            tp = random.randint(1, 3)
            dem = random.randint(1, 5) * 100
            xx = random.randint(0, 100)
            yy = random.randint(0, 100)
            serv_node = Node(id, tp, dem, xx, yy)
            self.all_nodes.append(serv_node)
            self.service_locations.append(serv_node)

        dist_matrix = [[0.0 for j in range(0, len(self.all_nodes))] for k in range(0, len(self.all_nodes))]  
        for i in range(0, len(self.all_nodes)):  # Creation of the distance matrix
            for j in range(0, len(self.all_nodes)):
                source = self.all_nodes[i]
                target = self.all_nodes[j]
                dx_2 = (source.x - target.x) ** 2
                dy_2 = (source.y - target.y) ** 2
                dist = round(math.sqrt(dx_2 + dy_2))
                dist_matrix[i][j] = dist

        for i in range(len(dist_matrix)):  # Creation of the time_matrix
            self.time_matrix.append([])
            for j in range(len(dist_matrix[i])):
                if i == j:
                    self.time_matrix[i].append(0.0)
                elif self.all_nodes[j].type == 1:
                    self.time_matrix[i].append(dist_matrix[i][j] / 35 * 60 + 5)
                elif self.all_nodes[j].type == 2:
                    self.time_matrix[i].append(dist_matrix[i][j] / 35 * 60 + 15)
                elif self.all_nodes[j].type == 3:
                    self.time_matrix[i].append(dist_matrix[i][j] / 35 * 60 + 25)
                else:
                    self.time_matrix[i].append(dist_matrix[i][j] / 35 * 60)


class Node:
    def __init__(self, id, tp, dem, xx, yy):
        self.id = id
        self.type = tp  # The node can be type 1 (5 min) type 2 (15 min) type 3 (25min)
        self.demand = dem
        self.x = xx
        self.y = yy


class Route:
    def __init__(self, dp, cap):  # One route, a node that's the depot, and the capacity
        self.sequenceOfNodes = []
        self.sequenceOfNodes.append(dp)
        self.cost = 0
        self.capacity = cap
        self.load = 0
