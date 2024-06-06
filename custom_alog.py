'''

items_location = {
    item_id: (x, y),
    ...
}

location_to_items = {

    (x, y): [ item_id, ... ],
}

order = [item_id, ...]

orders_dict = {
    order_id_${num}: [
        item_id,
    ],
}
'''
import json

OVERLAP = 'overlap'
DIFFERENCE = 'difference'

# load the data 
items_location_x: dict[str, list[int]] = {}
with open('dummyData/items_location_x.json') as f:
    items_location_x = json.load(f)

location_to_item_x: dict[str, list[str]] = {}
with open('dummyData/location_to_item_x.json') as f:
    location_to_item_x = json.load(f)

orders_dict_x: dict[str, list[str]] = {}
with open('dummyData/orders_x.json') as f:
    orders_dict_x = json.load(f)


print('items_location_x:', items_location_x)
print('location_to_item_x:', location_to_item_x)
print('orders_dict_x:', orders_dict_x)

# select an order to process
orders_to_pick: list[str] = ["order_id_15"]
location_to_pick: list[int] = [9]


# step 1: get all the order and sort by the similarity of the location
order_to_location: dict[str, dict[str , int]] = {}
# get the overlap and difference of the order with the location
for order_key in orders_dict_x:
    order_items = orders_dict_x[order_key]


    order_info = {
        OVERLAP: 0,
        DIFFERENCE: 0
    }

    for item in order_items:
        # for each item we will check if it is already in the location
        item_loc = items_location_x[item]
        # is any of the item in the location_to_pick
        for loc in location_to_pick:
            if loc in item_loc:
                order_info[OVERLAP] += 1
                break
            order_info[OVERLAP] += 1
            
    order_to_location[order_key] = order_info


print('order_to_location:', order_to_location)