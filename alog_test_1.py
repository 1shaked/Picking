import custom_alog as custom_alog
import pandas as pd
import numpy as np
import json as js
orders_df = pd.read_csv('sim/orders_ids.csv')
products_in_order_df = pd.read_csv('sim/products_in_order.csv')



# choose orders where site id is 168
orders_df = orders_df[orders_df['site_id'] == 168]
# join the products_in_order_df in order_df on the order_id with left join
orders = list(orders_df['order_id'].values)
orders_dict_x: dict[str, list[str]] = {}
for order in orders:
    # get all the products with this id
    temp = products_in_order_df[products_in_order_df['order_id'] == order]
    items = [str(item) for item in list(temp['item_id'].values)]
    orders_dict_x[str(order)] = items


print(products_in_order_df.head())

batches = custom_alog.create_full_batches(orders_dict_x)


print(batches)
