# algorithms/search.py
def binary_search_driver_by_id(drivers, driver_id):
    left, right= 0, len(drivers)-1
    while left <= right:
        mid = (left+right)//2
        if drivers[mid].id == driver_id:
            return drivers[mid]
        elif drivers[mid].id < driver_id:
            left = mid+1
        else:
            right = mid -1
    return None

def linear_search_driver_by_name(drivers, name):
    return [d for d in drivers if name.lower() in d.name.lower()]


# algorithms/search.py
def binary_search_customer_by_id(customers, cid):
    left, right= 0, len(customers)-1
    while left <= right:
        mid = (left+right)//2
        if customers[mid].id == cid:
            return customers[mid]
        elif customers[mid].id < cid:
            left = mid+1
        else:
            right = mid -1
    return None

def linear_search_customer_by_name(customers, name):
    return [c for c in customers if name.lower() in c.name.lower()]
