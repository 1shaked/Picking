import custom_alog as custom_alog
import pandas as pd

orders_df = pd.read_csv('sim/orders_ids.csv')
products_in_order_df = pd.read_csv('sim/products_in_order.csv')

products_locations = pd.read_excel('sim/products.xlsx')


print(orders_df.head())
print(products_in_order_df.head())
print(products_locations.head())
