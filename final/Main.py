from VRPMinimumInsertions_final import *
import time

start_time = time.time()

m = Model()
m.BuildModel()

s = SolverMinIns(m)
s.solve(start_time)
sol = s.sol


# s.ReportSolution(sol)
print("Time ran: ", (time.time() - start_time)/60, " minutes")
print("Solution value: ", sol.max_cost_of_route)


