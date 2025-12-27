from utils.distance import euclidean_distance
from utils.display import print_table

class MatchingService:
    def __init__(self, driver_service, customer_service, ride_service):
        self.driver_service = driver_service
        self.customer_service = customer_service
        self.ride_service = ride_service

    

    def find_nearby_drivers(self, customer_id, radius,min_dist):
        customer = self.customer_service.get_by_id(customer_id)
        if not customer:
            return []

        result = []
        
        for d in self.driver_service.drivers:
            dist = euclidean_distance(customer.x, customer.y, d.x, d.y)
            if dist < min_dist[0]:
                min_dist[0] = dist
            if dist <= radius:
                result.append((d, dist))

        result.sort(key=lambda x: (x[1], -x[0].rating))
        return result

    
    def auto_match_driver(self, customer_id, radius):
        drivers = self.find_nearby_drivers(customer_id, radius)
        if not drivers:
            return None
        return drivers[0][0]  # tài xế gần nhất
    



    def process_and_show_requests(self):
        try:
            with open("data/requests.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("❌ Không tìm thấy file data/requests.txt")
            return

        # CHỈNH 1: Kiểm tra nếu file chỉ có header hoặc trống
        if not lines or len(lines) <= 1:
            print("ℹ️ Danh sách yêu cầu trống.")
            return

        headers = ["ID Khách", "Tên Khách", "ID Tài xế", "Tên Tài xế", "Quãng Đường", "Thành tiền","Tiền tiết kiệm"]
        rows = []
        temp_rides = []

        for line in lines[1:]:
            if not line.strip(): continue
            # Tách dữ liệu từ file requests.txt
            parts = line.strip().split(",")
            cid = int(parts[0])
            chosen_did = int(float(parts[1])) # ID tài xế khách tự chọn ở Câu 5
            trip_dist = float(parts[2])
            
            customer = self.customer_service.get_by_id(cid)
            chosen_driver = self.driver_service.get_by_id(chosen_did) # Tài xế câu 5
            if not customer or not chosen_driver: continue

            # 1. Tính giá tiền Câu 5 (Tài xế tự chọn)
            ride_câu_5 = self.ride_service.book_ride(customer, chosen_driver, trip_dist)
            fare_câu_5 = ride_câu_5.fare

            # Logic tìm tài xế gần nhất tuyệt đối
            best_driver = None
            min_dist = float('inf')
            
            for d in self.driver_service.drivers:
                d_dist = euclidean_distance(customer.x, customer.y, d.x, d.y)
                if d_dist < min_dist:
                    min_dist = d_dist
                    best_driver = d

            if best_driver:
                # Tạo chuyến đi (đã làm tròn 3 chữ số trong ride_service)
                ride_câu_6 = self.ride_service.book_ride(customer, best_driver, trip_dist)
                fare_câu_6 = ride_câu_6.fare
                
                # 4. TIỀN HIỆU SUẤT = Chênh lệch giá do đi đón gần hơn
                # Nếu chọn đúng người gần nhất thì tiền này = 0
                efficiency_gain = fare_câu_5 - fare_câu_6

        
                rows.append([
                    customer.id, customer.name,
                    best_driver.id, best_driver.name,
                    f"{ride_câu_6.distance:.3f} km", 
                    f"{ride_câu_6.fare:,} VND",
                    f"{efficiency_gain:,} VND" # Số tiền tiết kiệm được
                ])
                temp_rides.append(ride_câu_6)

        if rows:
            print_table(headers, rows)
            
            confirm = input("\nXác nhận TẤT CẢ chuyến đi trên? (y/n): ")
            if confirm.lower() == 'y':
                for r in temp_rides:
                    self.ride_service.confirm_ride(r)
                    convert_requests_to_rides()
                # Xóa sạch file yêu cầu sau khi đã xử lý xong
                with open("data/requests.txt", "w", encoding="utf-8") as f:
                    f.write("CustomerID,DriverID,Distance\n")
                print("✅ Đã hoàn tất xử lý.")

            confirm = input("Có muốn hủy chuyến nào không? (y/n): ")
            if confirm.lower() == 'y':
                n = int(input("vui lòng nhập thứ tự chuyến muốn hủy bắt đầu từ 1: "))
                if n <= len(rows) and n >0:
                    del lines[n]
                    print("đã hủy chuyến đi")
                    with open("data/requests.txt", "w", encoding="utf-8") as f:
                        f.writelines(lines)
                    

                else:
                    print("vui lòng nhập đúng thứ tự!!")


import os

def convert_requests_to_rides(
    request_file="data/requests.txt",
    rides_file="data/rides.txt",
    price_per_km=10
):
    file_exists = os.path.exists(rides_file)
    ride_id = 1

    # Nếu file đã tồn tại và không rỗng → tính ride_id tiếp theo
    if file_exists and os.path.getsize(rides_file) > 0:
        with open(rides_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            ride_id = len(lines)  # đã có header → dòng cuối +1

    with open(request_file, "r", encoding="utf-8") as f:
        request_lines = f.readlines()[1:]  # bỏ header

    with open(rides_file, "a", encoding="utf-8", newline="") as f:
        # Chỉ ghi header nếu file chưa tồn tại hoặc rỗng
        if not file_exists or os.path.getsize(rides_file) == 0:
            f.write("RideID,CustomerID,DriverID,Distance,Fare\n")

        for line in request_lines:
            customer_id, driver_id, distance = line.strip().split(",")
            distance = float(distance)
            fare = distance * price_per_km

            f.write(f"{ride_id},{customer_id},{driver_id},{distance},{fare}\n")
            ride_id += 1






                


