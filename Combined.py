from VRP_Model import *
from VRPMinimumInsertions import *
from SolutionDrawer import *
import random


class Solution:
    def __init__(self):  # sider
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


class SwapMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = None

    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = 10 ** 9

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

class SwapTwoWithOneMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = None

    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = 10 ** 9

class SwapTwoWithTwoMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = None

    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = 10 ** 9

class Combined:

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
        self.searchTrajectory = []

    def solveCombined(self):  # with sort variable defines if the minimum_insertions_with_opened_routes will
        # sort the self.customers
        self.VND()
        return self.sol

    def FindRouteWithMaxCost(self):  # mo
        # function returning the route with the maximum cost and its index in the list of routes
        for i in range(len(self.sol.routes)):
            if self.sol.routes[i].cost == self.sol.max_cost_of_route:
                return (i, self.sol.routes[i])

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

    def VND(self):
        self.bestSolution = self.cloneSolution(self.sol)
        VNDIterator = 0
        kmax = 4
        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()
        twom = SwapTwoWithOneMove()
        twtm = SwapTwoWithTwoMove()
        k = 0
        draw = False

        while k <= kmax:
            self.InitializeOperators(rm, sm,top,twom,twtm)
            if k == 0:
                # relocations in both max route and other routes without increasing max_cost
                self.find_best_relocation_move_max_and_other(rm)
                if rm.originRoutePosition is not None and rm.moveCost < 0:
                    self.ApplyRelocationMove(rm)
                    if draw:
                        SolDrawer.draw(VNDIterator, self.sol, self.allNodes)
                    VNDIterator = VNDIterator + 1
                    self.searchTrajectory.append(self.sol.max_cost_of_route)
                    k = 0
                else:
                    k += 1
            elif k == 2:
                # swaps in both max route and other routes without increasing max_cost
                self.find_best_swap_move_max_and_other(sm)
                if sm.positionOfFirstRoute is not None and sm.moveCost < 0:
                    self.ApplySwapMove(sm)
                    if draw:
                        SolDrawer.draw(VNDIterator, self.sol, self.allNodes)
                    VNDIterator = VNDIterator + 1
                    self.searchTrajectory.append(self.sol.max_cost_of_route)
                    k = 0
                else:
                    k += 1
            elif k == 1:
                self.FindBestTwoOptMove(top)
                if top.positionOfFirstRoute is not None and top.moveCost < 0:
                    self.ApplyTwoOptMove(top)
                    if draw:
                        SolDrawer.draw(VNDIterator, self.sol, self.allNodes)
                    VNDIterator = VNDIterator + 1
                    self.searchTrajectory.append(self.sol.max_cost_of_route)
                    k = 0
                else:
                    k += 1
            elif k == 3:
                self.find_best_SwapTwoWithOneMove(twom)
                if twom.positionOfFirstRoute is not None and twom.moveCost < 0:
                    self.ApplySwapTwoWithOneMove(twom)
                    if draw:
                        SolDrawer.draw(VNDIterator, self.sol, self.allNodes)
                    VNDIterator = VNDIterator + 1
                    self.searchTrajectory.append(self.sol.max_cost_of_route)
                    k = 0
                else:
                    k += 1
            elif k == 4:
                self.find_best_SwapTwoWithTwoMove(twtm)
                if twtm.positionOfFirstRoute is not None and twtm.moveCost < 0:
                    self.ApplySwapTwoWithTwoMove(twtm)
                    if draw:
                        SolDrawer.draw(VNDIterator, self.sol, self.allNodes)
                    VNDIterator = VNDIterator + 1
                    self.searchTrajectory.append(self.sol.max_cost_of_route)
                    k = 0
                else:
                    k += 1

            if (self.sol.max_cost_of_route < self.bestSolution.max_cost_of_route):
                self.bestSolution = self.cloneSolution(self.sol)

        SolDrawer.drawTrajectory(self.searchTrajectory)

    def LocalSearch(self, operator):
        self.bestSolution = self.cloneSolution(self.sol)
        terminationCondition = False
        localSearchIterator = 0

        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()

        while terminationCondition is False:

            self.InitializeOperators(rm, sm,top)
            # Relocations
            if operator == 0:
                self.FindBestRelocationMove(rm)
                if rm.originRoutePosition is not None:
                    if rm.moveCost < 0:
                        self.ApplyRelocationMove(rm)
                    else:
                        terminationCondition = True
            elif operator == 1:
                # Swaps
                self.FindBestSwapMove(sm)
                if sm.positionOfFirstRoute is not None:
                    if sm.moveCost < 0:
                        self.ApplySwapMove(sm)
                    else:
                        terminationCondition = True
            elif operator == 2:
                # relocations in both max route and other routes without increasing max_cost
                self.find_best_relocation_move_max_and_other(rm)
                if rm.originRoutePosition is not None:
                    if rm.moveCost < 0:
                        self.ApplyRelocationMove(rm)
                    else:
                        terminationCondition = True
            elif operator == 3:
                # swaps in both max route and other routes without increasing max_cost
                self.find_best_swap_move_max_and_other(sm)
                if sm.positionOfFirstRoute is not None:
                    if sm.moveCost < 0:
                        self.ApplySwapMove(sm)
                    else:
                        terminationCondition = True
            elif operator == 5:
                # two opt
                self.FindBestTwoOptMove(top)
                if top.positionOfFirstRoute is not None:
                    if top.moveCost < 0:
                        self.ApplyTwoOptMove(top)
                    else:
                        terminationCondition = True

            self.TestSolution()

            if (self.sol.max_cost_of_route < self.bestSolution.max_cost_of_route):
                self.bestSolution = self.cloneSolution(self.sol)

            localSearchIterator = localSearchIterator + 1

        self.sol = self.bestSolution

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

    def FindBestRelocationMove2(self, rm):  # changes only in other routes increasing the max cost
        unpack = self.FindRouteWithMaxCost()  # find the Route with the max cost and its index in the routes matrix
        max_route = unpack[1]  # unpack Route
        for originRouteIndex in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[originRouteIndex]
            if rt1 != max_route:
                for targetRouteIndex in range(0,
                                              len(self.sol.routes)):  # Every possible route that the customer can go to
                    rt2: Route = self.sol.routes[targetRouteIndex]
                    if rt2 != max_route:
                        for originNodeIndex in range(1,
                                                     len(
                                                         rt1.sequenceOfNodes) - 1):  # The position of the customer that will depart
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
                                                     self.time_matrix[B.ID][
                                                         C.ID]  # Origin route Cost Change (route with max cost)
                                targetRtCostChange = self.time_matrix[F.ID][B.ID] + self.time_matrix[B.ID][G.ID] - \
                                                     self.time_matrix[F.ID][G.ID]  # Target route Cost Change

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

    def find_best_relocation_move_max_and_other(self, rm):  # relocations in both max route and other routes without
                                                            # increasing max_cost
        unpack = self.FindRouteWithMaxCost()  # find the Route with the max cost and its index in the routes matrix
        max_route_index = unpack[0]  # unpack index
        for targetRouteIndex in range(0, len(self.sol.routes)):  # Every possible route that the customer can go to
            self.find_best_relocation_for_max_route_and_another_route(rm, max_route_index, targetRouteIndex)
        if rm.originRoutePosition is not None:
            if rm.moveCost < 0:
                return
        for originRouteIndex in range(0, len(self.sol.routes)):
            if originRouteIndex == max_route_index:
                continue
            for targetRouteIndex in range(0, len(self.sol.routes)):  # Every possible route that the customer can go to
                if targetRouteIndex == max_route_index:
                    continue
                self.find_best_relocation_for_two_routes_not_max_route(rm, originRouteIndex, targetRouteIndex)

    def find_best_relocation_for_max_route_and_another_route(self, relocation_move, max_route_index, route2_index):
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
                                        self.time_matrix[B.ID][C.ID]  # Origin route Cost Change (route with max cost)
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
                                     len(route1.sequenceOfNodes) - 1):  # The position of the customer that will depart
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

    def find_best_swap_move_max_and_other(self, sm):    # swaps in both max route and other routes without increasing
                                                        # max_cost
        self.FindBestSwapMove(sm)
        if sm.positionOfFirstRoute is not None:
            if sm.moveCost < 0:
                return
        self.FindBestSwapMove2(sm)

    def FindBestSwapMove(self, sm):  # mo
        unpack = self.FindRouteWithMaxCost()  # find the Route with the max cost and its index in the routes matrix
        max_route_index = unpack[0]  # unpack index
        max_route = unpack[1]  # unpack Route
        for route2_index in range(0, len(
                self.sol.routes)):  # for every route that has not been checked for the first root
            route2: Route = self.sol.routes[route2_index]  # the route from which a node will be swapped
            for firstNodeIndex in range(1, len(max_route.sequenceOfNodes) - 1):  # for every node of the first route
                startOfSecondNodeIndex = 1  # start index for the second route
                if max_route_index == route2_index:  # if the routes are the same
                    startOfSecondNodeIndex = firstNodeIndex + 1  # start one node forward to avoid checking the same ones
                for secondNodeIndex in range(startOfSecondNodeIndex, len(
                        route2.sequenceOfNodes) - 1):  # for every node of the second route after the index we specified

                    # nodes of the first route
                    a1 = max_route.sequenceOfNodes[firstNodeIndex - 1]
                    b1 = max_route.sequenceOfNodes[firstNodeIndex]
                    c1 = max_route.sequenceOfNodes[firstNodeIndex + 1]

                    # nodes of the second route
                    a2 = route2.sequenceOfNodes[secondNodeIndex - 1]
                    b2 = route2.sequenceOfNodes[secondNodeIndex]
                    c2 = route2.sequenceOfNodes[secondNodeIndex + 1]

                    moveCost = None
                    costChangeFirstRoute = None
                    costChangeSecondRoute = None

                    if max_route_index == route2_index:  # if the routes are same
                        if firstNodeIndex == secondNodeIndex - 1:  # if the first node is behind the second node
                            costRemoved = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[b1.ID][b2.ID] + \
                                          self.time_matrix[b2.ID][c2.ID]
                            costAdded = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][b1.ID] + \
                                        self.time_matrix[b1.ID][c2.ID]
                            moveCost = costAdded - costRemoved

                        else:
                            costRemoved1 = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[b1.ID][c1.ID]
                            costAdded1 = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][c1.ID]
                            costRemoved2 = self.time_matrix[a2.ID][b2.ID] + self.time_matrix[b2.ID][c2.ID]
                            costAdded2 = self.time_matrix[a2.ID][b1.ID] + self.time_matrix[b1.ID][c2.ID]
                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                    else:
                        if max_route.load - b1.demand + b2.demand > self.capacity:
                            continue
                        if route2.load - b2.demand + b1.demand > self.capacity:
                            continue

                        costRemoved1 = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[b1.ID][c1.ID]
                        costAdded1 = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][c1.ID]
                        costRemoved2 = self.time_matrix[a2.ID][b2.ID] + self.time_matrix[b2.ID][c2.ID]
                        costAdded2 = self.time_matrix[a2.ID][b1.ID] + self.time_matrix[b1.ID][c2.ID]

                        costChangeFirstRoute = costAdded1 - costRemoved1
                        costChangeSecondRoute = costAdded2 - costRemoved2
                        if (max_route.cost + costChangeFirstRoute) > (route2.cost + costChangeSecondRoute):
                            moveCost = costChangeFirstRoute
                        else:
                            moveCost = route2.cost + costChangeSecondRoute - self.sol.max_cost_of_route
                    if moveCost < sm.moveCost and abs(moveCost) > 0.0001:
                        self.StoreBestSwapMove(max_route_index, route2_index, firstNodeIndex, secondNodeIndex,
                                               moveCost, costChangeFirstRoute, costChangeSecondRoute, sm)

    def FindBestSwapMove2(self, sm):  # mo
        unpack = self.FindRouteWithMaxCost()  # find the Route with the max cost and its index in the routes matrix
        max_route = unpack[1]  # unpack Route
        for route1_index in range(0, len(self.sol.routes)):
            route1: Route = self.sol.routes[route1_index]
            if route1 != max_route:
                for route2_index in range(route1_index, len(
                        self.sol.routes)):  # for every route that has not been checked for the first root
                    route2: Route = self.sol.routes[route2_index]  # the route from which a node will be swapped
                    if route2 != max_route:
                        for firstNodeIndex in range(1,
                                                    len(route1.sequenceOfNodes) - 1):  # for every node of the first route
                            startOfSecondNodeIndex = 1  # start index for the second route
                            if route1 == route2:  # if the routes are the same
                                startOfSecondNodeIndex = firstNodeIndex + 1  # start one node forward to avoid checking the same ones
                            for secondNodeIndex in range(startOfSecondNodeIndex, len(
                                    route2.sequenceOfNodes) - 1):  # for every node of the second route after the index we specified

                                # nodes of the first route
                                a1 = route1.sequenceOfNodes[firstNodeIndex - 1]
                                b1 = route1.sequenceOfNodes[firstNodeIndex]
                                c1 = route1.sequenceOfNodes[firstNodeIndex + 1]

                                # nodes of the second route
                                a2 = route2.sequenceOfNodes[secondNodeIndex - 1]
                                b2 = route2.sequenceOfNodes[secondNodeIndex]
                                c2 = route2.sequenceOfNodes[secondNodeIndex + 1]

                                moveCost = None
                                costChangeFirstRoute = None
                                costChangeSecondRoute = None

                                if route1 == route2:  # if the routes are same
                                    if firstNodeIndex == secondNodeIndex - 1:  # if the first node is behind the second node
                                        costRemoved = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[b1.ID][b2.ID] + \
                                                      self.time_matrix[b2.ID][c2.ID]
                                        costAdded = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][b1.ID] + \
                                                    self.time_matrix[b1.ID][c2.ID]
                                        moveCost = costAdded - costRemoved

                                    else:
                                        costRemoved1 = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[b1.ID][c1.ID]
                                        costAdded1 = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][c1.ID]
                                        costRemoved2 = self.time_matrix[a2.ID][b2.ID] + self.time_matrix[b2.ID][c2.ID]
                                        costAdded2 = self.time_matrix[a2.ID][b1.ID] + self.time_matrix[b1.ID][c2.ID]
                                        moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                                else:
                                    if route1.load - b1.demand + b2.demand > self.capacity:
                                        continue
                                    if route2.load - b2.demand + b1.demand > self.capacity:
                                        continue

                                    costRemoved1 = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[b1.ID][c1.ID]
                                    costAdded1 = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][c1.ID]
                                    costRemoved2 = self.time_matrix[a2.ID][b2.ID] + self.time_matrix[b2.ID][c2.ID]
                                    costAdded2 = self.time_matrix[a2.ID][b1.ID] + self.time_matrix[b1.ID][c2.ID]

                                    costChangeFirstRoute = costAdded1 - costRemoved1
                                    costChangeSecondRoute = costAdded2 - costRemoved2

                                    if (route1.cost + costChangeFirstRoute >= self.sol.max_cost_of_route or
                                            route2.cost + costChangeSecondRoute >= self.sol.max_cost_of_route):
                                        continue

                                    moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                                if moveCost < sm.moveCost and abs(moveCost) > 0.0001:
                                    self.StoreBestSwapMove(route1_index, route2_index, firstNodeIndex,
                                                           secondNodeIndex,
                                                           moveCost, costChangeFirstRoute, costChangeSecondRoute, sm)

    def ApplySwapMove(self, sm):
        rt1 = self.sol.routes[sm.positionOfFirstRoute]
        rt2 = self.sol.routes[sm.positionOfSecondRoute]
        b1 = rt1.sequenceOfNodes[sm.positionOfFirstNode]
        b2 = rt2.sequenceOfNodes[sm.positionOfSecondNode]
        rt1.sequenceOfNodes[sm.positionOfFirstNode] = b2
        rt2.sequenceOfNodes[sm.positionOfSecondNode] = b1

        if (rt1 == rt2):
            rt1.cost += sm.moveCost
        else:
            rt1.cost += sm.costChangeFirstRt
            rt2.cost += sm.costChangeSecondRt
            rt1.load = rt1.load - b1.demand + b2.demand
            rt2.load = rt2.load + b1.demand - b2.demand

        self.sol.max_cost_of_route = self.CalculateMaxCostOfRoute()  # find the new max cost after the relocation
        self.TestSolution()

    def StoreBestSwapMove(self, firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost,
                          costChangeFirstRoute, costChangeSecondRoute, sm):
        sm.positionOfFirstRoute = firstRouteIndex
        sm.positionOfSecondRoute = secondRouteIndex
        sm.positionOfFirstNode = firstNodeIndex
        sm.positionOfSecondNode = secondNodeIndex
        sm.costChangeFirstRt = costChangeFirstRoute
        sm.costChangeSecondRt = costChangeSecondRoute
        sm.moveCost = moveCost

    def FindBestTwoOptMove(self, top):
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

    def FindBestTwoOptMove_MaxRoute(self, top, rtInd1,
                                    rtInd2):  # spy ---> this method finds the best 2-opt move, which is the one that reduces cost the most (needs current best as input)
        rt1: Route = self.sol.routes[rtInd1]
        rt2: Route = self.sol.routes[rtInd2]
        route_max = self.CalculateMaxCostOfRoute()
        route1_current_cost = 0  # the current cost of the route based on the loop (0,A,B------
        for nodeInd1 in range(0, len(
                rt1.sequenceOfNodes) - 1):  # den prepei na ksekinaei apo 0 apeidei o pinakas den einai sumetrikos
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
                K = rt2.sequenceOfNodes[
                    nodeInd2]  # the node that we land to continue the sequence after resolving the intersection
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

        if rt1.cost >= max_cost_route or rt2.cost >= max_cost_route:
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

    def InitializeOperators(self, rm, sm, tp,two,twt):
        rm.Initialize()
        sm.Initialize()
        tp.Initialize()
        two.Initialize()
        twt.Initialize()

    def TestSolution(self):  # sider
        if len(self.sol.routes) > 25:  # if the solution used more routes than the routes available
            print("Routes' number problem.")
        max_cost_of_route = 0
        nodes_serviced = 0
        for r in range(0, len(self.sol.routes)):
            rt: Route = self.sol.routes[r]
            nodes_serviced += len(
                rt.sequenceOfNodes) - 2  # -2 because we remove depot that exist twice in every route
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

    def VNS(self):
        self.bestSolution = self.cloneSolution(self.sol)
        VNSIterator = 0
        kmax = 2
        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()
        k = 0
        draw = False
        while 1:
            while k <= kmax:
                self.InitializeOperators(rm, sm,top)
                if k == 0:
                    # relocations in both max route and other routes without increasing max_cost
                    self.find_best_relocation_move_max_and_other(rm)
                    if rm.originRoutePosition is not None and rm.moveCost < 0:
                        self.ApplyRelocationMove(rm)
                        if draw:
                            SolDrawer.draw(VNSIterator, self.sol, self.allNodes)
                        VNSIterator = VNSIterator + 1
                        self.searchTrajectory.append(self.sol.max_cost_of_route)
                        k = 0
                    else:
                        k += 1
                elif k == 1:
                    # swaps in both max route and other routes without increasing max_cost
                    self.find_best_swap_move_max_and_other(sm)
                    if sm.positionOfFirstRoute is not None and sm.moveCost < 0:
                        self.ApplySwapMove(sm)
                        if draw:
                            SolDrawer.draw(VNSIterator, self.sol, self.allNodes)
                        VNSIterator = VNSIterator + 1
                        self.searchTrajectory.append(self.sol.max_cost_of_route)
                        k = 0
                    else:
                        k += 1
                elif k == 2:
                    # two opt only in max route
                    self.FindBestTwoOptMove(top)
                    if top.positionOfFirstRoute is not None and top.moveCost < 0:
                        self.ApplyTwoOptMove(top)
                        if draw:
                            SolDrawer.draw(VNSIterator, self.sol, self.allNodes)
                        VNSIterator = VNSIterator + 1
                        self.searchTrajectory.append(self.sol.max_cost_of_route)
                        k = 0
                    else:
                        k += 1
                random_moves_done = 0
            print(self.sol.max_cost_of_route)
            while random_moves_done < 20:
                is_move_done = self.do_a_random_move()
                if is_move_done:
                    random_moves_done += 1
            k = 0

            # if (self.sol.max_cost_of_route < self.bestSolution.max_cost_of_route):
            #     self.bestSolution = self.cloneSolution(self.sol)

    def do_a_random_move(self):
        i = random.randint(0, 2)
        if i == 0:
            return self.do_a_random_relocation()
        elif i == 1:
            return self.do_a_random_swap()
        elif i == 2:
            return self.do_a_random_two_opt()


    def do_a_random_relocation(self):
        relocation_move = RelocationMove()

        route1_index = random.randint(0, 24)
        route1 = self.sol.routes[route1_index]
        route2_index = random.randint(0, 24)
        route2 = self.sol.routes[route2_index]
        origin_node_index = random.randint(1, len(route1.sequenceOfNodes) - 2)
        target_node_index = random.randint(0, len(route2.sequenceOfNodes) - 2)
        if route1_index == route2_index and \
                (target_node_index == origin_node_index or target_node_index == origin_node_index - 1):
            # If the relocation will be done on the same Route
            # If the origin and target Node are the same OR the target Node equals the last Node (the Depot) then continue
            return False

        A = route1.sequenceOfNodes[origin_node_index - 1]
        B = route1.sequenceOfNodes[origin_node_index]
        C = route1.sequenceOfNodes[origin_node_index + 1]

        F = route2.sequenceOfNodes[target_node_index]
        G = route2.sequenceOfNodes[target_node_index + 1]

        if route1_index != route2_index:  # If the routes are diferrent
            if route2.load + B.demand > route2.capacity:  # if the capacity constrains are violated then continue
                return False

        route1_cost_change = self.time_matrix[A.ID][C.ID] - self.time_matrix[A.ID][B.ID] - \
                             self.time_matrix[B.ID][
                                 C.ID]
        route2_cost_change = self.time_matrix[F.ID][B.ID] + self.time_matrix[B.ID][G.ID] - \
                             self.time_matrix[F.ID][G.ID]

        if (route1.cost + route1_cost_change >= self.sol.max_cost_of_route or
                route2.cost + route2_cost_change >= self.sol.max_cost_of_route):
            return False

        move_cost = route1_cost_change + route2_cost_change
        self.StoreBestRelocationMove(route1_index, route2_index, origin_node_index,
                                     target_node_index, move_cost, route1_cost_change,
                                     route2_cost_change, relocation_move)
        self.ApplyRelocationMove(relocation_move)
        return True

    def do_a_random_swap(self):
        swap_move = SwapMove()

        route1_index = random.randint(0, 24)
        route1 = self.sol.routes[route1_index]
        route2_index = random.randint(0, 24)
        route2 = self.sol.routes[route2_index]
        origin_node_index = random.randint(1, len(route1.sequenceOfNodes) - 2)
        target_node_index = random.randint(1, len(route2.sequenceOfNodes) - 2)
        # nodes of the first route
        a1 = route1.sequenceOfNodes[origin_node_index - 1]
        b1 = route1.sequenceOfNodes [origin_node_index]
        c1 = route1.sequenceOfNodes[origin_node_index + 1]

        # nodes of the second route
        a2 = route2.sequenceOfNodes[target_node_index - 1]
        b2 = route2.sequenceOfNodes[target_node_index]
        c2 = route2.sequenceOfNodes[target_node_index + 1]

        if route1_index == route2_index:  # if the routes are same
            if origin_node_index == target_node_index - 1:  # if the first node is behind the second node
                costRemoved = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[b1.ID][b2.ID] + \
                              self.time_matrix[b2.ID][c2.ID]
                costAdded = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][b1.ID] + \
                            self.time_matrix[b1.ID][c2.ID]

            else:
                costRemoved1 = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[b1.ID][c1.ID]
                costAdded1 = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][c1.ID]
                costRemoved2 = self.time_matrix[a2.ID][b2.ID] + self.time_matrix[b2.ID][c2.ID]
                costAdded2 = self.time_matrix[a2.ID][b1.ID] + self.time_matrix[b1.ID][c2.ID]
        else:
            if route1.load - b1.demand + b2.demand > self.capacity:
                return False
            if route2.load - b2.demand + b1.demand > self.capacity:
                return False

            costRemoved1 = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[b1.ID][c1.ID]
            costAdded1 = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][c1.ID]
            costRemoved2 = self.time_matrix[a2.ID][b2.ID] + self.time_matrix[b2.ID][c2.ID]
            costAdded2 = self.time_matrix[a2.ID][b1.ID] + self.time_matrix[b1.ID][c2.ID]

            costChangeFirstRoute = costAdded1 - costRemoved1
            costChangeSecondRoute = costAdded2 - costRemoved2
            if (route1.cost + costChangeFirstRoute) > (route2.cost + costChangeSecondRoute):
                moveCost = costChangeFirstRoute
            else:
                moveCost = route2.cost + costChangeSecondRoute - self.sol.max_cost_of_route

            self.StoreBestSwapMove(route1_index, route2_index, origin_node_index, target_node_index,
                                   moveCost, costChangeFirstRoute, costChangeSecondRoute, swap_move)
            self.ApplySwapMove(swap_move)
            return True

    def do_a_random_two_opt(self):
        two_opt_move = TwoOptMove()

        route1_index = random.randint(0, 24)
        route1 = self.sol.routes[route1_index]
        route2_index = random.randint(0, 24)
        route2 = self.sol.routes[route2_index]
        origin_node_index = random.randint(1, len(route1.sequenceOfNodes) - 2)
        target_node_index = random.randint(1, len(route2.sequenceOfNodes) - 2)

        A = route1.sequenceOfNodes[origin_node_index]  # the starting node of the intersection
        B = route1.sequenceOfNodes[origin_node_index + 1]  # the next node of the starting node
        K = route2.sequenceOfNodes[target_node_index]  # the node that we land to continue the sequence after resolving the intersection
        L = route2.sequenceOfNodes[target_node_index + 1]  # the next node of node K

        if route1_index == route2_index:
            if origin_node_index == 0 and target_node_index == len(route1.sequenceOfNodes) - 2:
                return False
            costAdded = self.time_matrix[A.ID][K.ID] + self.time_matrix[B.ID][L.ID]
            costRemoved = self.time_matrix[A.ID][B.ID] + self.time_matrix[K.ID][L.ID]
            moveCost = costAdded - costRemoved

        else:
            if origin_node_index == 0 and target_node_index == 0:
                return False
            if origin_node_index == len(route1.sequenceOfNodes) - 2 and target_node_index == len(route2.sequenceOfNodes) - 2:
                return False

            if self.CapacityIsViolated(route1, origin_node_index, route2, target_node_index):
                return False

            moveCost = self.RouteCostCheck(route1, route2, origin_node_index, target_node_index)

        self.StoreBestTwoOptMove(route1_index, route2_index, origin_node_index, target_node_index, moveCost, two_opt_move)
        self.ApplyTwoOptMove(two_opt_move)
        return True

    def find_best_SwapTwoWithTwoMove(self, stwtm):
        self.FindBestSwapTwoFromMaxRouteWithTwoMove(stwtm)
        if stwtm.positionOfFirstRoute is not None:
            if stwtm.moveCost < 0:
                return
        stwtm.Initialize()
        self.FindBestSwapTwoWithTwoMove2(stwtm)

    def FindBestSwapTwoFromMaxRouteWithTwoMove(self, stwtm):  # antono-sider swap 2 with 1 from the max route
        unpack = self.FindRouteWithMaxCost()  # find the Route with the max cost and its index in the routes matrix
        max_route_index = unpack[0]  # unpack index
        max_route = unpack[1]  # unpack Route
        for route2_index in range(0, len(
                self.sol.routes)):  # for every route that has not been checked for the first root
            route2: Route = self.sol.routes[route2_index]  # the route from which a node will be swapped
            for firstNodeIndex in range(1, len(max_route.sequenceOfNodes) - 2):  # for every node of the first route
                startOfSecondNodeIndex = 1  # start index for the second route
                if max_route_index == route2_index:  # if the routes are the same
                    startOfSecondNodeIndex = firstNodeIndex + 2  # start one node forward to avoid checking the same ones
                for secondNodeIndex in range(startOfSecondNodeIndex, len(
                        route2.sequenceOfNodes) - 2):  # for every node of the second route after the index we specified

                    # nodes of the first route
                    a1 = max_route.sequenceOfNodes[firstNodeIndex - 1]
                    b1 = max_route.sequenceOfNodes[firstNodeIndex]
                    c1 = max_route.sequenceOfNodes[firstNodeIndex + 1]
                    d1 = max_route.sequenceOfNodes[firstNodeIndex + 2]
                    # nodes of the second route
                    a2 = route2.sequenceOfNodes[secondNodeIndex - 1]
                    b2 = route2.sequenceOfNodes[secondNodeIndex]
                    c2 = route2.sequenceOfNodes[secondNodeIndex + 1]
                    d2 = route2.sequenceOfNodes[secondNodeIndex + 2]
                    moveCost = None
                    costChangeFirstRoute = None
                    costChangeSecondRoute = None

                    if max_route_index == route2_index:  # if the routes are same
                        if firstNodeIndex == secondNodeIndex - 2:  # if the first node is behind the second node
                            costRemoved = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[c1.ID][d1.ID] + \
                                          self.time_matrix[c2.ID][d2.ID]
                            costAdded = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[c2.ID][b1.ID] + \
                                        self.time_matrix[c1.ID][d2.ID]
                            moveCost = costAdded - costRemoved
                        else:
                            costRemoved1 = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[c1.ID][d1.ID]
                            costAdded1 = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[c2.ID][d1.ID]
                            costRemoved2 = self.time_matrix[a2.ID][b2.ID] + self.time_matrix[c2.ID][d2.ID]
                            costAdded2 = self.time_matrix[a2.ID][b1.ID] + self.time_matrix[c1.ID][d2.ID]
                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                    else:
                        if max_route.load - b1.demand - c1.demand + b2.demand + c2.demand > self.capacity:
                            continue
                        if route2.load + b1.demand + c1.demand - b2.demand - c2.demand > self.capacity:
                            continue

                        costRemoved1 = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[c1.ID][d1.ID] + \
                                       self.time_matrix[b1.ID][c1.ID]
                        costAdded1 = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[c2.ID][d1.ID] + \
                                        self.time_matrix[b2.ID][c2.ID]
                        costRemoved2 = self.time_matrix[a2.ID][b2.ID] + self.time_matrix[c2.ID][d2.ID] + \
                                        self.time_matrix[b2.ID][c2.ID]
                        costAdded2 = self.time_matrix[a2.ID][b1.ID] + self.time_matrix[c1.ID][d2.ID] + \
                                     self.time_matrix[b1.ID][c1.ID]

                        costChangeFirstRoute = costAdded1 - costRemoved1
                        costChangeSecondRoute = costAdded2 - costRemoved2
                        if (max_route.cost + costChangeFirstRoute) > (route2.cost + costChangeSecondRoute):
                            moveCost = costChangeFirstRoute
                        else:
                            moveCost = route2.cost + costChangeSecondRoute - self.sol.max_cost_of_route

                    # NO NEED TO CHECK IF THE MOVE IS TABOO, because it will be applied only if the max_cost_of_route
                    # gets reduced
                    # if self.MoveIsTabuForSwaps(a1.ID, b1.ID, c1.ID, a2.ID, b2.ID, c2.ID):
                    #     continue

                    if (moveCost < stwtm.moveCost and abs(moveCost)) > 0.0001:
                        self.StoreBestSwapMove(max_route_index, route2_index, firstNodeIndex, secondNodeIndex,
                                               moveCost, costChangeFirstRoute, costChangeSecondRoute, stwtm)

    def FindBestSwapTwoWithTwoMove2(self,
                                    stwtm):  # antono-sider 2 nodes leave from route 1 and 1 gets there from route 2
        unpack = self.FindRouteWithMaxCost()  # find the Route with the max cost and its index in the routes matrix
        max_route = unpack[1]  # unpack Route
        for route1_index in range(0, len(self.sol.routes)):
            route1: Route = self.sol.routes[route1_index]
            if route1 != max_route:
                for route2_index in range(route1_index, len(
                        self.sol.routes)):  # for every route that has not been checked for the first root
                    route2: Route = self.sol.routes[route2_index]  # the route from which a node will be swapped
                    if route2 != max_route:
                        for firstNodeIndex in range(1,
                                                    len(
                                                        route1.sequenceOfNodes) - 2):  # for every node of the first route
                            startOfSecondNodeIndex = 1  # start index for the second route
                            if route1 == route2:  # if the routes are the same
                                startOfSecondNodeIndex = firstNodeIndex + 2  # start one node forward to avoid checking the same ones
                            for secondNodeIndex in range(startOfSecondNodeIndex, len(
                                    route2.sequenceOfNodes) - 2):  # for every node of the second route after the index we specified

                                # nodes of the first route
                                a1 = route1.sequenceOfNodes[firstNodeIndex - 1]
                                b1 = route1.sequenceOfNodes[firstNodeIndex]
                                c1 = route1.sequenceOfNodes[firstNodeIndex + 1]
                                d1 = route1.sequenceOfNodes[firstNodeIndex + 2]
                                # nodes of the second route
                                a2 = route2.sequenceOfNodes[secondNodeIndex - 1]
                                b2 = route2.sequenceOfNodes[secondNodeIndex]
                                c2 = route2.sequenceOfNodes[secondNodeIndex + 1]
                                d2 = route2.sequenceOfNodes[secondNodeIndex + 2]
                                moveCost = None
                                costChangeFirstRoute = None
                                costChangeSecondRoute = None

                                if route1 == route2:  # if the routes are same
                                    if firstNodeIndex == secondNodeIndex - 2:  # if the first node is behind the second node

                                        costRemoved = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[c1.ID][d1.ID] + \
                                                      self.time_matrix[c2.ID][d2.ID]
                                        costAdded = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[c2.ID][b1.ID] + \
                                                    self.time_matrix[c1.ID][d2.ID]
                                        moveCost = costAdded - costRemoved
                                    else:
                                        costRemoved1 = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[c1.ID][d1.ID]
                                        costAdded1 = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[c2.ID][d1.ID]
                                        costRemoved2 = self.time_matrix[a2.ID][b2.ID] + self.time_matrix[c2.ID][d2.ID]
                                        costAdded2 = self.time_matrix[a2.ID][b1.ID] + self.time_matrix[c1.ID][d2.ID]
                                        moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)

                                        # if route1.cost + moveCost > self.sol.max_cost_of_route:
                                        #     continue
                                else:
                                    if route1.load - b1.demand - c1.demand + b2.demand + c2.demand > self.capacity:
                                        continue
                                    if route2.load + b1.demand + c1.demand - b2.demand - c2.demand > self.capacity:
                                        continue

                                    costRemoved1 = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[c1.ID][d1.ID] + \
                                                   self.time_matrix[b1.ID][c1.ID]
                                    costAdded1 = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[c2.ID][d1.ID] + \
                                                 self.time_matrix[b2.ID][c2.ID]
                                    costRemoved2 = self.time_matrix[a2.ID][b2.ID] + self.time_matrix[c2.ID][d2.ID] + \
                                                   self.time_matrix[b2.ID][c2.ID]
                                    costAdded2 = self.time_matrix[a2.ID][b1.ID] + self.time_matrix[c1.ID][d2.ID] + \
                                                 self.time_matrix[b1.ID][c1.ID]

                                    costChangeFirstRoute = costAdded1 - costRemoved1
                                    costChangeSecondRoute = costAdded2 - costRemoved2

                                    moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)

                                    # if (route1.cost + costChangeFirstRoute > self.sol.max_cost_of_route or
                                    #         route2.cost + costChangeSecondRoute > self.sol.max_cost_of_route):
                                    #     continue
                                    if (route1.cost + costChangeFirstRoute >= self.sol.max_cost_of_route or
                                            route2.cost + costChangeSecondRoute >= self.sol.max_cost_of_route):
                                        continue

                                if (moveCost < stwtm.moveCost and abs(moveCost)) > 0.0001:
                                    self.StoreBestSwapMove(route1_index, route2_index, firstNodeIndex,
                                                           secondNodeIndex,
                                                           moveCost, costChangeFirstRoute, costChangeSecondRoute, stwtm)

    def ApplySwapTwoWithTwoMove(self, stwtm):

        rt1 = self.sol.routes[stwtm.positionOfFirstRoute]
        rt2 = self.sol.routes[stwtm.positionOfSecondRoute]

        b1 = rt1.sequenceOfNodes[stwtm.positionOfFirstNode]
        c1 = rt1.sequenceOfNodes[stwtm.positionOfFirstNode + 1]

        b2 = rt2.sequenceOfNodes[stwtm.positionOfSecondNode]
        c2 = rt2.sequenceOfNodes[stwtm.positionOfSecondNode + 1]

        # print("b2:", b2.ID, "c2:", c2.ID, " b1:", b1.ID, "c1:", c1.ID)
        # print("RT1: ",rt1.sequenceOfNodes)
        # print("RT2: ", rt2.sequenceOfNodes)
        rt1.sequenceOfNodes[stwtm.positionOfFirstNode: stwtm.positionOfFirstNode + 2] = (b2, c2)
        rt2.sequenceOfNodes[stwtm.positionOfSecondNode: stwtm.positionOfSecondNode + 2] = (b1, c1)
        # print("RT1 AFTER: ", rt1.sequenceOfNodes)
        # print("RT2 AFTER: ", rt2.sequenceOfNodes)

        if (rt1 == rt2):
            rt1.cost += stwtm.moveCost
        else:
            rt1.cost += stwtm.costChangeFirstRt
            rt2.cost += stwtm.costChangeSecondRt
            rt1.load = rt1.load - b1.demand - c1.demand + b2.demand + c2.demand
            rt2.load = rt2.load + b1.demand + c1.demand - b2.demand - c2.demand
        self.sol.max_cost_of_route = self.CalculateMaxCostOfRoute()  # find the new max cost after the relocation

        self.TestSolution()

    def find_best_SwapTwoWithOneMove(self, stwom):
        self.FindBestSwapTwoWithOneFromMaxRouteMove(stwom)
        self.FindBestSwapTwoFromMaxRouteWithOneMove(stwom)
        if stwom.positionOfFirstRoute is not None:
            if stwom.moveCost < 0:
                return
        stwom.Initialize()
        self.FindBestSwapTwoWithOneMove2(stwom)
        print(stwom.positionOfFirstRoute,stwom.positionOfSecondRoute)

    def FindBestSwapTwoWithOneFromMaxRouteMove(self, stwom):  # antono-sider swap 2 with 1 from the max route
        unpack = self.FindRouteWithMaxCost()  # find the Route with the max cost and its index in the routes matrix
        max_route_index = unpack[0]  # unpack index
        max_route = unpack[1]  # unpack Route
        for route1_index in range(0, len(
                self.sol.routes)):  # for every route that has not been checked for the first root
            route1: Route = self.sol.routes[route1_index]  # the route from which a node will be swapped
            for route1NodeIndex in range(1, len(route1.sequenceOfNodes) - 2):  # for every node of the first route
                startOfMaxNodeIndex = 1  # start index for the second route
                if max_route_index == route1_index:  # if the routes are the same
                    startOfMaxNodeIndex = route1NodeIndex + 2  # start one node forward to avoid checking the same ones
                for maxNodeIndex in range(startOfMaxNodeIndex, len(
                        max_route.sequenceOfNodes) - 1):  # for every node of the second route after the index we specified
                    # nodes of the first route
                    a1 = route1.sequenceOfNodes[route1NodeIndex - 1]
                    b1 = route1.sequenceOfNodes[route1NodeIndex]
                    c1 = route1.sequenceOfNodes[route1NodeIndex + 1]
                    d1 = route1.sequenceOfNodes[route1NodeIndex + 2]
                    # nodes of the second route
                    a2 = max_route.sequenceOfNodes[maxNodeIndex - 1]
                    b2 = max_route.sequenceOfNodes[maxNodeIndex]
                    c2 = max_route.sequenceOfNodes[maxNodeIndex + 1]

                    moveCost = None
                    costChangeRoute1 = None
                    costChangeMaxRoute = None

                    if max_route_index == route1_index:  # if the routes are same
                        if route1NodeIndex == maxNodeIndex - 2:  # if the first node is behind the second node
                            costRemoved = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[c1.ID][d1.ID] + \
                                          self.time_matrix[b2.ID][c2.ID]
                            costAdded = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][b1.ID] + \
                                        self.time_matrix[c1.ID][c2.ID]
                            moveCost = costAdded - costRemoved
                        else:
                            costRemoved1 = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[c1.ID][d1.ID]
                            costAdded1 = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][d1.ID]
                            costRemoved2 = self.time_matrix[a2.ID][b2.ID] + self.time_matrix[b2.ID][c2.ID]
                            costAdded2 = self.time_matrix[a2.ID][b1.ID] + self.time_matrix[c1.ID][c2.ID]
                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                    else:
                        if route1.load - b1.demand - c1.demand + b2.demand > self.capacity:
                            continue
                        if max_route.load + b1.demand + c1.demand - b2.demand > self.capacity:
                            continue

                        costRemoved1 = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[c1.ID][d1.ID] + \
                                       self.time_matrix[b1.ID][c1.ID]
                        costAdded1 = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][d1.ID]
                        costRemoved2 = self.time_matrix[a2.ID][b2.ID] + self.time_matrix[b2.ID][c2.ID]
                        costAdded2 = self.time_matrix[a2.ID][b1.ID] + self.time_matrix[c1.ID][c2.ID] + \
                                     self.time_matrix[b1.ID][c1.ID]

                        costChangeRoute1 = costAdded1 - costRemoved1
                        costChangeMaxRoute = costAdded2 - costRemoved2
                        if (route1.cost + costChangeRoute1) > (max_route.cost + costChangeMaxRoute):
                            moveCost = route1.cost + costChangeRoute1 - self.sol.max_cost_of_route
                        else:
                            moveCost = costChangeMaxRoute


                    # NO NEED TO CHECK IF THE MOVE IS TABOO, because it will be applied only if the max_cost_of_route
                    # gets reduced
                    # if self.MoveIsTabuForSwaps(a1.ID, b1.ID, c1.ID, a2.ID, b2.ID, c2.ID):
                    #     continue

                    if (moveCost < stwom.moveCost and abs(moveCost)) > 0.0001:
                        self.StoreBestSwapMove(route1_index, max_route_index, route1NodeIndex, maxNodeIndex,
                                               moveCost, costChangeRoute1, costChangeMaxRoute, stwom)


    def FindBestSwapTwoFromMaxRouteWithOneMove(self, stwom):  # antono-sider swap 2 with 1 from the max route
        unpack = self.FindRouteWithMaxCost()  # find the Route with the max cost and its index in the routes matrix
        max_route_index = unpack[0]  # unpack index
        max_route = unpack[1]  # unpack Route
        for route2_index in range(0, len(
                self.sol.routes)):  # for every route that has not been checked for the first root
            route2: Route = self.sol.routes[route2_index]  # the route from which a node will be swapped
            for firstNodeIndex in range(1, len(max_route.sequenceOfNodes) - 2):  # for every node of the first route
                startOfSecondNodeIndex = 1  # start index for the second route
                if max_route_index == route2_index:  # if the routes are the same
                    startOfSecondNodeIndex = firstNodeIndex + 2  # start one node forward to avoid checking the same ones
                for secondNodeIndex in range(startOfSecondNodeIndex, len(
                        route2.sequenceOfNodes) - 1):  # for every node of the second route after the index we specified

                    # nodes of the first route
                    a1 = max_route.sequenceOfNodes[firstNodeIndex - 1]
                    b1 = max_route.sequenceOfNodes[firstNodeIndex]
                    c1 = max_route.sequenceOfNodes[firstNodeIndex + 1]
                    d1 = max_route.sequenceOfNodes[firstNodeIndex + 2]
                    # nodes of the second route
                    a2 = route2.sequenceOfNodes[secondNodeIndex - 1]
                    b2 = route2.sequenceOfNodes[secondNodeIndex]
                    c2 = route2.sequenceOfNodes[secondNodeIndex + 1]

                    moveCost = None
                    costChangeFirstRoute = None
                    costChangeSecondRoute = None

                    if max_route_index == route2_index:  # if the routes are same
                        if firstNodeIndex == secondNodeIndex - 2:  # if the first node is behind the second node
                            costRemoved = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[c1.ID][d1.ID] + \
                                          self.time_matrix[b2.ID][c2.ID]
                            costAdded = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][b1.ID] + \
                                        self.time_matrix[c1.ID][c2.ID]
                            moveCost = costAdded - costRemoved
                        else:
                            costRemoved1 = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[c1.ID][d1.ID]
                            costAdded1 = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][d1.ID]
                            costRemoved2 = self.time_matrix[a2.ID][b2.ID] + self.time_matrix[b2.ID][c2.ID]
                            costAdded2 = self.time_matrix[a2.ID][b1.ID] + self.time_matrix[c1.ID][c2.ID]
                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                    else:
                        if max_route.load - b1.demand - c1.demand + b2.demand > self.capacity:
                            continue
                        if route2.load + b1.demand + c1.demand - b2.demand > self.capacity:
                            continue

                        costRemoved1 = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[c1.ID][d1.ID] + \
                                       self.time_matrix[b1.ID][c1.ID]
                        costAdded1 = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][d1.ID]
                        costRemoved2 = self.time_matrix[a2.ID][b2.ID] + self.time_matrix[b2.ID][c2.ID]
                        costAdded2 = self.time_matrix[a2.ID][b1.ID] + self.time_matrix[c1.ID][c2.ID] + \
                                     self.time_matrix[b1.ID][c1.ID]

                        costChangeFirstRoute = costAdded1 - costRemoved1
                        costChangeSecondRoute = costAdded2 - costRemoved2
                        if (max_route.cost + costChangeFirstRoute) > (route2.cost + costChangeSecondRoute):
                            moveCost = costChangeFirstRoute
                        else:
                            moveCost = route2.cost + costChangeSecondRoute - self.sol.max_cost_of_route

                    # NO NEED TO CHECK IF THE MOVE IS TABOO, because it will be applied only if the max_cost_of_route
                    # gets reduced
                    # if self.MoveIsTabuForSwaps(a1.ID, b1.ID, c1.ID, a2.ID, b2.ID, c2.ID):
                    #     continue

                    if (moveCost < stwom.moveCost and abs(moveCost)) > 0.0001:
                        self.StoreBestSwapMove(max_route_index, route2_index, firstNodeIndex, secondNodeIndex,
                                               moveCost, costChangeFirstRoute, costChangeSecondRoute, stwom)

    def FindBestSwapTwoWithOneMove2(self,
                                    stwom):  # antono-sider 2 nodes leave from route 1 and 1 gets there from route 2
        unpack = self.FindRouteWithMaxCost()  # find the Route with the max cost and its index in the routes matrix
        max_route = unpack[1]  # unpack Route
        for route1_index in range(0, len(self.sol.routes)):
            route1: Route = self.sol.routes[route1_index]
            if route1 != max_route:
                for route2_index in range(route1_index, len(
                        self.sol.routes)):  # for every route that has not been checked for the first root
                    route2: Route = self.sol.routes[route2_index]  # the route from which a node will be swapped
                    if route2 != max_route:
                        for firstNodeIndex in range(1,
                                                    len(
                                                        route1.sequenceOfNodes) - 2):  # for every node of the first route
                            startOfSecondNodeIndex = 1  # start index for the second route
                            if route1 == route2:  # if the routes are the same
                                startOfSecondNodeIndex = firstNodeIndex + 2  # start one node forward to avoid checking the same ones
                            for secondNodeIndex in range(startOfSecondNodeIndex, len(
                                    route2.sequenceOfNodes) - 1):  # for every node of the second route after the index we specified

                                # nodes of the first route
                                a1 = route1.sequenceOfNodes[firstNodeIndex - 1]
                                b1 = route1.sequenceOfNodes[firstNodeIndex]
                                c1 = route1.sequenceOfNodes[firstNodeIndex + 1]
                                d1 = route1.sequenceOfNodes[firstNodeIndex + 2]
                                # nodes of the second route
                                a2 = route2.sequenceOfNodes[secondNodeIndex - 1]
                                b2 = route2.sequenceOfNodes[secondNodeIndex]
                                c2 = route2.sequenceOfNodes[secondNodeIndex + 1]

                                moveCost = None
                                costChangeFirstRoute = None
                                costChangeSecondRoute = None

                                if route1 == route2:  # if the routes are same
                                    if firstNodeIndex == secondNodeIndex - 2:  # if the first node is behind the second node

                                        costRemoved = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[c1.ID][d1.ID] + \
                                                      self.time_matrix[b2.ID][c2.ID]
                                        costAdded = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][b1.ID] + \
                                                    self.time_matrix[c1.ID][c2.ID]
                                        moveCost = costAdded - costRemoved
                                    else:
                                        costRemoved1 = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[c1.ID][d1.ID]
                                        costAdded1 = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][d1.ID]
                                        costRemoved2 = self.time_matrix[a2.ID][b2.ID] + self.time_matrix[b2.ID][c2.ID]
                                        costAdded2 = self.time_matrix[a2.ID][b1.ID] + self.time_matrix[c1.ID][c2.ID]
                                        moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)

                                        # if route1.cost + moveCost > self.sol.max_cost_of_route:
                                        #     continue
                                else:
                                    if route1.load - b1.demand - c1.demand + b2.demand > self.capacity:
                                        continue
                                    if route2.load + b1.demand + c1.demand - b2.demand > self.capacity:
                                        continue

                                    costRemoved1 = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[c1.ID][d1.ID] + \
                                                   self.time_matrix[b1.ID][c1.ID]
                                    costAdded1 = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][d1.ID]
                                    costRemoved2 = self.time_matrix[a2.ID][b2.ID] + self.time_matrix[b2.ID][c2.ID]
                                    costAdded2 = self.time_matrix[a2.ID][b1.ID] + self.time_matrix[c1.ID][c2.ID] + \
                                                 self.time_matrix[b1.ID][c1.ID]

                                    costChangeFirstRoute = costAdded1 - costRemoved1
                                    costChangeSecondRoute = costAdded2 - costRemoved2

                                    moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)

                                    # if (route1.cost + costChangeFirstRoute > self.sol.max_cost_of_route or
                                    #         route2.cost + costChangeSecondRoute > self.sol.max_cost_of_route):
                                    #     continue
                                    if (route1.cost + costChangeFirstRoute >= self.sol.max_cost_of_route or
                                            route2.cost + costChangeSecondRoute >= self.sol.max_cost_of_route):
                                        continue

                                if moveCost < stwom.moveCost and abs(moveCost) > 0.0001:
                                    self.StoreBestSwapMove(route1_index, route2_index, firstNodeIndex,
                                                           secondNodeIndex,
                                                           moveCost, costChangeFirstRoute, costChangeSecondRoute, stwom)

    def ApplySwapTwoWithOneMove(self, stwom):

        rt1 = self.sol.routes[stwom.positionOfFirstRoute]
        rt2 = self.sol.routes[stwom.positionOfSecondRoute]

        b1 = rt1.sequenceOfNodes[stwom.positionOfFirstNode]
        c1 = rt1.sequenceOfNodes[stwom.positionOfFirstNode + 1]

        b2 = rt2.sequenceOfNodes[stwom.positionOfSecondNode]

        # print("b2:", b2.ID, " b1:", b1.ID, "c1:", c1.ID)
        # print("RT1: ",rt1.sequenceOfNodes)
        # print("RT2: ", rt2.sequenceOfNodes)
        rt1.sequenceOfNodes.insert(stwom.positionOfFirstNode + 2, b2)
        rt1.sequenceOfNodes.remove(b1)
        rt1.sequenceOfNodes.remove(c1)
        if rt1 == rt2:
            rt2.sequenceOfNodes[stwom.positionOfSecondNode - 1: stwom.positionOfSecondNode] = (b1, c1)
        else:
            rt2.sequenceOfNodes[stwom.positionOfSecondNode : stwom.positionOfSecondNode + 1] = (b1, c1)
        # print("RT1 AFTER: ", rt1.sequenceOfNodes)
        # print("RT2 AFTER: ", rt2.sequenceOfNodes)

        if (rt1 == rt2):
            rt1.cost += stwom.moveCost
        else:
            rt1.cost += stwom.costChangeFirstRt
            rt2.cost += stwom.costChangeSecondRt
            rt1.load = rt1.load - b1.demand - c1.demand + b2.demand
            rt2.load = rt2.load + b1.demand + c1.demand - b2.demand

        self.sol.max_cost_of_route = self.CalculateMaxCostOfRoute()  # find the new max cost after the relocation

        self.TestSolution()
        unpack = self.FindRouteWithMaxCost()
        # print("Swap Move",b1.ID,b2.ID, rt1 == unpack[1] or rt2 == unpack[1], sm.moveCost)