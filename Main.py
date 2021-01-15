from VRPMinimumInsertions import *
import pprint,time

m = Model()
m.BuildModel()
best = 100
start=time.time()
for i in range(28, 29):
    s = SolverMinIns(m, 2.5, 0.25)
    sol = s.solve(2)
    if sol.max_cost_of_route < best:
        best = sol.max_cost_of_route
        best_i = i



end=time.time()
print((end-start)/60)
