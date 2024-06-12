
import json

from typing import Union




OVERLAP = 'overlap'
DIFFERENCE = 'difference'
MAX_BATCH = 25
RADIUS = 2



def get_center_locations_for_item(item: str):
    # get the center location for the item
    center_location_x: dict[str, list[str]] = {}
    with open('dummyData/center_location_x.json') as f:
        center_location_x = json.load(f)

    items_locations: list[str] = []
    for loc in center_location_x:
        if item in center_location_x[loc]:
            items_locations.append(loc)

    return items_locations
        

# def get_orders_location(location_to_pick: list[int], orders_dict_x: dict[str, list[str]]):
#     # step 1: get all the order and sort by the similarity of the location
#     order_to_location: dict[str, dict[str , int]] = {}
#     # get the overlap and difference of the order with the location
#     for order_key in orders_dict_x:
#         order_items = orders_dict_x[order_key]
#         order_info = {
#             OVERLAP: 0,
#             DIFFERENCE: 0
#         }
#         for item in order_items:
#             item_loc = get_item_best_location_locations(item, location_to_pick)
#             if (item_loc in location_to_pick):
#                 order_info[OVERLAP] += 1
#                 continue
#             order_info[DIFFERENCE] += 1

#         order_to_location[order_key] = order_info
#     return order_to_location


def get_most_similar_order(locations: list[str], orders_dict_x: dict[str, list[str]], selected_orders: list[str]) -> Union[str, None]:
    # get the order with the most overlap
    max_overlap = 0
    max_order = None
    orders_dict_copy = json.loads(json.dumps(orders_dict_x))
    order_diff_over = {}
    for order_key in orders_dict_copy:
        if order_key in selected_orders:
            continue
        order_info = orders_dict_x[order_key]
        order_diff_over[order_key] = {
            OVERLAP: 0,
            DIFFERENCE: 0
        }
        for item in order_info:
            loc = get_item_best_location_locations(item, locations)
            print(type(locations))
            if loc in locations:
                order_diff_over[order_key][OVERLAP] += 1
                continue
            order_diff_over[order_key][DIFFERENCE] += 1
    for order_key in order_diff_over:
        order_info = order_diff_over[order_key]
        if order_info[OVERLAP] > max_overlap:
            max_overlap = order_info[OVERLAP]
            max_order = order_key
    return max_order

def get_order_with_most_locations(orders_dict_x: dict[str, list[str]]):
    # get the order with the most location
    max_location = 0
    max_order = None
    for order_key in orders_dict_x:
        order_info = orders_dict_x[order_key]
        if len(order_info) > max_location:
            max_location = len(order_info)
            max_order = order_key
    return max_order

def get_item_best_location_locations(item: str, locations: list[str], ):
    # get the items location for the order
    centers = get_center_locations_for_item(item)
    if centers == None or len(centers) == 0:
        return None
    for center in centers:
        center_int = int(center)
        for loc in range(center_int - RADIUS, center_int + RADIUS + 1):
            if loc in locations:
                return loc
    return centers[0]


def get_orders_locations( orders_dict_x: dict[str, list[str]] ,order_key: str, locations: list[str],):
    ''' get the orders location for the order
    
    return: order_locations: dict[str, str] (item, location)
    '''
    # get the location for the order
    order_info = orders_dict_x[order_key]
    order_locations: dict[str, str] = {}
    for item in order_info:
        loc = get_item_best_location_locations(item, locations)
        order_locations[item] = loc
    return order_locations



# load the data 
# items_location_x: dict[str, list[int]] = {}
# with open('dummyData/items_location_x.json') as f:
#     items_location_x = json.load(f)

# location_to_item_x: dict[str, list[str]] = {}
# with open('dummyData/location_to_item_x.json') as f:
#     location_to_item_x = json.load(f)

orders_dict_x: dict[str, list[str]] = {}
with open('dummyData/orders_x.json') as f:
    orders_dict_x = json.load(f)

center_location_x: dict[str, list[str]] = {}
with open('dummyData/center_location_x.json') as f:
    center_location = json.load(f)






def create_batch(orders_dict_x: dict[str, list[str]]):
    # select an order to process
    most_used = get_order_with_most_locations(orders_dict_x)
    orders_to_pick: list[str] = [most_used]
    location_to_pick: list[int] = list(get_orders_locations(orders_dict_x, most_used, []).values())
    for i in range(MAX_BATCH):
        order_to_add = get_most_similar_order(location_to_pick, orders_dict_x , orders_to_pick)
        orders_to_pick.append(order_to_add)
        # get the order locations
        t = get_orders_locations(orders_dict_x, order_to_add, location_to_pick).values()
        items_loc_for_order = list(t)
        location_to_pick = list(set(items_loc_for_order + location_to_pick))
        del orders_dict_x[order_to_add]

    print(location_to_pick, location_to_pick)
    return [orders_to_pick, location_to_pick];


def create_full_batches(orders_dict_x: dict[str, list[str]]):
    
    while len(orders_dict_x) > 0:
        orders, locs = create_batch(orders_dict_x)
        print(orders, locs)

create_batch(orders_dict_x)