import json
import pulp

MAX_BATCH_SIZE = 5

orders_dict_x: dict[str, list[str]] = {}
with open('dummyData/orders_x.json') as f:
    orders_dict_x = json.load(f)

center_location_x: dict[str, list[str]] = {}
with open('dummyData/center_location_x.json') as f:
    center_location = json.load(f)


print(orders_dict_x, center_location_x)


def create_batch_from_orders(orders_dict_x: dict[str, list[str]]):
    pass

# 

# Create a LP maximization problem
lp_problem = pulp.LpProblem("Maximize Z", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable("x", lowBound=0)  # x >= 0
y = pulp.LpVariable("y", lowBound=0)  # y >= 0

# Objective function
lp_problem += 3 * x + 2 * y, "Z"

# Constraints
lp_problem += x + y <= 4, "Constraint 1"
lp_problem += x <= 2, "Constraint 2"
lp_problem += y <= 3, "Constraint 3"

# Solve the problem
lp_problem.solve()

# Print the results
print(f"Status: {pulp.LpStatus[lp_problem.status]}")
print(f"x = {pulp.value(x)}")
print(f"y = {pulp.value(y)}")
print(f"Objective = {pulp.value(lp_problem.objective)}")