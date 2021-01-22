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
    routes = [[0,19,31,108,3,71,156,121,89],
              [0,118,113,30,182,165,95,23,44],
              [0,91,110,144,74,46,7,105,62,199,68],
              [0,162,58,50,35,26,4,136,72,192],
              [0,66,127,179,123,65,94,120,8],
              [0,135,104,73,186,151,114,171,52,54],
              [0,172,176,106,117,141,69,168],
              [0,17,21,189,33,87,184],
              [0,20,109,41,190,76,160,1,158,79,10],
              [0,174,59,9,77,150,6,81,132],
              [0,157,187,159,145,198,124],
              [0,180,75,188,28,34,149,142],
              [0,36,27,194,60,161,129,67],
              [0,12,80,47,97,42,122,102],
              [0,140,143,173,191,200,32,112,103],
              [0,53,15,48,16,24,93,111],
              [0,126,147,98,175,29,61,128],
              [0,193,56,78,107,181,148,13,11],
              [0,99,82,185,92,119,137,169,196],
              [0,153,116,146,22,155,5,84,39,197],
              [0,183,125,63,18,115,167,170,45,96,154,139],
              [0,51,163,166,88,83,101,86,38],
              [0,37,134,133,14,64,40,49,195,2],
              [0,25,178,100,57,90,70,138,152],
              [0,130,177,85,164,43,131,55]]

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
            # print(total_route_time)
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
