# utils/file_io.py
#dùng để đọc , lưu file chuyển txt thành object 
from models.driver import Driver

def load_drivers(file_path):
    drivers = []
    with open(file_path, "r", encoding="utf-8") as f:
        next(f) # <--- CHÈN DÒNG NÀY (Bỏ qua dòng tiêu đề)
        for line in f:
            id, name, rating, x, y = line.strip().split(",")
            drivers.append(
                Driver(int(id), name, float(rating), float(x), float(y))
            )
    return drivers

def save_drivers(file_path, drivers):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("ID,Name,Rating,x,y\n") # <--- CHÈN DÒNG NÀY
        for d in drivers:
            f.write(f"{d.id},{d.name},{d.rating},{d.x},{d.y}\n")


# utils/file_io.py
from models.customer import Customer

def load_customers(file_path):
    import os
    from models.customer import Customer
    if not os.path.exists(file_path): return []
    customers = []
    with open(file_path, "r", encoding="utf-8") as f:
        next(f) # <--- CHÈN DÒNG NÀY
        for line in f:
            id, name, district, x, y = line.strip().split(",")
            customers.append(Customer(int(id), name, district, float(x), float(y)))
    return customers

def save_customers(file_path, customers):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("ID,Name,District,x,y\n") # <--- CHÈN DÒNG NÀY
        for c in customers:
            f.write(f"{c.id},{c.name},{c.district},{c.x},{c.y}\n")




from models.ride import Ride

def load_rides(path):
    rides = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            next(f)  # Bỏ qua header
            for line_num, line in enumerate(f, start=2):  # start=2 vì đã bỏ header
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # Tách dòng và chỉ lấy 5 phần tử đầu
                    parts = line.split(",")
                    if len(parts) < 5:
                        print(f"Lỗi dòng {line_num}: Thiếu dữ liệu - {line}")
                        continue
                    
                    # Chỉ lấy 5 phần tử đầu, bỏ phần thừa
                    ride_id, cid, did, dist, fare = parts[:5]
                    
                    rides.append(
                        Ride(
                            int(ride_id.strip()),
                            int(cid.strip()),
                            int(did.strip()),
                            float(dist.strip()),
                            float(fare.strip())
                        )
                    )
                except (ValueError, IndexError) as e:
                    print(f"Lỗi xử lý dòng {line_num}: {line}")
                    print(f"Chi tiết lỗi: {e}")
                    continue
                    
    except FileNotFoundError:
        print(f"File {path} không tồn tại. Tạo danh sách rides trống.")
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
    
    return rides

def save_rides(path, rides):
    with open(path, "w", encoding="utf-8") as f:
        f.write("RideID,CustomerID,DriverID,Distance,Fare\n") # <--- CHÈN DÒNG NÀY
        for r in rides:
            f.write(f"{r.ride_id},{r.customer_id},{r.driver_id},{r.distance},{r.fare}\n")


