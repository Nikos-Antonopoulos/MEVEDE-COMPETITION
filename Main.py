from VRPMinimumInsertions import *
import pprint

m = Model()
m.BuildModel()
best = 100
for i in range(28, 29):
    s = SolverMinIns(m, 2.5, 0.25)
    sol = s.solve(7)
    if sol.max_cost_of_route < best:
        best = sol.max_cost_of_route
        best_i = i





