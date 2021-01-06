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
    
    def load_objects(self):
        routes = [[0,1,50,65,101,130,150,165,183],
                    [0,2,46,74,77,96,120,146,179],
                    [0,3,34,72,104,123,145,162,194 ],
                    [0,4,40,80,103,138,163,175,198 ],
                    [0,5,49,59,70,98,106,140,166,195],
                    [0,6,36,62,91,107,131,178],
                    [0,7,33,73,99,105,126,153,169 ],
                    [0,8,47,78,115,143,167,193],
                    [0,9,39,61,90,100,108,119,133,159,177,187],
                    [0,10,51,75,85,102,127,154,173],
                    [0,11,48,82,111,142,156,184],
                    [0,12,30,41,69,93,125,151,164],
                    [0,13,38,79,94,141,158,196,199],
                    [0,14,29,60,88,117,135,155,180,200],
                    [0,15,43,57,95,124,148,181,189],
                    [0,16,52,87,122,160,192],
                    [0,17,27,44,76,112,137,171,188],
                    [0,18,31,56,64,86,116,149,174,185],
                    [0,19,28,55,71,110,129,168],
                    [0,20,32,58,84,114,147,170,191],
                    [0,21,37,53,67,97,144,161,197],
                    [0,22,35,81,118,136,157,190],
                    [0,23,42,68,89,128,139,176,186],
                    [0,24,54,92,113,134,152,182],
                    [0,25,26,45,63,66,83,109,121,132,172 ]]
        return routes
                    
    
    def CalculateMaxCostOfRoute(self,routes,time_matrix):#asking for model to get the matrix
        print(time_matrix[1][200])

        max_cost_of_routes = 0
        for i in range (0, len(routes)):#for every route in the specific solution
            list_i = routes[i] 
            cost_of_current_route = 0
            for j in range (0, len(list_i) -1 ):
                a = list_i[j] 
                b = list_i[j + 1]
                cost_of_current_route += time_matrix[a][b]   
            if(cost_of_current_route > max_cost_of_routes):
                max_cost_of_routes=cost_of_current_route
        return max_cost_of_routes

class Node:
    def __init__(self, id, tp, dem, xx, yy):
        self.ID = id
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

