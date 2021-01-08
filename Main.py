from Solver import *
from VRP_Model import *
from paperSolution import *
import pprint


m = Model()
m.BuildModel()
s=Solver(m)
s.solve()
# routes=m.load_objects()
# print(m.CalculateMaxCostOfRoute(routes,m.time_matrix))

