
from VRPMinimumInsertions import *
import pprint


m = Model()
m.BuildModel()
best = 100
for i in range(28,29):
    s = SolverMinIns(m, i/4)
    for j in range(0, 10):
        sol = s.solve(j)
        if sol.max_cost_of_route < best:
            best = sol.max_cost_of_route
            best_i = i
            best_j = j
print(best, best_i, best_j)




# routes=m.load_objects()
# print(m.CalculateMaxCostOfRoute(routes,m.time_matrix))

