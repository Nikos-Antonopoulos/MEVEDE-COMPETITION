import random,math
import numpy as np 
import matplotlib.pyplot as plt

class Node:
    def __init__(self, id, tp, dem, xx, yy):
        self.id = id
        self.type = tp
        self.demand = dem
        self.x = xx
        self.y = yy
all_nodes = []
service_locations = []
depot = Node(0, 0, 0, 50, 50)
all_nodes.append(depot)
random.seed(1)
plt.scatter(50,50,s=60,alpha=1)
for i in range(0, 200):
    id = i + 1
    tp = random.randint(1,3)
    dem = random.randint(1,5) * 100
    xx = random.randint(0, 100)
    yy = random.randint(0, 100)
    serv_node = Node(id, tp, dem, xx, yy)
    all_nodes.append(serv_node)
    service_locations.append(serv_node)

 # plotting nodes 
    print(xx,yy)
    N = 50
    area=30
    plt.scatter(xx,yy,s=area,alpha=0.5)


plt.gca().set_aspect('equal', adjustable='box')
plt.show()
#end of plotting nodes 
dist_matrix = [[0.0 for j in range(0, len(all_nodes))] for k in range(0, len(all_nodes))]
for i in range(0, len(all_nodes)):
    for j in range(0, len(all_nodes)):
        source = all_nodes[i]
        target = all_nodes[j]
        dx_2 = (source.x - target.x)**2
        dy_2 = (source.y - target.y) ** 2
        dist = round(math.sqrt(dx_2 + dy_2))
        dist_matrix[i][j] = dist 

# 1st way for ultra flexing :
minutes_dist_matrix = [[0.0 if i == j else (dist_matrix[i][j] / 35 * 60 + 5) if all_nodes[j].type == 1 else (dist_matrix[i][j] / 35 * 60 + 15) if all_nodes[j].type == 2 else (dist_matrix[i][j] / 35 * 60 + 25) for j in range(0, len(dist_matrix[i]))] for i in range(0, len(dist_matrix))]

# 2nd way minimalistic :
minutes_dist_matrix = []
for i in range(0, len(dist_matrix)):
    minutes_dist_matrix.append([])
    for j in range(0, len(dist_matrix[i])):
        if i == j:
            minutes_dist_matrix[i].append(0.0)
        elif all_nodes[j].type == 1:
            minutes_dist_matrix[i].append(dist_matrix[i][j] / 35 * 60 + 5)
        elif all_nodes[j].type == 2:
            minutes_dist_matrix[i].append(dist_matrix[i][j] / 35 * 60 + 15)
        else:
            minutes_dist_matrix[i].append(dist_matrix[i][j] / 35 * 60 + 25)
