
import custom_alog as ca
import math
import json

def generate_order_matrix( orders_dict_x: dict[str, list[str]] ,):
    '''
    this will generate two matrixes,
    one with the overlap and the other with the difference 
    and return them
    '''
    # create the matrix
    order_matrix_overlap = dict()
    order_matrix_difference = dict()
    
    for order_key in orders_dict_x:
        order_matrix_overlap[order_key] = {}
        order_matrix_difference[order_key] = {}
        for order_key2 in orders_dict_x:
            if order_key == order_key2:
                continue
            order_matrix_overlap[order_key][order_key2] = 0
            order_matrix_difference[order_key][order_key2] = 0

        
class Batch:
    '''
    The Batch is the object that will hold the orders that will be picked
    '''
    locations : list[int]= []
    orders    : list[str]= []
    def __init__(self):
        self.locations = []
        self.orders = []



orders_dict_x: dict[str, list[str]] = {}
with open('sim/orders_x.json') as f:
    orders_dict_x = json.load(f)
# generate bins 
total_bins: int = math.ceil(len(orders_dict_x.keys()) / ca.MAX_BATCH)

# generate the bins array
bins = [Batch() for _ in range(total_bins)]


def init_bins(orders_dict_x: dict[str, list[str]], bins: list[Batch]):
    '''
    This will init the bins with the orders

    TODO: add a check to not add order that is contained in another order
    '''
    for bin_object in bins:
        # find the most used order
        most_used, score_init = ca.get_order_with_most_locations(orders_dict_x)
        if most_used == None:
            break
        # add the order to the bin
        bin_object.orders.append(most_used)
        # get the locations for the order
        locations = ca.get_orders_locations(orders_dict_x, most_used, [])
        bin_object.locations = locations
        del orders_dict_x[most_used]



init_bins(orders_dict_x, bins)

bin_index: int | None = None
score: float = -1_000_000
order: str | None = None
for index , bin_object in enumerate(bins):
    
    for order in bin_object.orders:
        print(order)
        order_most_similar , score_similar = ca.get_most_similar_order(bin_object.locations, orders_dict_x, bin_object.orders)
        # we will check the similarity of the orders in the bin
        if score == None or bin_index == None or order == None:
            order = order_most_similar
            bin_index = index
            score = score_similar
            continue
    print(order, score, bin_index)