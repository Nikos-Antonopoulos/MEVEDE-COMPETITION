from VRP_Model import *
from SolutionDrawer import *


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


class CustomerInsertion(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.cost = 10 ** 9


class CustomerInsertionAllPositions(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.insertionPosition = None
        self.cost = 10 ** 9


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


class Solver:
    def __init__(self, m):
        self.allNodes = m.all_nodes
        self.customers = m.service_locations
        self.depot = m.all_nodes[0]
        self.time_matrix = m.time_matrix
        self.capacity = m.capacity
        self.sol = None
        self.bestSolution = None
        self.searchTrajectory = []

    def check_zach_example(self):  # sider
        zach_routes = routes = [[0, 1, 50, 65, 101, 130, 150, 165, 183, 0],
                                [0, 2, 46, 74, 77, 96, 120, 146, 179, 0],
                                [0, 3, 34, 72, 104, 123, 145, 162, 194, 0],
                                [0, 4, 40, 80, 103, 138, 163, 175, 198, 0],
                                [0, 5, 49, 59, 70, 98, 106, 140, 166, 19, 0],
                                [0, 6, 36, 62, 91, 107, 131, 178, 0],
                                [0, 7, 33, 73, 99, 105, 126, 153, 169, 0],
                                [0, 8, 47, 78, 115, 143, 167, 193, 0],
                                [0, 9, 39, 61, 90, 100, 108, 119, 133, 159, 177, 187, 0],
                                [0, 10, 51, 75, 85, 102, 127, 154, 173, 0],
                                [0, 11, 48, 82, 111, 142, 156, 184, 0],
                                [0, 12, 30, 41, 69, 93, 125, 151, 164, 0],
                                [0, 13, 38, 79, 94, 141, 158, 196, 199, 0],
                                [0, 14, 29, 60, 88, 117, 135, 155, 180, 200, 0],
                                [0, 15, 43, 57, 95, 124, 148, 181, 189, 0],
                                [0, 16, 52, 87, 122, 160, 192, 0],
                                [0, 17, 27, 44, 76, 112, 137, 171, 188, 0],
                                [0, 18, 31, 56, 64, 86, 116, 149, 174, 185, 0],
                                [0, 19, 28, 55, 71, 110, 129, 168, 0],
                                [0, 20, 32, 58, 84, 114, 147, 170, 191, 0],
                                [0, 21, 37, 53, 67, 97, 144, 161, 197, 0],
                                [0, 22, 35, 81, 118, 136, 157, 190, 0],
                                [0, 23, 42, 68, 89, 128, 139, 176, 186, 0],
                                [0, 24, 54, 92, 113, 134, 152, 182, 0],
                                [0, 25, 26, 45, 63, 66, 83, 109, 121, 132, 172, 0]]
        self.sol = Solution()
        for zach_route in zach_routes:
            new_route = Route(self.allNodes[0], 3000)
            for zach_node in zach_route:
                new_route.sequenceOfNodes.append(self.allNodes[zach_node])
            self.sol.routes.append(new_route)
        calculated_max_cost = self.CalculateMaxCostOfRoute()
        if calculated_max_cost == 16.271428571428572:
            print("All good in zach's example")
        else:
            print("Something is wrong in zach's example. Answer found: " + str(calculated_max_cost) +
                  ", correct answer: 16.271428571428572")

    def solve(self):
        self.SetRoutedFlagToFalseForAllCustomers()
        #   self.ApplyNearestNeighborMethod()
        self.MinimumInsertions()
        self.ReportSolution(self.sol)
        self.LocalSearch(0)
        self.ReportSolution(self.sol)
        return self.sol

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

    def SetRoutedFlagToFalseForAllCustomers(self):
        for i in range(0, len(self.customers)):
            self.customers[i].isRouted = False

    def ApplyNearestNeighborMethod(self):  # spy
        modelIsFeasible = True
        self.sol = Solution()
        insertions = 0

        while (insertions < len(self.customers)):  # while there are still not visited nodes
            bestInsertion = CustomerInsertion()  # CustomerInsertion defines an insertion (customer, route, cost)
            lastOpenRoute: Route = self.GetLastOpenRoute()  # returns the last open route (if it exists)
            # which is the route in the last position
            # of the matrix routes ( routes[-1] )

            if lastOpenRoute is not None:
                self.IdentifyBestInsertion(bestInsertion,
                                           lastOpenRoute)  # sets as bestInsertion the node (from the not routed nodes)
                # which is the nearest neighbor to the last
                # node in the examining route

            if (bestInsertion.customer is not None):  # applies best insertion and modifies cost and load respectively
                self.ApplyCustomerInsertion(bestInsertion)
                insertions += 1
            else:
                # if there is an empty available route
                if lastOpenRoute is not None and len(lastOpenRoute.sequenceOfNodes) == 2:
                    modelIsFeasible = False
                    break
                else:
                    rt = Route(self.depot, self.capacity)
                    self.sol.routes.append(rt)

        if (modelIsFeasible == False):
            print('FeasibilityIssue')
            # reportSolution

    def MinimumInsertions(self):  # sider
        modelIsFeasible = True
        self.sol = Solution()
        insertions = 0

        while (insertions < len(self.customers)):  # while there are customers that are not inserted
            bestInsertion = CustomerInsertionAllPositions()
            lastOpenRoute: Route = self.GetLastOpenRoute()  # the last route of the current solution
            # when a new route opens all the previous ones are closed
            # that's why we are using the last route, which is the only open

            if lastOpenRoute is not None:  # it means that there is at least one route opened
                self.IdentifyBestInsertionAllPositions(bestInsertion,
                                                       lastOpenRoute)  # the best insertion will be saved in the object bestInsertion

            if (bestInsertion.customer is not None):  # if a best insertion was found
                self.ApplyCustomerInsertionAllPositions(bestInsertion)  # insertion gets added to self.sol
                insertions += 1
            else:
                # If there is an empty available route
                if lastOpenRoute is not None and len(
                        lastOpenRoute.sequenceOfNodes) == 2:  # len(lastOpenRoute.sequenceOfNodes) == 2 means that in the route
                    # there are only the two dp (starting and ending point) items of initialization,
                    # so the load is 0 and if bestInsertion.customer is None means that there is at
                    # least one customer with demand bigger than the capacity of the route, so the model
                    # is not feasible
                    modelIsFeasible = False
                    break
                # If there is no empty available route and no feasible insertion was identified, which means that there is no available customer that can be added in lastOpenRoute
                else:
                    rt = Route(self.depot, self.capacity)  # a new route gets opened
                    self.sol.routes.append(rt)  # the new route gets added to the solution

        if (modelIsFeasible == False):
            print('FeasibilityIssue')
            # reportSolution

        self.TestSolution()

    def LocalSearch(self, operator):
        self.bestSolution = self.cloneSolution(self.sol)
        terminationCondition = False
        localSearchIterator = 0

        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()

        while terminationCondition is False:

            self.InitializeOperators(rm, sm, top)
            SolDrawer.draw(localSearchIterator, self.sol, self.allNodes)

            # Relocations
            if operator == 0:
                self.FindBestRelocationMove(rm)
                if rm.originRoutePosition is not None:
                    if rm.moveCost < 0:
                        self.ApplyRelocationMove(rm)
                    else:
                        terminationCondition = True
            # Swaps
            elif operator == 1:
                self.FindBestSwapMove(sm)
                if sm.positionOfFirstRoute is not None:
                    if sm.moveCost < 0:
                        self.ApplySwapMove(sm)
                    else:
                        terminationCondition = True
            elif operator == 2:
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

    def VND(self):
        self.bestSolution = self.cloneSolution(self.sol)
        VNDIterator = 0
        kmax = 2
        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()
        k = 0
        draw = True

        while k <= kmax:
            self.InitializeOperators(rm, sm, top)
            if k == 1:
                self.FindBestRelocationMove(rm)
                if rm.originRoutePosition is not None and rm.moveCost < 0:
                    self.ApplyRelocationMove(rm)
                    if draw:
                        SolDrawer.draw(VNDIterator, self.sol, self.allNodes)
                    VNDIterator = VNDIterator + 1
                    self.searchTrajectory.append(self.sol.cost)
                    k = 0
                else:
                    k += 1
            elif k == 2:
                self.FindBestSwapMove(sm)
                if sm.positionOfFirstRoute is not None and sm.moveCost < 0:
                    self.ApplySwapMove(sm)
                    if draw:
                        SolDrawer.draw(VNDIterator, self.sol, self.allNodes)
                    VNDIterator = VNDIterator + 1
                    self.searchTrajectory.append(self.sol.cost)
                    k = 0
                else:
                    k += 1
            elif k == 0:
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

            if (self.sol.max_cost_of_route < self.bestSolution.cost):
                self.bestSolution = self.cloneSolution(self.sol)

        SolDrawer.drawTrajectory(self.searchTrajectory)

    def ApplyMove(self, moveStructure):
        if isinstance(moveStructure, RelocationMove):
            self.ApplyRelocationMove(moveStructure)
        elif isinstance(moveStructure, SwapMove):
            self.ApplySwapMove(moveStructure)
        elif isinstance(moveStructure, TwoOptMove):
            self.ApplyTwoOptMove(moveStructure)

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

    def FindBestSwapMove(self, sm):
        for firstRouteIndex in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[firstRouteIndex]
            for secondRouteIndex in range(firstRouteIndex, len(self.sol.routes)):
                rt2: Route = self.sol.routes[secondRouteIndex]
                for firstNodeIndex in range(1, len(rt1.sequenceOfNodes) - 1):
                    startOfSecondNodeIndex = 1
                    if rt1 == rt2:
                        startOfSecondNodeIndex = firstNodeIndex + 1
                    for secondNodeIndex in range(startOfSecondNodeIndex, len(rt2.sequenceOfNodes) - 1):

                        a1 = rt1.sequenceOfNodes[firstNodeIndex - 1]
                        b1 = rt1.sequenceOfNodes[firstNodeIndex]
                        c1 = rt1.sequenceOfNodes[firstNodeIndex + 1]

                        a2 = rt2.sequenceOfNodes[secondNodeIndex - 1]
                        b2 = rt2.sequenceOfNodes[secondNodeIndex]
                        c2 = rt2.sequenceOfNodes[secondNodeIndex + 1]

                        moveCost = None
                        costChangeFirstRoute = None
                        costChangeSecondRoute = None

                        if rt1 == rt2:
                            if firstNodeIndex == secondNodeIndex - 1:
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
                            if rt1.load - b1.demand + b2.demand > self.capacity:
                                continue
                            if rt2.load - b2.demand + b1.demand > self.capacity:
                                continue

                            costRemoved1 = self.time_matrix[a1.ID][b1.ID] + self.time_matrix[b1.ID][c1.ID]
                            costAdded1 = self.time_matrix[a1.ID][b2.ID] + self.time_matrix[b2.ID][c1.ID]
                            costRemoved2 = self.time_matrix[a2.ID][b2.ID] + self.time_matrix[b2.ID][c2.ID]
                            costAdded2 = self.time_matrix[a2.ID][b1.ID] + self.time_matrix[b1.ID][c2.ID]

                            costChangeFirstRoute = costAdded1 - costRemoved1
                            costChangeSecondRoute = costAdded2 - costRemoved2

                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                        if moveCost < sm.moveCost and abs(moveCost) > 0.0001:
                            self.StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex,
                                                   moveCost, costChangeFirstRoute, costChangeSecondRoute, sm)

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

    def ApplySwapMove(self, sm):
        oldCost = self.CalculateTotalCost(self.sol)
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

        self.sol.cost += sm.moveCost
        self.TestSolution()

    def ReportSolution(self, sol):
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            for j in range(0, len(rt.sequenceOfNodes)):
                print(rt.sequenceOfNodes[j].ID, end=' ')
            print(rt.cost)
        print(self.sol.max_cost_of_route)

    def GetLastOpenRoute(self):
        if len(self.sol.routes) == 0:
            return None
        else:
            return self.sol.routes[-1]

    def IdentifyBestInsertion(self, bestInsertion, rt):
        for i in range(0, len(self.customers)):
            candidateCust: Node = self.customers[i]
            if candidateCust.isRouted is False:
                if rt.load + candidateCust.demand <= rt.capacity:
                    lastNodePresentInTheRoute = rt.sequenceOfNodes[-2]
                    trialCost = self.time_matrix[lastNodePresentInTheRoute.ID][candidateCust.ID]
                    if trialCost < bestInsertion.cost:
                        bestInsertion.customer = candidateCust
                        bestInsertion.route = rt
                        bestInsertion.cost = trialCost

    def ApplyCustomerInsertion(self, insertion):
        insCustomer = insertion.customer
        rt = insertion.route
        # before the second depot occurrence
        insIndex = len(rt.sequenceOfNodes) - 1
        rt.sequenceOfNodes.insert(insIndex, insCustomer)

        beforeInserted = rt.sequenceOfNodes[-3]

        costAdded = self.time_matrix[beforeInserted.ID][insCustomer.ID] + self.time_matrix[insCustomer.ID][
            self.depot.ID]
        costRemoved = self.time_matrix[beforeInserted.ID][self.depot.ID]

        rt.cost += costAdded - costRemoved
        self.sol.cost += costAdded - costRemoved

        rt.load += insCustomer.demand

        insCustomer.isRouted = True

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

    def StoreBestSwapMove(self, firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost,
                          costChangeFirstRoute, costChangeSecondRoute, sm):
        sm.positionOfFirstRoute = firstRouteIndex
        sm.positionOfSecondRoute = secondRouteIndex
        sm.positionOfFirstNode = firstNodeIndex
        sm.positionOfSecondNode = secondNodeIndex
        sm.costChangeFirstRt = costChangeFirstRoute
        sm.costChangeSecondRt = costChangeSecondRoute
        sm.moveCost = moveCost

    def CalculateTotalCost(self, sol):  # Antonopoulos
        c = 0
        for i in range(0, len(sol.routes)):  # for every route in the specific solution
            rt = sol.routes[i]
            for j in range(0, len(rt.sequenceOfNodes) - 1):  # goes back to base as well
                a = rt.sequenceOfNodes[j]
                b = rt.sequenceOfNodes[j + 1]
                c += self.time_matrix[a.ID][b.ID]  # adding cost from current node to the next node.
        return c  # returns the cost of the object:sol that belongs to class:Solution

    def InitializeOperators(self, rm, sm, top):
        rm.Initialize()
        sm.Initialize()
        top.Initialize()

    def FindBestTwoOptMove(self,
                           top):  # spy ---> this method finds the best 2-opt move, which is the one that reduces cost the most (needs current best as input)
        for rtInd1 in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[rtInd1]  # initialization of index 1 (starting node of intersection)
            for rtInd2 in range(rtInd1, len(self.sol.routes)):
                rt2: Route = self.sol.routes[
                    rtInd2]  # initialization of index 2 (landing node after resolving intersection)
                for nodeInd1 in range(0, len(rt1.sequenceOfNodes) - 1):
                    start2 = 0
                    if (rt1 == rt2):
                        start2 = nodeInd1 + 2  # landing point must be at least 2 positions after starting point

                    for nodeInd2 in range(start2, len(rt2.sequenceOfNodes) - 1):
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
                            costAdded = self.time_matrix[A.ID][L.ID] + self.time_matrix[B.ID][
                                K.ID]  # we add the cost of the 2 arcs created
                            # which are A-K B-L
                            costRemoved = self.time_matrix[A.ID][B.ID] + self.time_matrix[K.ID][
                                L.ID]  # we remove the cost of the 2 arcs deleted
                            # which are A-B K-L
                            moveCost = costAdded - costRemoved  # calculation of Dz for current 2-opt move
                        if moveCost < top.moveCost and abs(
                                moveCost) > 0.0001:  # compares current move cost with best move cost at the time and stores best
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

    def StoreBestTwoOptMove(self, rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost,
                            top):  # spy ---> this method keeps the routes and nodes of current best 2-opt move
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

        self.sol.max_cost_of_route += top.moveCost
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

    def IdentifyBestInsertionAllPositions(self, bestInsertion, rt):  # sider
        # bestInsertion: type of CustomerInsertionAllPositions rt: type of Route
        # the method finds the best insertion for a given route and assigns it to bestInsertion parameter (it is an Object so there is no need to return)
        for i in range(0, len(
                self.customers)):  # iterate all the customers, i is the index of the checking customer in self.customers
            candidateCust: Node = self.customers[i]  # the checking customer
            if candidateCust.isRouted is False:  # if the current customer being checked is not inserted
                # in a route of the solution
                if rt.load + candidateCust.demand <= rt.capacity:
                    lastNodePresentInTheRoute = rt.sequenceOfNodes[-2]
                    for j in range(0, len(
                            rt.sequenceOfNodes) - 1):  # j is the index of a node in rt(parameter).sequenceOfNodes
                        # it will be checked if the insertion of candidateCust between
                        # rt.sequenceOfNodes[j] and rt.sequenceOfNodes[j+1] costs less
                        # than the current best insertion
                        A = rt.sequenceOfNodes[j]
                        B = rt.sequenceOfNodes[j + 1]
                        costAdded = self.time_matrix[A.ID][candidateCust.ID] + self.time_matrix[candidateCust.ID][
                            B.ID]  # the costs of the 2 new connections created
                        costRemoved = self.time_matrix[A.ID][
                            B.ID]  # the cost of the connection that broke (it will be reduced from the trialCost)
                        trialCost = costAdded - costRemoved  # how the cost changed after the insertion

                        if trialCost < bestInsertion.cost:  # bestInsertion.cost is initialized to 10 ** 9
                            # the fields of bestInsertion will be updated according to the new best insertion found
                            bestInsertion.customer = candidateCust
                            bestInsertion.route = rt
                            bestInsertion.cost = trialCost
                            bestInsertion.insertionPosition = j  # the position after which the bestInsertion.customer will be inserted

    def ApplyCustomerInsertionAllPositions(self, insertion):  # sider
        # insertion: type of CustomerInsertionAllPositions
        # the new insetion will be added to the current solution
        insCustomer = insertion.customer
        rt = insertion.route
        # before the second depot occurrence
        insIndex = insertion.insertionPosition
        rt.sequenceOfNodes.insert(insIndex + 1,
                                  insCustomer)  # insCustomer gets inserted after the rt.sequenceOfNodes[indIndex]
        rt.cost += insertion.cost  # route's cost gets updated
        if rt.cost > self.sol.max_cost_of_route:  # if the new cost of the route is bigger than the max_cost_of_route of the solution,
            # self.sol.max_cost_of_route gets updated to the rt.cost
            self.sol.max_cost_of_route = rt.cost
        rt.load += insCustomer.demand  # route's cost gets updated
        insCustomer.isRouted = True  # inserted customer marked as routed
