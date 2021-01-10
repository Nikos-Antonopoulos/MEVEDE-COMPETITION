from VRP_Model import *
from VRPMinimumInsertions import *
from SolutionDrawer import *


class Solution:
    def __init__(self): #sider
        self.max_cost_of_route = 0.0
        self.routes = []

class RelocationMove(object):
    def __init__(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = None

    def Initialize(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = 10 ** 9

class Relocations:

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

    def solveRelocations(self): # with sort variable defines if the minimum_insertions_with_opened_routes will
                                        # sort the self.customers

        self.LocalSearch(0)
        return self.sol

    def FindRouteWithMaxCost(self): # mo
        # function returning the route with the maximum cost and its index in the list of routes
        for i in range(len(self.sol.routes)):
            if self.sol.routes[i].cost == self.sol.max_cost_of_route:
                return (i,self.sol.routes[i])
       # return [(i,self.sol.routes[i]) if self.sol.routes[i].cost == self.sol.max_cost_of_route else None for i in range(len(self.sol.routes))]

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


    def LocalSearch(self, operator):
        self.bestSolution = self.cloneSolution(self.sol)
        terminationCondition = False
        localSearchIterator = 0

        rm = RelocationMove()

        while terminationCondition is False:

            self.InitializeOperators(rm)
            #SolDrawer.draw(localSearchIterator, self.sol, self.allNodes)

            # Relocations
            if operator == 0:
                self.FindBestRelocationMove(rm)
                if rm.originRoutePosition is not None:
                    if rm.moveCost < 0:
                        self.ApplyRelocationMove(rm)
                    else:
                        terminationCondition = True

            self.TestSolution()

            if (self.sol.max_cost_of_route < self.bestSolution.max_cost_of_route):
                self.bestSolution = self.cloneSolution(self.sol)

            localSearchIterator = localSearchIterator + 1

        self.sol = self.bestSolution
        print(localSearchIterator)

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

    def FindBestRelocationMove(self, rm):  # antonopoulos - mo
        unpack = self.FindRouteWithMaxCost()  # find the Route with the max cost and its index in the routes matrix
        originRouteIndex = unpack[0]  # unpack index
        rt1 = unpack[1]  # unpack Route
        for targetRouteIndex in range(0, len(self.sol.routes)):  # Every possible route that the customer can go to
            rt2: Route = self.sol.routes[targetRouteIndex]
            for originNodeIndex in range(1,
                                         len(rt1.sequenceOfNodes) - 1):  # The position of the customer that will depart
                for targetNodeIndex in range(0, len(
                        rt2.sequenceOfNodes) - 1):  # Every possible position that the customer can go to

                    if originRouteIndex == targetRouteIndex and (
                            targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                        # If the relocation will be done on the same Route
                        # If the origin and target Node are the same OR the target Node equals the last Node (the Depot) then continue
                        continue

                    A = rt1.sequenceOfNodes[originNodeIndex - 1]
                    B = rt1.sequenceOfNodes[originNodeIndex]
                    C = rt1.sequenceOfNodes[originNodeIndex + 1]

                    F = rt2.sequenceOfNodes[targetNodeIndex]
                    G = rt2.sequenceOfNodes[targetNodeIndex + 1]

                    if rt1 != rt2:  # If the routes are diferrent
                        if rt2.load + B.demand > rt2.capacity:  # if the capacity constrains are violated then continue
                            continue

                    originRtCostChange = self.time_matrix[A.ID][C.ID] - self.time_matrix[A.ID][B.ID] - \
                                         self.time_matrix[B.ID][C.ID]  # Origin route Cost Change (route with max cost)
                    targetRtCostChange = self.time_matrix[F.ID][B.ID] + self.time_matrix[B.ID][G.ID] - \
                                         self.time_matrix[F.ID][G.ID]  # Target route Cost Change
                    if rt1 != rt2:  # If the routes are diferrent
                        if (rt1.cost + originRtCostChange) > (rt2.cost + targetRtCostChange):  # if the max route is
                            # has still bigger
                            # cost or the other
                            # route with the new
                            # node has bigger cost
                            moveCost = originRtCostChange  # move cost if max route has bigger cost
                        else:
                            moveCost = rt2.cost + targetRtCostChange - self.sol.max_cost_of_route  # move cost if the other route has bigger cost
                    else:  # If the routes are same
                        costAdded = self.time_matrix[A.ID][C.ID] + self.time_matrix[F.ID][B.ID] + \
                                    self.time_matrix[B.ID][G.ID]  # cost added in the route
                        costRemoved = self.time_matrix[A.ID][B.ID] + self.time_matrix[B.ID][C.ID] + \
                                      self.time_matrix[F.ID][G.ID]  # cost removed from the route
                        moveCost = costAdded - costRemoved  # move cost is the difference from the old cost

                    if (moveCost < rm.moveCost) and abs(
                            moveCost) > 0.0001:  # if the profit is better than the profit that we've already found in the loop
                        self.StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex,
                                                     targetNodeIndex, moveCost, originRtCostChange,
                                                     targetRtCostChange, rm)

        return rm.originRoutePosition

    def ApplyRelocationMove(self, rm: RelocationMove):

        originRt = self.sol.routes[rm.originRoutePosition]  # origin route of the node to be relocated
        targetRt = self.sol.routes[rm.targetRoutePosition]  # target route of the node to be relocated

        B = originRt.sequenceOfNodes[rm.originNodePosition]  # the Node object to be relocated

        if originRt == targetRt:  # If the routes are same
            del originRt.sequenceOfNodes[rm.originNodePosition]  # delete the node from it's previous place
            if rm.originNodePosition < rm.targetNodePosition:  # if the origin node is previous from the target node in the sequence
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition,
                                                B)  # relocate the node at the target's node index
            else:
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1,
                                                B)  # relocate the node one index after the target node

            originRt.cost += rm.moveCost  # the new cost of the route will just adjusted by the move cost

        else:  # if the routes are different
            del originRt.sequenceOfNodes[rm.originNodePosition]  # delete the node from its previous place
            targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1,
                                            B)  # relocate the node one index after the target node

            originRt.cost += rm.costChangeOriginRt  # the new cost of the origin route will just adjusted by the cost
            # change of this specific route
            targetRt.cost += rm.costChangeTargetRt  # the new cost of the target route will just adjusted by the cost
            # change of this specific route
            # adjust the load of each route
            originRt.load -= B.demand
            targetRt.load += B.demand

        self.sol.max_cost_of_route = self.CalculateMaxCostOfRoute()  # find the new max cost after the relocation

        self.TestSolution()

    def StoreBestRelocationMove(self, originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost,
                                originRtCostChange, targetRtCostChange, rm: RelocationMove):
        # store the data for the relocation move
        rm.originRoutePosition = originRouteIndex
        rm.originNodePosition = originNodeIndex
        rm.targetRoutePosition = targetRouteIndex
        rm.targetNodePosition = targetNodeIndex
        rm.costChangeOriginRt = originRtCostChange
        rm.costChangeTargetRt = targetRtCostChange
        rm.moveCost = moveCost

    def InitializeOperators(self, rm):
        rm.Initialize()

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
