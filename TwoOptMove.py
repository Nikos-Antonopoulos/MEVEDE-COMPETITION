from VRP_Model import *
from VRPMinimumInsertions import *
from SolutionDrawer import *

class Solution:
    def __init__(self): #sider
        self.max_cost_of_route = 0.0
        self.routes = []

class TwoOptMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = None

    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = 10 ** 9


class TwoOptMoveImplication:

    def __init__(self, minIns):
        # m is the model, siders_constant, siders_constant2 (the second is optional) are numbers that define how
        # important is it for an insertion not to increase the min_max cost of the solution
        self.allNodes = minIns.allNodes
        self.customers = minIns.customers
        self.depot = minIns.allNodes[0]
        self.time_matrix = minIns.time_matrix
        self.capacity = minIns.capacity
        self.sol = minIns.sol
        self.bestSolution = None

    def CalculateMaxCostOfRoute(self):  # sider
        # returns the max cost of the routes in the current solution
        # return max(
        #     sum(
        #         self.time_matrix[self.sol.routes[i].sequenceOfNodes[j].ID][self.sol.routes[i].sequenceOfNodes[j + 1].ID]
        #         for j in range(len(self.sol.routes[i].sequenceOfNodes) - 1)
        #     ) for i in range(len(self.sol.routes))
        # )
        return max(route.cost for route in self.sol.routes)  # if the routes costs are correct this will work, else
        # try the commented piece of code

    def FindRouteWithMaxCost(self): # mo
        # function returning the route with the maximum cost and its index in the list of routes
        for i in range(len(self.sol.routes)):
            if self.sol.routes[i].cost == self.sol.max_cost_of_route:
                return (i,self.sol.routes[i])
       # return [(i,self.sol.routes[i]) if self.sol.routes[i].cost == self.sol.max_cost_of_route else None for i in range(len(self.sol.routes))]

    def LocalSearch(self, operator):
        self.bestSolution = self.cloneSolution(self.sol)
        terminationCondition = False
        localSearchIterator = 0

        top = TwoOptMove()

        while terminationCondition is False:
            top.Initialize()
            #SolDrawer.draw(localSearchIterator, self.sol, self.allNodes)
            if operator == 2:
                self.FindBestTwoOptMove(top)
                if top.positionOfFirstRoute is not None:
                    if top.moveCost < 0:
                        self.ApplyTwoOptMove(top)
                    else:
                        terminationCondition = True
            self.TestSolution()
            self.ReportSolution(self.sol)

            if (self.sol.max_cost_of_route <= self.bestSolution.max_cost_of_route):
                self.bestSolution = self.cloneSolution(self.sol)

            localSearchIterator = localSearchIterator + 1

        self.sol = self.bestSolution


    def ReportSolution(self, sol):
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            for j in range(0, len(rt.sequenceOfNodes)):
                print(rt.sequenceOfNodes[j].ID, end=' ')
            print(rt.cost)
        print(self.sol.max_cost_of_route)

    def cloneRoute(self, rt: Route):
        cloned = Route(self.depot, self.capacity)
        cloned.cost = rt.cost
        cloned.load = rt.load
        cloned.sequenceOfNodes = rt.sequenceOfNodes.copy()
        return cloned

    def cloneSolution(self, sol: Solution):
        cloned = Solution()
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            clonedRoute = self.cloneRoute(rt)
            cloned.routes.append(clonedRoute)
        cloned.max_cost_of_route = self.sol.max_cost_of_route
        return cloned

    def FindBestTwoOptMove(self,top):  # spy ---> this method finds the best 2-opt move, which is the one that reduces cost the most (needs current best as input)
        #for rtInd1 in range(0, len(self.sol.routes)):
        max_route_cost = self.CalculateMaxCostOfRoute()
        rtInd1, rt1 = self.FindRouteWithMaxCost()
        #rt1: Route = self.sol.routes[rtInd1]  # initialization of index 1 (starting node of intersection)
        for rtInd2 in range(0, len(self.sol.routes)):
            rt2: Route = self.sol.routes[rtInd2]  # initialization of index 2 (landing node after resolving intersection)
            for nodeInd1 in range(1, len(rt1.sequenceOfNodes) - 1):# den prepei na ksekinaei apo 0 apeidei o pinakas den einai sumetrikos
                start2 = 1
                if (rt1 == rt2):
                    start2 = nodeInd1 + 2  # landing point must be at least 2 positions after starting point

                for nodeInd2 in range(start2, len(rt2.sequenceOfNodes) - 1):
                    moveCost = 10 ** 9

                    A = rt1.sequenceOfNodes[nodeInd1]  # the starting node of the intersection
                    B = rt1.sequenceOfNodes[nodeInd1 + 1]  # the next node of the starting node
                    K = rt2.sequenceOfNodes[nodeInd2]  # the node that we land to continue the sequence after resolving the intersection
                    L = rt2.sequenceOfNodes[nodeInd2 + 1]  # the next node of node K

                    if rt1 == rt2:
                        if nodeInd1 == 0 and nodeInd2 == len(rt1.sequenceOfNodes) - 2:
                            continue
                        costAdded = self.time_matrix[A.ID][K.ID] + self.time_matrix[B.ID][L.ID]
                        costRemoved = self.time_matrix[A.ID][B.ID] + self.time_matrix[K.ID][L.ID]
                        moveCost = costAdded - costRemoved

                    else:
                        if nodeInd1 == 0 and nodeInd2 == 0:
                            continue
                        if nodeInd1 == len(rt1.sequenceOfNodes) - 2 and nodeInd2 == len(rt2.sequenceOfNodes) - 2:
                            continue

                        if self.CapacityIsViolated(rt1, nodeInd1, rt2, nodeInd2):
                            continue

                        moveCost = self.RouteCostCheck(rt1, rt2, nodeInd1, nodeInd2)

                    if moveCost < top.moveCost and abs(moveCost) > 0.0001:
                        # compares current move cost with best move cost at the time and stores best
                        self.StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top)

    def CapacityIsViolated(self, rt1, nodeInd1, rt2, nodeInd2):
        rt1FirstSegmentLoad = 0
        for i in range(0, nodeInd1 + 1):
            n = rt1.sequenceOfNodes[i]
            rt1FirstSegmentLoad += n.demand
        rt1SecondSegmentLoad = rt1.load - rt1FirstSegmentLoad

        rt2FirstSegmentLoad = 0
        for i in range(0, nodeInd2 + 1):
            n = rt2.sequenceOfNodes[i]
            rt2FirstSegmentLoad += n.demand
        rt2SecondSegmentLoad = rt2.load - rt2FirstSegmentLoad

        if (rt1FirstSegmentLoad + rt2SecondSegmentLoad > rt1.capacity):
            return True
        if (rt2FirstSegmentLoad + rt1SecondSegmentLoad > rt2.capacity):
            return True

        return False

    def RouteCostCheck(self,rtInd1, rtInd2, nodeInd1, nodeInd2):
        rt1 = self.cloneRoute(rtInd1)
        rt2 = self.cloneRoute(rtInd2)
        relocatedSegmentOfRt1 = rt1.sequenceOfNodes[nodeInd1 + 1:]

        # slice with the nodes from position top.positionOfFirstNode + 1 onwards
        relocatedSegmentOfRt2 = rt2.sequenceOfNodes[nodeInd2 + 1:]

        del rt1.sequenceOfNodes[nodeInd1 + 1:]
        del rt2.sequenceOfNodes[nodeInd2 + 1:]

        rt1.sequenceOfNodes.extend(relocatedSegmentOfRt2)
        rt2.sequenceOfNodes.extend(relocatedSegmentOfRt1)

        self.UpdateRouteCostAndLoad(rt1)
        self.UpdateRouteCostAndLoad(rt2)
        max_cost_route = self.CalculateMaxCostOfRoute()

        if rt1.cost < max_cost_route and rt2.cost < max_cost_route:
            move_cost = rt1.cost - max_cost_route
            return move_cost
        else:
            return 10*9



    def StoreBestTwoOptMove(self, rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost,top):
        # spy ---> this method keeps the routes and nodes of current best 2-opt move
        top.positionOfFirstRoute = rtInd1
        top.positionOfSecondRoute = rtInd2
        top.positionOfFirstNode = nodeInd1
        top.positionOfSecondNode = nodeInd2
        top.moveCost = moveCost

    def ApplyTwoOptMove(self, top):
        rt1: Route = self.sol.routes[top.positionOfFirstRoute]
        rt2: Route = self.sol.routes[top.positionOfSecondRoute]

        if rt1 == rt2:
            # reverses the nodes in the segment [positionOfFirstNode + 1,  top.positionOfSecondNode]
            reversedSegment = reversed(rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1])
            # lst = list(reversedSegment)
            # lst2 = list(reversedSegment)
            rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegment

            # reversedSegmentList = list(reversed(rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1]))
            # rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegmentList

            rt1.cost += top.moveCost

        else:
            # slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt1 = rt1.sequenceOfNodes[top.positionOfFirstNode + 1:]

            # slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt2 = rt2.sequenceOfNodes[top.positionOfSecondNode + 1:]

            del rt1.sequenceOfNodes[top.positionOfFirstNode + 1:]
            del rt2.sequenceOfNodes[top.positionOfSecondNode + 1:]

            rt1.sequenceOfNodes.extend(relocatedSegmentOfRt2)
            rt2.sequenceOfNodes.extend(relocatedSegmentOfRt1)

            self.UpdateRouteCostAndLoad(rt1)
            self.UpdateRouteCostAndLoad(rt2)

        self.sol.max_cost_of_route = self.CalculateMaxCostOfRoute()
        self.TestSolution()

    def UpdateRouteCostAndLoad(self, rt: Route):
        tc = 0
        tl = 0
        for i in range(0, len(rt.sequenceOfNodes) - 1):
            A = rt.sequenceOfNodes[i]
            B = rt.sequenceOfNodes[i + 1]
            tc += self.time_matrix[A.ID][B.ID]
            tl += A.demand
        rt.load = tl
        rt.cost = tc

    def TestSolution(self):  # sider
        if len(self.sol.routes) > 25:  # if the solution used more routes than the routes available
            print("Routes' number problem.")
        max_cost_of_route = 0
        nodes_serviced = 0
        for r in range(0, len(self.sol.routes)):
            rt: Route = self.sol.routes[r]
            nodes_serviced += len(rt.sequenceOfNodes) - 2  # -2 because we remove depot that exist twice in every route
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
            if rtCost > max_cost_of_route:
                max_cost_of_route = rtCost
        if abs(max_cost_of_route - self.sol.max_cost_of_route) > 0.0001:
            print('Solution Cost problem, solution cost: ' + str(self.sol.max_cost_of_route) +
                  ' calculated cost: ' + str(self.CalculateMaxCostOfRoute()))
        if nodes_serviced != len(self.customers):
            print('Number of serviced nodes problem')