from VRPMinimumInsertions_final import *
import time

m = Model()
m.BuildModel()
start = time.time()

list_of_constants= [(4.5, 0), (2.5, 0.5), (4.5, 1), (6, 1.5), (3.5, 0.75)]
for const1, const2 in list_of_constants:
    for seed in range(101, 111):
        s = SolverMinIns(m, const1, const2)
        s.solve(seed)
        sol = s.sol
        f = open("final_test_file.txt", "a")
        f.write("\n" + str(sol.max_cost_of_route) + " " + str(const1) + " " +str(const2) + " " + str(seed))

# s.ReportSolution(sol)
print(sol.max_cost_of_route)

end = time.time()
print((end-start)/60)

f.close()