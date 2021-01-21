from VRPMinimumInsertions_final import *
import time

m = Model()
m.BuildModel()
start_time = time.time()

s = SolverMinIns(m, 1.5)
s.solve(start_time)
sol = s.sol


# s.ReportSolution(sol)
print("Solution value: ", sol.max_cost_of_route)
print("Time ran: ", (time.time() - start_time)/60, " minutes")

