from models.ride import Ride
from utils.file_io import load_rides, save_rides
from utils.distance import euclidean_distance
from structures.stack import Stack
from config import RIDES_FILE
from utils.display import print_table

FARE_PER_KM = 12000 # Định nghĩa một hằng số cho giá cước mỗi kilomet là 12,000 VNĐ


class RideService:
    def __init__(self):
        # Load lịch sử chuyến đi từ file
        self.rides = load_rides(RIDES_FILE)

        # Stack phục vụ undo
        self.undo_stack = Stack()  # Khởi tạo một cấu trúc dữ liệu Stack (Ngăn xếp - LIFO) để lưu trữ các hành động gần đây

    # =========================
    # 1. HIỂN THỊ CHUYẾN ĐI THEO TÀI XẾ
    # =========================
    def get_rides_by_driver(self,driver_id):
        rides = load_rides(RIDES_FILE)
        result = [r for r in rides if r.driver_id == driver_id]
        result.sort(key=lambda r: r.ride_id)  # theo thời gian

        
        return result

    # =========================
    # 2. ĐẶT XE (CHƯA LƯU)
    # =========================
    def book_ride(self, customer, driver, trip_distance):
        pickup_distance = euclidean_distance(  # Sử dụng hàm euclidean_distance để tính quãng đường từ vị trí khách hàng đến vị trí tài xế (quãng đường đón khách).
            customer.x, customer.y,
            driver.x, driver.y
        )

        total_distance = round((pickup_distance + trip_distance),3) # Cộng quãng đường đón khách với quãng đường di chuyển thực tế của chuyến đi (trip_distance).
        fare = int(total_distance * FARE_PER_KM)   # Tính tiền: Nhân tổng quãng đường với đơn giá FARE_PER_KM.

        ride_id = len(self.rides) + 1

        ride = Ride(
            ride_id=ride_id,
            customer_id=customer.id,
            driver_id=driver.id,
            distance=total_distance,
            fare=fare
        )
        return ride

    # =========================
    # 3. XÁC NHẬN CHUYẾN ĐI
    # =========================
    def confirm_ride(self, ride):
        # 1. Chèn chuyến đi mới vào đầu danh sách (vị trí index 0)
        self.rides.insert(0, ride)
        
        # 2. Cập nhật lại toàn bộ ride_id theo thứ tự từ mới nhất đến cũ nhất
        # Chuyến đầu tiên (mới nhất) sẽ là 1, tiếp theo là 2, 3...
        for index, r in enumerate(self.rides):
            r.ride_id = index + 1
            
        # 3. Đưa vào stack để phục vụ Undo (nếu cần)
        self.undo_stack.push(ride)

    # =========================
    # 4. HỦY CHUYẾN (CHƯA LƯU)
    # =========================
    def cancel_ride(self):
        return "Ride cancelled"

    # =========================
    # 5. UNDO
    # =========================
    def undo_last_action(self):
        ride = self.undo_stack.pop()
        if ride and ride in self.rides:
            self.rides.remove(ride)
            
            # QUAN TRỌNG: Sau khi Undo (xóa), phải đánh lại ID từ 1 đến N
            # để đảm bảo tính liên tục của danh sách
            for index, r in enumerate(self.rides):
                r.ride_id = index + 1
            return True
        return False

    # =========================
    # 6. LƯU FILE
    # =========================
    


    def show_rides(self, rides):
        headers = ["RideID", "CustomerID", "DriverID", "Distance(km)", "Fare(VND)"]
        rows = [
            [r.ride_id, r.customer_id, r.driver_id, r.distance, format(r.fare*1000, ",.0f")]
            for r in rides
        ]
        print_table(headers, rows)


    def save(self):
            """Lưu toàn bộ danh sách chuyến đi hiện có trong RAM vào file txt."""
            # Gọi hàm save_rides từ utils/file_io.py (Cách khuyên dùng)
            save_rides(RIDES_FILE, self.rides)
            
            # Hoặc nếu bạn muốn in xác nhận ngay tại đây để kiểm tra:
            print(f"📂 Đã ghi {len(self.rides)} chuyến đi vào {RIDES_FILE}")

    