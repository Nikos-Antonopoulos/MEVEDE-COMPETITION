import random
import math
import pprint

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

        self.time_matrix = [[0.0 for j in range(0, len(self.all_nodes))] for k in range(0, len(self.all_nodes))]
        for i in range(0, len(self.all_nodes)):  # Creation of the time matrix /George Markou
            for j in range(0, len(self.all_nodes)):
                source = self.all_nodes[i]
                target = self.all_nodes[j]
                dx_2 = (source.x - target.x) ** 2
                dy_2 = (source.y - target.y) ** 2
                dist = round(math.sqrt(dx_2 + dy_2))
                bonus_time = 0
                if i == j:  # The distance Between the node and itself is 0
                    self.time_matrix[i][j] = 0
                else:
                    # In this section we get the sum of bonus_time from the target and source node
                    if target.type == 1 and source.type == 1:  # Type 1 = 5 so (5+5)/2=5
                        bonus_time = 5
                    elif (target.type == 1 and source.type == 2) or (target.type == 2 and source.type == 1):
                        # Type 1 = 5  and Type 2 = 15 so (15+5)/2=10
                        bonus_time = 10
                    elif target.type == 2 and source.type == 2:
                        bonus_time = 15
                    elif (target.type == 2 and source.type == 3) or (target.type == 3 and source.type == 2):
                        bonus_time = 20
                    elif target.type == 3 and source.type == 3:
                        bonus_time = 25
                    else:
                        # if i==0 or j==0 which means its either going to the depot or moving away from it
                        if target.type == 1:
                            bonus_time = 5/2
                        elif target.type == 2:
                            bonus_time = 15/2
                        elif target.type == 3:
                            bonus_time = 25/2
                        elif source.type == 1:
                            bonus_time = 5/2
                        elif source.type == 2:
                            bonus_time = 15/2
                        elif source.type == 3:
                            bonus_time = 25/2
                    time = dist / 35 * 60 + bonus_time
                    if j == 0:  # If a route is returning to the depot the only extra cost is the bonus_time cost
                        self.time_matrix[i][j] = bonus_time
                    else:
                        self.time_matrix[i][j] = time

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
        self.sequenceOfNodes.append(dp)
        self.cost = 0
        self.capacity = cap
        self.load = 0
