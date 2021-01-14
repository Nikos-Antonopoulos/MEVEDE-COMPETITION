import pprint
from paperSolution import * 
m = Model()
m.BuildModel()
best = 100

s = Solverpaper(m)
sol = s.solve(7)

