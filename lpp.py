import numpy as np
from scipy.optimize import linprog

c =[-3, -2]

A = [
    [2,1],
    [4,-5]
]

b = [20, 10]

x_bounds = (0, None)
y_bounds = (0, None)

result = linprog(c, A_ub =A, b_ub=b, bounds=[x_bounds, y_bounds], method = "highs")

print('Optimal value:', -result.fun)
print('Values of x:', result.x)