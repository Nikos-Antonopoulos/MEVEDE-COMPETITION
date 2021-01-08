from VRP_Model import *
from SolutionDrawer import *

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
        self.subjective_cost = 10 ** 9 # subjective cost is the cost of an insertion that considers the effect on the
                                       # min max cost of the solution too

class Solver:
    def __init__(self, m, siders_constant):
        self.allNodes = m.all_nodes
        self.customers = m.service_locations
        self.depot = m.all_nodes[0]
        self.time_matrix = m.time_matrix
        self.capacity = m.capacity
        self.sol = None
        self.bestSolution = None
        self.searchTrajectory = []
        self.siders_constant = siders_constant # it is a constant that defines how strong the effect of the change
                                               # an insertion causes on the min max solution relatively to the
                                               # trialCost of the insertion (the cost on the route)

    def solve(self, with_sort = False): # with sort variable defines if the minimum_insertions_with_opened_routes will
                                        # sort the self.customers
        self.SetRoutedFlagToFalseForAllCustomers()
     #   self.ApplyNearestNeighborMethod()
        self.minimum_insertions_with_opened_routes(with_sort)
        # self.ReportSolution(self.sol)
        # self.VND()
        SolDrawer.draw(0, self.sol, self.allNodes)
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

    def TestSolution(self):  # sider # NEEDS TO BE OPTIMIZED
        if len(self.sol.routes) > 25:  # if the solution used more routes than the routes available
            print("Routes' number problem.")
        for r in range(0, len(self.sol.routes)):
            rt: Route = self.sol.routes[r]
            rtCost = 0
            rtLoad = 0
            for n in range(0, len(rt.sequenceOfNodes) - 1):
                A = rt.sequenceOfNodes[n]
                B = rt.sequenceOfNodes[n + 1]
                rtCost += self.time_matrix[A.ID][B.ID]
                rtLoad += A.demand
            if abs(rtCost - rt.cost) > 0.0001:
                print('Route Cost problem')
            if rtLoad != rt.load:
                print('Route Load problem')
        max_cost_of_route = max(
            sum(
                self.time_matrix[self.sol.routes[i].sequenceOfNodes[j].ID][self.sol.routes[i].sequenceOfNodes[j + 1].ID]
                for j in range(len(self.sol.routes[i].sequenceOfNodes) - 1)
            ) for i in range(len(self.sol.routes))
        )
        if abs(max_cost_of_route - self.sol.max_cost_of_route) > 0.0001:
            print('Solution Cost problem, solution cost: ' + str(self.sol.max_cost_of_route) +
                  ' calculated cost: ' + str(self.CalculateMaxCostOfRoute()))

    def SetRoutedFlagToFalseForAllCustomers(self):
        for i in range(0, len(self.customers)):
            self.customers[i].isRouted = False


    def minimum_insertions_with_opened_routes(self, with_sort): # sider
        self.sol = Solution()
        insertions = 0
        self.open_routes(25)
        if with_sort:
            self.customers.sort(key=Node.distance_from_depot)

        while insertions < len(self.customers): # while there are customers that are not inserted
            best_insertion = CustomerInsertionAllPositions()
            self.identify_best_insertion_in_all_routes(best_insertion)

            if best_insertion.customer is not None:
                self.ApplyCustomerInsertionAllPositions(best_insertion)  # insertion gets added to self.sol
                insertions += 1

            else:
                print("No solution could be found.")
                break;
        self.TestSolution()

    def open_routes(self, number_of_routes):
        for i in range(number_of_routes):
            rt = Route(self.depot, self.capacity)  # a new route gets opened
            self.sol.routes.append(rt)  # the new route gets added to the solution

    def identify_best_insertion_in_all_routes(self, best_insertion):
        for i in range(len(self.customers)):
            candidate_cust: Node = self.customers[i]
            if candidate_cust.isRouted is False:
                best_insertion_for_customer = CustomerInsertionAllPositions()
                self.find_best_insertion_for_customer(candidate_cust, best_insertion_for_customer)
                if best_insertion_for_customer.subjective_cost < best_insertion.subjective_cost:
                    # the fields of bestInsertion will be updated according to the new best insertion found
                    best_insertion.customer = best_insertion_for_customer.customer
                    best_insertion.route = best_insertion_for_customer.route
                    best_insertion.cost = best_insertion_for_customer.cost
                    best_insertion.insertionPosition = best_insertion_for_customer.insertionPosition
                    best_insertion.subjective_cost = best_insertion_for_customer.subjective_cost


    def find_best_insertion_for_customer(self, candidate_cust, best_insertion_for_customer):
        for route in self.sol.routes:
            if route.load + candidate_cust.demand <= route.capacity:
                for i in range(0, len(route.sequenceOfNodes) - 1):  # j is the index of a node in rt(parameter).sequenceOfNodes
                                                                 # it will be checked if the insertion of candidateCust between
                                                                 # rt.sequenceOfNodes[j] and rt.sequenceOfNodes[j+1] costs less
                                                                 # than the current best insertion
                    A = route.sequenceOfNodes[i]
                    B = route.sequenceOfNodes[i + 1]
                    costAdded = self.time_matrix[A.ID][candidate_cust.ID] + self.time_matrix[candidate_cust.ID][
                        B.ID]  # the costs of the 2 new connections created
                    costRemoved = self.time_matrix[A.ID][
                        B.ID]  # the cost of the connection that broke (it will be reduced from the trialCost)
                    trialCost = costAdded - costRemoved  # how the cost changed after the insertion

                    subjective_cost_of_insertion = trialCost
                    if route.cost + trialCost > self.sol.max_cost_of_route:
                        subjective_cost_of_insertion += self.siders_constant*(route.cost + trialCost - self.sol.max_cost_of_route)



                    if  subjective_cost_of_insertion < best_insertion_for_customer.subjective_cost:  # bestInsertion.cost is initialized to 10 ** 9
                         # the fields of bestInsertion will be updated according to the new best insertion found
                         best_insertion_for_customer.customer = candidate_cust
                         best_insertion_for_customer.route = route
                         best_insertion_for_customer.cost = trialCost
                         best_insertion_for_customer.insertionPosition = i  # the position after which the bestInsertion.customer will be inserted
                         best_insertion_for_customer.subjective_cost = subjective_cost_of_insertion

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
