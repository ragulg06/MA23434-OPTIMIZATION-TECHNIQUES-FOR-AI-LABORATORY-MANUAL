import numpy as np
from scipy.optimize import linprog

cost = np.array([
    [4,8,8],
    [2,7,6],
    [3,4,2]
])

c = cost.flatten()
supply = np.array([50, 40, 60])

demand = np.array([30, 70, 50])

A_eq = [] 
b_eq = []

for i in range(len(supply)):
    constraint = [0] * len(c)
    for j in range(len(demand)):
        constraint[i * len(demand) + j] = 1
    A_eq.append(constraint)
    b_eq.append(supply[i])

for j in range(len(demand)):
    constraint = [0] * len(c)
    for i in range(len(supply)):
        constraint[i * len(demand) + j] = 1
    A_eq.append(constraint)
    b_eq.append(demand[j])

result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method = "highs")

result_matrix = result.x.reshape(len(supply), len(demand))

print("Optimal value:", result.fun)
print("Optimal solution matrix:\n", result_matrix)
