

orders = {
    # order number : { items: [
    #    {
    #item: 'item name', quantity: 1, location , 
          # },
    #    ], 
    #}
}

max_batch_size = 25


start_order = PickRandomOrder(orders) # this also delete the order from the orders list

batches = []
while len(orders) !== 0:
    locations = getLocations(batches[-1])
    while batches[-1].size <= max_batch_size:
        similar_orders = getMostSimilarOrdersFromLocatio(locations, orders)
        batches[-1].addOrder(similar_orders[0])
        PickOrder(similar_orders[0])
