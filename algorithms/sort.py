# algorithms/sort.py

def quick_sort_drivers_by_id(drivers, reverse=False):
    """
    Sắp xếp tài xế theo ID sử dụng thuật toán Quick Sort.
    Độ phức tạp: O(n log n).
    """
    if len(drivers) <= 1:
        return drivers

    # Chọn pivot là phần tử giữa để tối ưu trường hợp dữ liệu đã gần sắp xếp
    pivot_obj = drivers[len(drivers) // 2]
    pivot_id = pivot_obj.id

    if not reverse:
        left = [d for d in drivers if d.id < pivot_id]
        middle = [d for d in drivers if d.id == pivot_id]
        right = [d for d in drivers if d.id > pivot_id]
    else:
        # Nếu reverse=True, đảo ngược logic so sánh
        left = [d for d in drivers if d.id > pivot_id]
        middle = [d for d in drivers if d.id == pivot_id]
        right = [d for d in drivers if d.id < pivot_id]

    return quick_sort_drivers_by_id(left, reverse) + middle + quick_sort_drivers_by_id(right, reverse)

def radix_sort_drivers_by_rating(drivers):
    if not drivers:
        return drivers

    # Bước 1: chuẩn hóa rating float -> int
    for d in drivers:
        d._rating_key = int(d.rating * 10)

    max_val = max(d._rating_key for d in drivers)
    exp = 1

    while max_val // exp > 0:
        buckets = [[] for _ in range(10)]

        for d in drivers:
            digit = (d._rating_key // exp) % 10
            buckets[digit].append(d)

        drivers = []
        for b in buckets:
            drivers.extend(b)

        exp *= 10

    # Bước 2: đảo ngược để GIẢM DẦN
    drivers.reverse()

    # Bước 3: dọn key phụ
    for d in drivers:
        del d._rating_key

    return drivers





def quick_sort_customers_by_id(customers):
    if len(customers) <= 1:
        return customers

    pivot = customers[len(customers) // 2].id
    left = [c for c in customers if c.id < pivot]
    middle = [c for c in customers if c.id == pivot]
    right = [c for c in customers if c.id > pivot]

    return quick_sort_customers_by_id(left) + middle + quick_sort_customers_by_id(right)





