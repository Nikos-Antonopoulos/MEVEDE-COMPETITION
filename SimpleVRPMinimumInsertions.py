from VRP_Model import *
from SolutionDrawer import *
from Combined import *

class Solution:
    def __init__(self): #sider
        self.max_cost_of_route = 0.0
        self.routes = []

class CustomerInsertionAllPositions(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.insertionPosition = None
        self.cost = 10 ** 9

class SolverSimpleMinIns:
    def __init__(self, m):
        self.allNodes = m.all_nodes
        self.customers = m.service_locations
        self.depot = m.all_nodes[0]
        self.time_matrix = m.time_matrix
        self.capacity = m.capacity
        self.sol = None
        self.bestSolution = None
        self.searchTrajectory = []

    def solve(self, with_sort = False): # with sort variable defines if the minimum_insertions_with_opened_routes will
                                        # sort the self.customers
        self.SetRoutedFlagToFalseForAllCustomers()
        self.minimum_insertions_with_opened_routes(with_sort)
        # self.ReportSolution(self.sol)
        #SolDrawer.draw(0, self.sol, self.allNodes)
        print("start", self.sol.max_cost_of_route)
        combined = Combined(self)
        combined.VND()
        return self.sol

    def ReportSolution(self, sol):
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            for j in range (0, len(rt.sequenceOfNodes)):
                print(rt.sequenceOfNodes[j].ID, end=' ')
            print(rt.cost)
        print (self.sol.max_cost_of_route )

    def CalculateMaxCostOfRoute(self):  # sider
        # returns the max cost of the routes in the current solution
        return max(route.cost for route in self.sol.routes)

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

    def SetRoutedFlagToFalseForAllCustomers(self):
        for i in range(0, len(self.customers)):
            self.customers[i].isRouted = False


    def minimum_insertions_with_opened_routes(self, with_sort): # sider
        self.sol = Solution()
        insertions = 0
        self.open_routes(25) # 25 routes get opened
        if with_sort: # if sort is needed, self.customers get sorted
            self.customers.sort(key=Node.distance_from_depot)

        while insertions < len(self.customers): # while there are customers that are not inserted
            best_insertion = CustomerInsertionAllPositions()
            self.identify_best_insertion_in_all_routes(best_insertion) # the best insertion gets found

            if best_insertion.customer is not None: # if best_insertion was found
                                                    # (which means at least one valid insertion found)
                self.ApplyCustomerInsertionAllPositions(best_insertion)  # insertion gets added to self.sol
                insertions += 1

            else:
                print("No solution could be found.")
                break
        self.TestSolution()

    def open_routes(self, number_of_routes):
        # number_of_routs: an int that show how many routes will be opened
        # open a route --> add an empty route to the routes of the current solution
        for i in range(number_of_routes):
            rt = Route(self.depot, self.capacity)  # a new route gets opened
            self.sol.routes.append(rt)  # the new route gets added to the solution

    def identify_best_insertion_in_all_routes(self, best_insertion):
        for i in range(len(self.customers)): # iterate all customers
            candidate_cust: Node = self.customers[i] # the current checking customer
            if candidate_cust.isRouted is False: # if the customer is not routed
                best_insertion_for_customer = CustomerInsertionAllPositions()
                self.find_best_insertion_for_customer(candidate_cust, best_insertion_for_customer) # finds the best
                                                                                                   # insertion for the
                                                                                                   # particular customer
                if best_insertion_for_customer.cost < best_insertion.cost:
                    # if the best insertion of the checking customer is better than the best insertion at this moment
                    # according to the trial cost
                    best_insertion.customer = best_insertion_for_customer.customer
                    best_insertion.route = best_insertion_for_customer.route
                    best_insertion.cost = best_insertion_for_customer.cost
                    best_insertion.insertionPosition = best_insertion_for_customer.insertionPosition


    def find_best_insertion_for_customer(self, candidate_cust, best_insertion_for_customer):
        for route in self.sol.routes: # iterate all routes
            if route.load + candidate_cust.demand <= route.capacity: # if the route's capacity constraint is not violated
                for i in range(0, len(route.sequenceOfNodes) - 1):  # iterate all the possible position for an insertion
                                                                    # in a route
                    A = route.sequenceOfNodes[i]
                    B = route.sequenceOfNodes[i + 1]
                    cost_added = self.time_matrix[A.ID][candidate_cust.ID] + self.time_matrix[candidate_cust.ID][
                        B.ID]  # the costs of the 2 new connections created
                    cost_removed = self.time_matrix[A.ID][
                        B.ID]  # the cost of the connection that broke (it will be reduced from the trialCost)
                    trial_cost = cost_added - cost_removed  # how the cost changed after the insertion



                    if  trial_cost < best_insertion_for_customer.cost:
                         # if the best insertion of the checking customer is better than the best insertion at this moment
                         # according to the subjective cost (subjective cost is initialized to 10**9)
                         # the fields of bestInsertion will be updated according to the new best insertion found
                         best_insertion_for_customer.customer = candidate_cust
                         best_insertion_for_customer.route = route
                         best_insertion_for_customer.cost = trial_cost
                         best_insertion_for_customer.insertionPosition = i  # the position after which the bestInsertion.customer will be inserted

    def ApplyCustomerInsertionAllPositions(self, insertion): #sider
        # insertion: type of CustomerInsertionAllPositions
        # the new insetion will be added to the current solution
        insCustomer = insertion.customer
        rt = insertion.route
        # before the second depot occurrence
        insIndex = insertion.insertionPosition
        rt.sequenceOfNodes.insert(insIndex + 1, insCustomer) # insCustomer gets inserted after the rt.sequenceOfNodes[indIndex]
        rt.cost += insertion.cost # route's cost gets updated
        if rt.cost > self.sol.max_cost_of_route: # if the new cost of the route is bigger than the max_cost_of_route of the solution,
                                                 # self.sol.max_cost_of_route gets updated to the rt.cost
            self.sol.max_cost_of_route = rt.cost
        rt.load += insCustomer.demand # route's cost gets updated
        insCustomer.isRouted = True # inserted customer marked as routed
