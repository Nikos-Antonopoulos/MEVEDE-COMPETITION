# from VRP_Model import *
# from VRPMinimumInsertions import *
# from SolutionDrawer import *
# from Swaps import *
# from Relocations import *
import random, pprint, math


class Model:
    def __init__(self):  # markou, sider
        self.all_nodes = []  # All the nodes that are included in the model plus the depot
        self.service_locations = []  # All the locations that have to be served
        self.time_matrix = []  # Time Matrix created from the distance matrix and the node type.
        self.capacity = 3000  # Capacity of the Vehicles measured in kg (3tn).
        self.unloading_time_per_type = {  # the time that each type of node needs to unload
            0: 0,
            1: 5,
            2: 15,
            3: 25
        }
        all_nodes = []
        service_locations = []
        depot = Node(0, 0, 0, 50, 50)
        all_nodes.append(depot)
        random.seed(1)
        for i in range(0, 200):
            id = i + 1
            tp = random.randint(1, 3)
            dem = random.randint(1, 5) * 100
            xx = random.randint(0, 100)
            yy = random.randint(0, 100)
            serv_node = Node(id, tp, dem, xx, yy)
            all_nodes.append(serv_node)
            service_locations.append(serv_node)

        dist_matrix = [[0.0 for j in range(0, len(all_nodes))] for k in range(0, len(all_nodes))]
        for i in range(0, len(all_nodes)):
            for j in range(0, len(all_nodes)):
                source = all_nodes[i]
                target = all_nodes[j]
                dx_2 = (source.x - target.x) ** 2
                dy_2 = (source.y - target.y) ** 2
                dist = round(math.sqrt(dx_2 + dy_2))
                dist_matrix[i][j] = dist
        self.dist_matrix = dist_matrix
        self.all_nodes = all_nodes

    #4.247619047619047
    routes = [[0, 108, 121, 89, 128, 61, 175, 29],
              [0, 19, 140, 193, 143, 173, 13, 11],
              [0, 99, 31, 3, 71, 156, 56, 148, 181, 78, 107],
              [0, 14, 64, 153, 116, 146, 27, 194, 60, 161],
              [0, 59, 9, 77, 184, 81, 132],
              [0, 110, 74, 154, 139, 106, 117, 141, 69, 168],
              [0, 144, 176, 96, 80, 47, 97, 122, 102],
              [0, 40, 187, 150, 6, 145, 198, 124],
              [0, 134, 21, 22, 155, 5, 84, 39, 197],
              [0, 183, 114, 88, 86, 38, 136, 4, 72, 192],
              [0, 162, 58, 50, 185, 92, 119, 152, 76],
              [0, 125, 171, 83, 101, 52, 42, 54],
              [0, 36, 191, 200, 32, 112, 103, 129, 67],
              [0, 37, 133, 49, 195, 2, 189, 87, 33],
              [0, 75, 188, 28, 149, 34, 142, 66, 53],
              [0, 180, 130, 18, 63, 172, 45, 170, 167, 115],
              [0, 91, 12, 46, 95, 23, 44, 68, 199],
              [0, 25, 100, 90, 109, 138, 169, 137, 196],
              [0, 51, 135, 73, 20, 82, 57, 70, 41, 147],
              [0, 127, 177, 85, 164, 43, 131, 55, 111],
              [0, 17, 157, 30, 113, 7, 105, 62],
              [0, 104, 186, 151, 163, 166, 35, 26],
              [0, 118, 165, 182, 179, 123, 65, 94, 120, 8],
              [0, 174, 159, 15, 48, 16, 24, 93],
              [0, 178, 126, 98, 190, 160, 1, 158, 79, 10]]

    def CalculateMaxSolutionCost(self):  # calculates manually the max cost of a given solution

        routes_times = []  # here we store the cost of each route in terms of time

        for i in range(0, len(self.routes)):

            total_route_distance = 0  # here we store the distance of each route
            total_route_time = 0
            for j in range(0, len(self.routes[i]) - 1):
                total_route_distance = self.dist_matrix[self.routes[i][j]][
                    self.routes[i][j + 1]]  # here we calculate the distance of each route manually

                total_route_time_without_unload = total_route_distance / 35  # converting distance to time

                unload_time = self.unloading_time_per_type[self.all_nodes[self.routes[i][j + 1]].type]/60

                total_route_time += total_route_time_without_unload + unload_time  # adding the unload cost using the type of each node
            print(total_route_time)
            routes_times.append(
                total_route_time)  # storing the manually calculated time of every route of the given solution

        return max(routes_times)  # return the max time (cost) of the solution


class Node:
    def __init__(self, id, tp, dem, xx, yy):
        self.id = id
        self.type = tp
        self.demand = dem
        self.x = xx
        self.y = yy





model = Model()
print(model.CalculateMaxSolutionCost())
