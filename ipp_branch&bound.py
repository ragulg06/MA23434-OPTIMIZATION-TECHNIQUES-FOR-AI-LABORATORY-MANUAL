import numpy as np
from scipy.optimize import linprog
from queue import Queue

# Function to solve the linear programming relaxation
def solve_lp(c, A, b, bounds):
    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
    return res

# Branch and Bound method
def branch_and_bound(c, A, b, bounds):
    Q = Queue()
    Q.put((c, A, b, bounds))
    best_solution = None
    best_value = float('-inf')
    
    while not Q.empty():
        current_problem = Q.get()
        res = solve_lp(*current_problem)
        
        if res.success and -res.fun > best_value:
            solution = res.x
            if all(np.isclose(solution, np.round(solution))):
                # If all variables are (almost) integers
                value = -res.fun  # Objective function value
                if value > best_value:
                    best_value = value
                    best_solution = solution
            else:
                # Branching: create two new problems
                for i in range(len(solution)):
                    if not np.isclose(solution[i], np.round(solution[i])):
                        lower_bound = current_problem[3].copy()
                        upper_bound = current_problem[3].copy()
                        
                        # For the lower branch: x_i <= floor(solution[i])
                        lower_bound[i] = (lower_bound[i][0], np.floor(solution[i]))
                        Q.put((current_problem[0], current_problem[1], current_problem[2], lower_bound))
                        
                        # For the upper branch: x_i >= ceil(solution[i])
                        upper_bound[i] = (np.ceil(solution[i]), upper_bound[i][1])
                        Q.put((current_problem[0], current_problem[1], current_problem[2], upper_bound))
                        break  # Only branch on one variable at a time

    return best_solution, best_value

# Example usage
c = [-4, -3]  # Coefficients for the objective function (maximize 4x + 3y)
A = [[2, 1], [1, 2]]  # Coefficients for the constraints
b = [8, 6]  # Right-hand side values for the constraints
bounds = [(0, None), (0, None)]  # x >= 0, y >= 0

# Solve the integer programming problem
solution, value = branch_and_bound(c, A, b, bounds)

print(f"Optimal solution: {solution}")
print(f"Optimal value: {value}")
