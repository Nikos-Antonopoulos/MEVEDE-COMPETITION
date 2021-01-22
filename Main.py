from VRPMinimumInsertions_final import *
import time

m = Model()
m.BuildModel()
start = time.time()

good_const = [(3.25, 0.75)]
for const1, const2 in good_const:
    for seed in range(107, 108):
        s = SolverMinIns(m, const1, const2)
        s.solve(seed)
        sol = s.sol
        f = open("final_test_file.txt", "a")
        f.write("\n" + str(sol.max_cost_of_route) + " " + str(const1) + " " + str(const2) + " " + str(seed))

# s.ReportSolution(sol)
print(sol.max_cost_of_route)

end = time.time()
print((end-start)/60)

f.close()
