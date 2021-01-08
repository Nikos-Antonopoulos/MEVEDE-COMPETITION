from Solver import *
from VRP_Model import *
import pprint,random
m = Model()
m.BuildModel()
#print(m.service_locations)



def ApplyCustomerInsertionAllPositions(insertion): #sider
    # insertion: type of CustomerInsertionAllPositions
    # the new insetion will be added to the current solution
    insCustomer = insertion.customer
    rt = insertion.route
    # before the second depot occurrence
    insIndex = insertion.insertionPosition
    rt.sequenceOfNodes.insert(insIndex + 1, insCustomer) # insCustomer gets inserted after the rt.sequenceOfNodes[indIndex]
    rt.cost += insertion.cost # route's cost gets updated
 #   if rt.cost > self.sol.max_cost_of_route: # if the new cost of the route is bigger than the max_cost_of_route of the solution,
                                                # self.sol.max_cost_of_route gets updated to the rt.cost
   #     self.sol.max_cost_of_route = rt.cost
    rt.load += insCustomer.demand # route's cost gets updated
    insCustomer.isRouted = True # inserted customer marked as routed






Unserved_locations=m.service_locations #All the customers that havent been served
routes=[None]*25 #Array that has 25 objects of Route type
depot = Node(0, 0, 0, 50, 50)
solution=[]


for i in range(25):
    routes[i]=Route(depot,3000)#initializing every route so that it begins and ends  to the depot
    solution.append(routes[i])    



while(Unserved_locations):
    potential_candidates_for_insertion=[]
    currently_best_quality = 10**5

    for i in range(0, len(Unserved_locations)):
        node_to_be_inserted:Node = Unserved_locations[i] #komvos gia eisagwgh
        for j in range(0,len(routes)):
            current_route:Route = routes[j] #route pou tha bei o komvos 
            if(node_to_be_inserted.demand + current_route.load<=current_route.capacity):
                for k in range (0,len(current_route.sequenceOfNodes)-1): #thesh pou tha bei o komvos 

                    node_after_which_the_new_node_can_be_inserted:Node = current_route.sequenceOfNodes[k]
                    node_before_which_the_new_node_can_be_inserted:Node = current_route.sequenceOfNodes[k+1]

                    costAdded= m.time_matrix[node_before_which_the_new_node_can_be_inserted.ID][node_to_be_inserted.ID] 
                    + m.time_matrix[node_to_be_inserted.ID][node_after_which_the_new_node_can_be_inserted.ID]
                    costRemoved= m.time_matrix[node_after_which_the_new_node_can_be_inserted][node_before_which_the_new_node_can_be_inserted]
                   
                    bestInsertion = CustomerInsertionAllPositions()
                    bestInsertion.customer=node_to_be_inserted
                    bestInsertion.route=current_route
                    bestInsertion.cost=costAdded
                    bestInsertion.insertionPosition=k

                    
                    if(F(solution)<currently_best_quality):
                        potential_candidates_for_insertion.clear()

                        potential_candidates_for_insertion.append(node_to_be_inserted,node_after_which_the_new_node_can_be_inserted)
                        currently_best_quality = F(solution)
                    elif(F(solution)==currently_best_quality):
                        potential_candidates_for_insertion.append(node_to_be_inserted,node_after_which_the_new_node_can_be_inserted)
        (p,q)=random.choice(potential_candidates_for_insertion)
        addtoSolution(pq)
        ApplyCustomerInsertionAllPositions(bestInsertion)

        Unserved_locations.remove(p)

