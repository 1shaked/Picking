import pandas as pd
import numpy as np
import json as js
products_locations = pd.read_excel('sim/products.xlsx')

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
