# utils/file_io.py
#dùng để đọc , lưu file chuyển txt thành object 
from models.driver import Driver
import os 

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

# --- QUẢN LÝ LỊCH SỬ CHUYẾN ĐI (RIDES.TXT) ---
def load_rides(path):
    rides = []
    if not os.path.exists(path): return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            next(f)
            for line in f:
                line = line.strip()
                if not line: continue
                # File rides.txt lưu: RideID, CID, DID, Distance, Fare (5 cột)
                parts = line.split(",")
                if len(parts) >= 5:
                    rides.append(Ride(int(parts[0]), int(parts[1]), int(parts[2]), float(parts[3]), float(parts[4])))
    except Exception as e:
        print(f"Lỗi đọc file rides: {e}")
    return rides

def save_rides(path, rides):
    with open(path, "w", encoding="utf-8") as f:
        f.write("RideID,CustomerID,DriverID,Distance,Fare\n")
        for r in rides:
            f.write(f"{r.ride_id},{r.customer_id},{r.driver_id},{r.distance},{r.fare}\n")

# --- QUẢN LÝ HÀNG ĐỢI TẠM THỜI (REQUESTS.TXT) ---
# Dùng cho Câu 5 và Câu 6 để lưu tạm 6 cột dữ liệu
def save_request_to_file(cid, cname, did, dname, dist, fare):
    path = "data/requests.txt"
    # Kiểm tra xem file có dữ liệu chưa để ghi header
    file_exists = os.path.exists(path) and os.path.getsize(path) > 0
    with open(path, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("CID,CName,DID,DName,Distance,Fare\n")
        f.write(f"{cid},{cname},{did},{dname},{dist},{fare}\n")


