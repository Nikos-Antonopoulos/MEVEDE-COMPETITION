from Solver import *
from VRP_Model import *
import pprint,random
from SolutionDrawer import *

m = Model()
m.BuildModel()
s=Solver(m)
s.solve()

class Solution:
    def __init__(self): #sider
        self.max_cost_of_route = 0.0
        self.routes = []




class Solver:
    def solve(self, with_sort = False): # with sort variable defines if the minimum_insertions_with_opened_routes will
                                        # sort the self.customers
        print("hi")
        self.paper_structure_method(with_sort)
        self.ReportSolution(self.sol)
        SolDrawer.draw(0, self.sol, self.allNodes)
        return self.sol
        
    def __init__(self, m):
        self.allNodes = m.all_nodes
        self.customers = m.service_locations
        self.depot = m.all_nodes[0]
        self.time_matrix = m.time_matrix
        self.capacity = m.capacity
        self.sol = None
        self.bestSolution = None

    def paper_structure_method(self,with_sort):#NikosA
        print("hio")
        Unserved_locations=self.customers.copy() #All the customers that havent been served
        routes=[None]*25 #Array that has 25 objects of Route type
        depot = Node(0, 0, 0, 50, 50)        
        self.sol = Solution()
        
        for i in range(25):
            routes[i]=Route(depot,3000)#initializing every route so that it begins and ends  to the depot
            self.sol.routes.append(routes[i])    
        if with_sort: # if sort is needed, self.customers get sorted
            self.customers.sort(key=Node.distance_from_depot)

        print(self.customers)
        while(Unserved_locations):
            for i in range(0, len(self.customers)):
                print(i)
                node_to_be_inserted:Node = self.customers[i] #komvos gia eisagwgh
                best_insertion = CustomerInsertionAllPositions()
                self.find_best_insertion(node_to_be_inserted,best_insertion)

                if best_insertion.customer is not None:
                    
                    if(len(best_insertion.potential_candidates_for_insertion)==1):
                        self.ApplyCustomerInsertionAllPositions(best_insertion)
                    
                    elif(len(best_insertion.potential_candidates_for_insertion)>1):
                        best_insertion=random.choice(best_insertion.potential_candidates_for_insertion)
                        self.ApplyCustomerInsertionAllPositions(best_insertion)
                    else:
                        print("there are no potential customers")
                    Unserved_locations.remove(best_insertion.customer)


                    #Remove the node from unserved
                    #Add the node to potential positions
                else: 
                    print("No solution could be found ")
                    break
        self.TestSolution()
    
    def find_best_insertion(self,node_to_be_inserted,best_insertion):
         for j in range(0,len(self.sol.routes)):
            current_route:Route = self.sol.routes[j] #route pou tha bei o komvos 
            if(node_to_be_inserted.demand + current_route.load<=current_route.capacity):
                for k in range (0,len(current_route.sequenceOfNodes)-1): #thesh pou tha bei o komvos 

                    A:Node = current_route.sequenceOfNodes[k]#node_after_which_the_new_node_can_be_inserted
                    B:Node = current_route.sequenceOfNodes[k+1]#node_before_which_the_new_node_can_be_inserted

                    costAdded= self.time_matrix[B.ID][node_to_be_inserted.ID] 
                    + self.time_matrix[node_to_be_inserted.ID][A.ID]
                   
                    costRemoved= self.time_matrix[A.ID][B.ID]
                    
                    trial_cost = costAdded-costRemoved
                    trial_objective_change= current_route.cost + trial_cost - self.sol.max_cost_of_route
                    #kata poso h allagh auksanei to kostos thn antikeimenikh 

                if(trial_objective_change < best_insertion.objective_change):
                    best_insertion.customer = node_to_be_inserted
                    best_insertion.route = current_route
                    best_insertion.cost = trial_cost
                    best_insertion.insertionPosition = k  # the position after which the bestInsertion.customer will be inserted
                    best_insertion.objective_change = trial_objective_change
                    best_insertion.potential_candidates_for_insertion.clear()
                    best_insertion.potential_candidates_for_insertion.append(best_insertion)
                    # AUTO TO SHMEIO PREPEI NA ALLAKSEI GIATI DEN YPOLOGIZW TO TRIAL LENGTH SOLUTION KAI TO BEST_ISNERTION.SOLUTION_LENGTH AKOMA 
                elif( (trial_objective_change==best_insertion.objective_change) and trial_cost < best_insertion.cost):
                    best_insertion.customer = node_to_be_inserted
                    best_insertion.route = current_route
                    best_insertion.cost = trial_cost
                    best_insertion.insertionPosition = k  # the position after which the bestInsertion.customer will be inserted
                    best_insertion.objective_change = trial_objective_change
                    best_insertion.potential_candidates_for_insertion.append(best_insertion)                    
    
    def ApplyCustomerInsertionAllPositions(self,insertion): #sider
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

    def TestSolution(self):  # sider
        if len(self.sol.routes) > 25:  # if the solution used more routes than the routes available
            print("Routes' number problem.")
        max_cost_of_route = 0
        nodes_serviced = 0
        for r in range(0, len(self.sol.routes)):
            rt: Route = self.sol.routes[r]
            nodes_serviced += len(rt.sequenceOfNodes) - 2 # -2 because we remove depot that exist twice in every route
            rt_cost = 0
            rt_load = 0
            for n in range(0, len(rt.sequenceOfNodes) - 1):
                A = rt.sequenceOfNodes[n]
                B = rt.sequenceOfNodes[n + 1]
                rt_cost += self.time_matrix[A.ID][B.ID]
                rt_load += A.demand
            if abs(rt_cost - rt.cost) > 0.0001:
                print('Route Cost problem')
            if rt_load != rt.load:
                print('Route Load problem')
            if rt_cost > max_cost_of_route:
                max_cost_of_route = rt_cost
        if abs(max_cost_of_route - self.sol.max_cost_of_route) > 0.0001:
            print('Solution Cost problem, solution cost: ' + str(self.sol.max_cost_of_route) +
                  ' calculated cost: ' + str(self.CalculateMaxCostOfRoute()))
        if nodes_serviced != len(self.customers):
            print('Number of serviced nodes problem')
    
    def CalculateMaxCostOfRoute(self):  # sider
        # returns the max cost of the routes in the current solution
        return max(route.cost for route in self.sol.routes)
   
    def ReportSolution(self, sol):
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            for j in range (0, len(rt.sequenceOfNodes)):
                print(rt.sequenceOfNodes[j].ID, end=' ')
            print(rt.cost)
        print (self.sol.max_cost_of_route )
    
class CustomerInsertionAllPositions(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.insertionPosition = None
        self.cost = 10 ** 9
        self.objective_change = 10 ** 9 
        self.solution_length = -10
        self.potential_candidates_for_insertion=[]


def ReportSolution(self, sol):
    for i in range(0, len(sol.routes)):
        rt = sol.routes[i]
        for j in range (0, len(rt.sequenceOfNodes)):
            print(rt.sequenceOfNodes[j].ID, end=' ')
        print(rt.cost)
    print (self.sol.max_cost_of_route )

