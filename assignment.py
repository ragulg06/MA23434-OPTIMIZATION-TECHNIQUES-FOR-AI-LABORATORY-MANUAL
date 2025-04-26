from scipy.optimize import linear_sum_assignment

cost_matrix = [
    [4, 1, 3],
    [2, 0, 5],
    [3, 2, 2]
]

row_indices, col_indices = linear_sum_assignment(cost_matrix)

import numpy as np
cost_matrix = np.array(cost_matrix)  # Add this line because you are doing matrix slicing later

total_cost = cost_matrix[row_indices, col_indices].sum()

print("Optimal Assignment:")
for i, worker in enumerate(col_indices):
    print(f"Task {i+1} assigned to Worker {worker+1}")  # spelling corrected

print("Total Cost:", total_cost)
