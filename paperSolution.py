from Solver import *
from VRP_Model import *
import pprint
m = Model()
m.BuildModel()
#print(m.service_locations)







Unserved_locations=m.service_locations #All the customers that havent been served
routes=[None]*25 #Array that has 25 objects of Route type
depot = Node(0, 0, 0, 50, 50)
solution=[]


for i in range(25):
    routes[i]=Route(depot,3000)#initializing every route so that it begins and ends  to the depot
    solution.append(routes[i])    


potential_candidates_for_insertion=[]
currently_best_quality = 10**5



for node_to_be_inserted in Unserved_locations: #unserved location is an object of node class 
    for current_route in routes:#current route is an object of route class 
        for node_after_which_the_new_node_can_be_inserted in current_route.sequenceOfNodes[:-1]:
            print(node_after_which_the_new_node_can_be_inserted)
