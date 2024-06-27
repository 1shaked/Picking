import custom_alog as custom_alog
import pandas as pd
import numpy as np
import json as js
orders_df = pd.read_csv('sim/orders_ids.csv')
products_in_order_df = pd.read_csv('sim/products_in_order.csv')

products_locations = pd.read_excel('sim/products.xlsx')


# choose orders where site id is 168
orders_df = orders_df[orders_df['site_id'] == 168]
# join the products_in_order_df in order_df on the order_id with left join
orders = list(orders_df['order_id'].values)
orders_dict_x: dict[str, list[str]] = {}
for order in orders:
    # get all the products with this id
    temp = products_in_order_df[products_in_order_df['order_id'] == order]
    items = list(temp['item_id'].values)
    orders_dict_x[order] = items


# Convert the 'Itur' column to numeric, forcing errors to NaN (you can handle them as needed)
products_locations['IturAsNumber'] = pd.to_numeric(products_locations['Itur'], errors='coerce')

# Now perform the division and rounding
products_locations['location'] = (products_locations['IturAsNumber'] / 5).round()

locations: dict[str, list[str]] = {}
locations_unique = products_locations['location'].unique()
for location in locations_unique:
    # check if is nan
    
    if np.isnan(location) or location == None:
        continue
    # get all products in this location
    temp = products_locations[products_locations['location'] == location]
    items = list(temp['item_id'].unique())
    print(items)
    locations[str(int(location))] = [str(item) for item in items]

with open('sim/center_locations.json', 'w') as f:
    f.write(js.dumps(
        locations,
        indent=2
    ))


print(products_in_order_df.head())

batches = custom_alog.create_full_batches(orders_dict_x)


'''
# how many stops do we have per  (unique product / stops_number)
# how many stops do we have per  (unique product / order_size)
# 

'''
