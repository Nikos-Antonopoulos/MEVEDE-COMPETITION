from VRPMinimumInsertions import *
import pprint,time

m = Model()
m.BuildModel()
best = 100
start=time.time()
for i in range(0,1):
    s = SolverMinIns(m, 4.5, 1)
    sol = s.solve()
    if sol.max_cost_of_route < best:
        best = sol.max_cost_of_route
        best_i = i
    print(sol.max_cost_of_route)


end=time.time()
print((end-start)/60)
