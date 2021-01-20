from VRPMinimumInsertions_final import *
import time

m = Model()
m.BuildModel()
start = time.time()


for i in range(8, 32):
    for j in range(1, 8):
        for seed in range(101, 111):
            s = SolverMinIns(m, i/4, j/4)
            s.solve(seed)
            sol = s.sol
            print("hi")
            f = open("final_test_file.txt", "a")
            f.write("\n" + str(sol.max_cost_of_route) + " " + str(i) + " " +str(j) + " " + str(seed))

# s.ReportSolution(sol)
print(sol.max_cost_of_route)

end = time.time()
print((end-start)/60)

f.close()