from Solver import *
from VRP_Model import *
import pprint
m = Model()
m.BuildModel()
# routes=m.load_objects()
# print(m.CalculateMaxCostOfRoute(routes,m.time_matrix))

s = Solver(m)
s.check_zach_example()
sol = s.solve()
