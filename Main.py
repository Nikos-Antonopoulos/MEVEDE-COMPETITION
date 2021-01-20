from VRPMinimumInsertions_final import *
import time

m = Model()
m.BuildModel()
start = time.time()


for i in range(2, 7):
    for j in range(0, 3):
        for seed in range(101, 111):
            s = SolverMinIns(m, i, j)
            s.solve(seed)
            sol = s.sol
            f = open("final_test_file.txt", "a")
            f.write("\n" + str(sol.max_cost_of_route) + " " + str(i) + " " +str(j) + " " + str(seed))

# s.ReportSolution(sol)
print(sol.max_cost_of_route)

end = time.time()
print((end-start)/60)

f.close()