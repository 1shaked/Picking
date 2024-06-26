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
'''
This is a linear programming problem that will solve the picking issue in a warehouse.
'''

# x_(ipj) = is product i in location p in order j and will be picked [0, 1]
# XL_(ip) = is product i in order p [0, 1] 
# S_(xj) = is order j in batch x [0, 1]
# MAX_BATCH_SIZE = 5
# SL_(xp) = is batch x stopping in location p [0, 1]
# ST_(x) = sum if SL_(xp) is true for all p in P
# MIN sum ST_(x)
# radius = 1

'''
example issue 
location set P = {0 - 10}
XL_(1, 0)  = 1
XL_(1, 3)  = 1

XL_(2, 0)  = 1
XL_(2, 5)  = 1
XL_(2, 8)  = 1

XL_(3, 0)  = 1
XL_(3, 8)  = 1
XL_(3, 10) = 1

XL_(4, 0)  = 1
XL_(4, 10) = 1

order 1 = {1 , 2}
order 2 = {3, 4}
order 3 = {1, 3}
'''


# Initialize the problem
prob = pulp.LpProblem("Warehouse_Picking", pulp.LpMinimize)

# Constants
MAX_BATCH_SIZE = 2
radius = 1
locations = list(range(11))  # P = {0 - 10}
orders = [1, 2, 3, 4]
products = [1 , 2 , 3 , 4]

# Define decision variables
x = pulp.LpVariable.dicts("x", ((i, p, j) for i in products for p in locations for j in orders), cat='Binary')
XL = pulp.LpVariable.dicts("XL", ((i, p) for i in orders for p in locations), cat='Binary')
S = pulp.LpVariable.dicts("S", ((x, j) for x in orders for j in orders), cat='Binary')
SL = pulp.LpVariable.dicts("SL", ((x, p) for x in orders for p in locations), cat='Binary')
ST = pulp.LpVariable.dicts("ST", (x for x in orders), cat='Binary')

# Objective function
prob += pulp.lpSum(ST[x] for x in orders), "Minimize_ST"

# Constraints
# Each product can only be in one location in each order and have to be in one location
for i in products:
    prob += pulp.lpSum(x[i, p, j] for p in locations for j in orders) >= 1 # we can set to == 1
# Batch size constraint
for order_number in orders:
    prob += pulp.lpSum(S[order_number, j] for j in orders) == MAX_BATCH_SIZE



# Example constraints for product locations in orders
prob += XL[1, 0] == 1
prob += XL[1, 3] == 1

prob += XL[2, 0] == 1
prob += XL[2, 5] == 1
prob += XL[2, 8] == 1

prob += XL[3, 0] == 1
prob += XL[3, 8] == 1
prob += XL[3, 10] == 1

prob += XL[4, 0] == 1
prob += XL[4, 10] == 1


# Linking constraints for SL and ST
for order_number in orders:
    for p in locations:
        prob += SL[order_number, p] >= 
        prob += SL[order_number, p] <= pulp.lpSum(x[i, p, j] for i in orders for j in orders)
    prob += ST[order_number] == pulp.lpSum(SL[order_number, p] for p in locations)

# Solve the problem
prob.solve()

# Print the results
print("Status:", pulp.LpStatus[prob.status])

for v in prob.variables():
    if v.varValue == 1:
        print(v.name, "=", v.varValue)

print("Optimal ST value:", pulp.value(prob.objective))