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
            SolDrawer.draw(localSearchIterator, self.sol, self.allNodes)
            if operator == 2:
                self.FindBestTwoOptMove(top)
                if top.positionOfFirstRoute is not None:
                    if top.moveCost < 0:
                        self.ApplyTwoOptMove(top)
                    else:
                        terminationCondition = True
            self.TestSolution()
            #self.ReportSolution(self.sol)


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

    def FindBestTwoOptMove(self,top):
        rtInd_max, rt_max = self.FindRouteWithMaxCost()
        for rtInd2 in range(0, len(self.sol.routes)):
            self.FindBestTwoOptMove_MaxRoute(top, rtInd_max, rtInd2)
        if top.positionOfFirstRoute is not None:
            if top.moveCost < 0:
                return
        for rtInd1 in range(0, len(self.sol.routes)):
            if rtInd1 == rtInd_max:
                continue
            for rtInd2 in range(0, len(self.sol.routes)):
                if rtInd2 == rtInd_max:
                    continue
                self.FindBestTwoOptMove_notMaxRoute(top, rtInd1, rtInd2)

    def FindBestTwoOptMove_MaxRoute(self,top, rtInd1, rtInd2):  # spy ---> this method finds the best 2-opt move, which is the one that reduces cost the most (needs current best as input)
        rt1: Route = self.sol.routes[rtInd1]
        rt2: Route = self.sol.routes[rtInd2]
        route_max = self.CalculateMaxCostOfRoute()
        route1_current_cost = 0  # the current cost of the route based on the loop (0,A,B------
        for nodeInd1 in range(0, len(rt1.sequenceOfNodes) - 1):# den prepei na ksekinaei apo 0 apeidei o pinakas den einai sumetrikos
            route2_current_cost = 0
            one = rt1.sequenceOfNodes[nodeInd1 - 1]
            two = rt1.sequenceOfNodes[nodeInd1]
            route1_current_cost += self.time_matrix[one.ID][two.ID]  # adding to current route cost
            start2 = 0
            if (rt1 == rt2):
                start2 = nodeInd1 + 2  # landing point must be at least 2 positions after starting point

            for nodeInd2 in range(start2, len(rt2.sequenceOfNodes) - 1):
                three = rt2.sequenceOfNodes[nodeInd2 - 1]
                four = rt2.sequenceOfNodes[nodeInd2]
                route2_current_cost += self.time_matrix[three.ID][four.ID]
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

                    rt1_cost = route1_current_cost + self.time_matrix[A.ID][L.ID] + rt2.cost - route2_current_cost - \
                               self.time_matrix[K.ID][L.ID]
                    rt2_cost = route2_current_cost + self.time_matrix[B.ID][K.ID] + rt1.cost - route1_current_cost - \
                               self.time_matrix[A.ID][B.ID]

                    if rt1_cost < route_max and rt2_cost < route_max:
                        if rt1_cost > rt2_cost:
                            moveCost = rt1_cost - route_max
                        else:
                            moveCost = rt2_cost - route_max

                if moveCost < top.moveCost and abs(moveCost) > 0.0001:
                    # compares current move cost with best move cost at the time and stores best
                    self.StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top)



    def FindBestTwoOptMove_notMaxRoute(self, top, rtInd1, rtInd2):  # spy + mark ---> this method finds the best 2-opt move, which is the one that reduces cost the most (needs current best as input)
        rt1: Route = self.sol.routes[rtInd1]
        rt2: Route = self.sol.routes[rtInd2]
        route_max = self.CalculateMaxCostOfRoute()
        route1_current_cost = 0 # the current cost of the route based on the loop (0,A,B------
        route2_current_cost = 0 # the current cost of the route based on the loop (0,K,L------
        for nodeInd1 in range(1, len(rt1.sequenceOfNodes) - 1): # den prepei na ksekinaei apo 0 apeidei o pinakas den einai sumetrikos
            route2_current_cost = 0
            one = rt1.sequenceOfNodes[nodeInd1-1]
            two = rt1.sequenceOfNodes[nodeInd1]
            route1_current_cost += self.time_matrix[one.ID][two.ID]  # adding to current route cost
            start2 = 1
            if (rt1 == rt2):
                start2 = nodeInd1 + 2  # landing point must be at least 2 positions after starting point

            for nodeInd2 in range(start2, len(rt2.sequenceOfNodes) - 1):
                three = rt2.sequenceOfNodes[nodeInd2-1]
                four = rt2.sequenceOfNodes[nodeInd2]
                route2_current_cost += self.time_matrix[three.ID][four.ID]
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

                    rt1_cost = route1_current_cost + self.time_matrix[A.ID][L.ID] + rt2.cost - route2_current_cost - \
                               self.time_matrix[K.ID][L.ID]
                    rt2_cost = route2_current_cost + self.time_matrix[B.ID][K.ID] + rt1.cost - route1_current_cost - \
                               self.time_matrix[A.ID][B.ID]

                    if rt1_cost >= route_max or rt2_cost >= route_max:
                         continue

                    costAdded = self.time_matrix[A.ID][L.ID] + self.time_matrix[B.ID][K.ID]
                    costRemoved = self.time_matrix[A.ID][B.ID] + self.time_matrix[K.ID][L.ID]
                    moveCost = costAdded - costRemoved

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
            if rt1.cost > rt2.cost:
                move_cost = rt1.cost - max_cost_route
                return move_cost
            else:
                move_cost = rt2.cost - max_cost_route
                return move_cost
        else:
            return 10*9

    def RouteCostCheck_notMax(self, rtInd1, rtInd2, nodeInd1, nodeInd2):
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

        if rt1.cost > max_cost_route or rt2.cost > max_cost_route:
            return True
        else:
            return False



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

            def find_best_relocation_move_max_and_other(self,
                                                        rm):  # relocations in both max route and other routes without
                # increasing max_cost
                unpack = self.FindRouteWithMaxCost()  # find the Route with the max cost and its index in the routes matrix
                max_route_index = unpack[0]  # unpack index
                for targetRouteIndex in range(0,
                                              len(self.sol.routes)):  # Every possible route that the customer can go to
                    self.find_best_relocation_for_max_route_and_another_route(rm, max_route_index, targetRouteIndex)
                if rm.originRoutePosition is not None:
                    if rm.moveCost < 0:
                        return
                for originRouteIndex in range(0, len(self.sol.routes)):
                    if originRouteIndex == max_route_index:
                        continue
                    for targetRouteIndex in range(0, len(
                            self.sol.routes)):  # Every possible route that the customer can go to
                        if targetRouteIndex == max_route_index:
                            continue
                        self.find_best_relocation_for_two_routes_not_max_route(rm, originRouteIndex, targetRouteIndex)

            def find_best_relocation_for_max_route_and_another_route(self, relocation_move, max_route_index,
                                                                     route2_index):
                max_route: Route = self.sol.routes[max_route_index]
                route2: Route = self.sol.routes[route2_index]
                for originNodeIndex in range(1, len(
                        max_route.sequenceOfNodes) - 1):  # The position of the customer that will depart
                    for targetNodeIndex in range(0, len(
                            route2.sequenceOfNodes) - 1):  # Every possible position that the customer can go to

                        if max_route_index == route2_index and \
                                (targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            # If the relocation will be done on the same Route
                            # If the origin and target Node are the same OR the target Node equals the last Node (the Depot) then continue
                            continue

                        A = max_route.sequenceOfNodes[originNodeIndex - 1]
                        B = max_route.sequenceOfNodes[originNodeIndex]
                        C = max_route.sequenceOfNodes[originNodeIndex + 1]

                        F = route2.sequenceOfNodes[targetNodeIndex]
                        G = route2.sequenceOfNodes[targetNodeIndex + 1]

                        if max_route_index != route2_index:  # If the routes are diferrent
                            if route2.load + B.demand > route2.capacity:  # if the capacity constrains are violated then continue
                                continue

                        max_route_cost_change = self.time_matrix[A.ID][C.ID] - self.time_matrix[A.ID][B.ID] - \
                                                self.time_matrix[B.ID][
                                                    C.ID]  # Origin route Cost Change (route with max cost)
                        route2_cost_change = self.time_matrix[F.ID][B.ID] + self.time_matrix[B.ID][G.ID] - \
                                             self.time_matrix[F.ID][G.ID]  # Target route Cost Change

                        if max_route_index != route2_index:  # If the routes are diferrent
                            if (max_route.cost + max_route_cost_change) > (
                                    route2.cost + route2_cost_change):  # if the max route is
                                # has still bigger
                                # cost or the other
                                # route with the new
                                # node has bigger cost
                                move_cost = max_route_cost_change  # move cost if max route has bigger cost
                            else:
                                move_cost = route2.cost + route2_cost_change - self.sol.max_cost_of_route  # move cost if the other route has bigger cost
                        else:  # If the routes are same
                            move_cost = max_route_cost_change + route2_cost_change  # move cost is the difference from the old cost

                        if (move_cost < relocation_move.moveCost) and \
                                abs(
                                    move_cost) > 0.0001:  # if the profit is better than the profit that we've already found in the loop
                            self.StoreBestRelocationMove(max_route_index, route2_index, originNodeIndex,
                                                         targetNodeIndex, move_cost, max_route_cost_change,
                                                         route2_cost_change, relocation_move)

            def find_best_relocation_for_two_routes_not_max_route(self, relocation_move, route1_index, route2_index):
                route1: Route = self.sol.routes[route1_index]
                route2: Route = self.sol.routes[route2_index]
                for originNodeIndex in range(1,
                                             len(
                                                 route1.sequenceOfNodes) - 1):  # The position of the customer that will depart
                    for targetNodeIndex in range(0, len(
                            route2.sequenceOfNodes) - 1):  # Every possible position that the customer can go to

                        if route1_index == route2_index and \
                                (targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            # If the relocation will be done on the same Route
                            # If the origin and target Node are the same OR the target Node equals the last Node (the Depot) then continue
                            continue

                        A = route1.sequenceOfNodes[originNodeIndex - 1]
                        B = route1.sequenceOfNodes[originNodeIndex]
                        C = route1.sequenceOfNodes[originNodeIndex + 1]

                        F = route2.sequenceOfNodes[targetNodeIndex]
                        G = route2.sequenceOfNodes[targetNodeIndex + 1]

                        if route1_index != route2_index:  # If the routes are diferrent
                            if route2.load + B.demand > route2.capacity:  # if the capacity constrains are violated then continue
                                continue

                        route1_cost_change = self.time_matrix[A.ID][C.ID] - self.time_matrix[A.ID][B.ID] - \
                                             self.time_matrix[B.ID][
                                                 C.ID]  # Origin route Cost Change (route with max cost)
                        route2_cost_change = self.time_matrix[F.ID][B.ID] + self.time_matrix[B.ID][G.ID] - \
                                             self.time_matrix[F.ID][G.ID]  # Target route Cost Change

                        if (route1.cost + route1_cost_change >= self.sol.max_cost_of_route or
                                route2.cost + route2_cost_change >= self.sol.max_cost_of_route):
                            continue

                        move_cost = route1_cost_change + route2_cost_change  # move cost is the difference from the old cost

                        if (move_cost < relocation_move.moveCost) \
                                and abs(
                            move_cost) > 0.0001:  # if the profit is better than the profit that we've already found in the loop
                            self.StoreBestRelocationMove(route1_index, route2_index, originNodeIndex,
                                                         targetNodeIndex, move_cost, route1_cost_change,
                                                         route2_cost_change, relocation_move)