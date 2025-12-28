from utils.distance import euclidean_distance
from utils.display import print_table
import os

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
    
# Trong class MatchingService (MatchingService.py)
    def process_and_show_requests(self):
        req_path = "data/requests.txt"
        try:
            with open(req_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("ℹ️ Hàng đợi trống.")
            return

        if len(lines) <= 1:
            print("ℹ️ Hàng đợi trống.")
            return

        headers = ["STT", "ID Khách", "Tên Khách", "ID Tài xế", "Tên Tài xế", "Quãng Đường", "Thành tiền"]
        
        while True:
            rows = []
            data_to_process = []
            # lines[1:] là bỏ qua header
            for i, line in enumerate(lines[1:], 1):
                p = line.strip().split(",")
                if len(p) < 6: continue
                # p = [cid, cname, did, dname, dist, fare]
                rows.append([i, p[0], p[1], p[2], p[3], f"{float(p[4]):.2f} km", f"{float(p[5]):,.0f} VND"])
                data_to_process.append(p)

            print("\n📋 DANH SÁCH HÀNG ĐỢI HIỆN TẠI:")
            print_table(headers, rows)

            print("\nLựa chọn: [y] Xác nhận tất cả | [d] Xóa một chuyến | [any] Thoát")
            action = input("Chọn: ").lower()

            if action == 'd':
                try:
                    idx = int(input("Nhập STT muốn xóa: "))
                    if 1 <= idx <= len(data_to_process):
                        del lines[idx] # Xóa dòng tương ứng (tính cả header là idx)
                        with open(req_path, "w", encoding="utf-8") as f:
                            f.writelines(lines)
                        print("🗑 Đã xóa yêu cầu.")
                    else: print("❌ STT không tồn tại.")
                except: print("❌ Nhập số hợp lệ.")
            
            elif action == 'y':
                # CHỐT ĐƠN: Ghi vào rides.txt
                self.move_requests_to_history(data_to_process)
                # Xóa sạch requests.txt (chỉ để lại header)
                with open(req_path, "w", encoding="utf-8") as f:
                    f.write("CID,CName,DID,DName,Distance,Fare\n")
                print("✅ Đã lưu tất cả vào lịch sử (rides.txt) và làm trống hàng đợi.")
                break
            else:
                break

    def move_requests_to_history(self, new_data_list):
        
        ride_path = "data/rides.txt"
        old_rides = []

        # Bước 1: Đọc toàn bộ dữ liệu cũ đang có trong file (nếu có)
        if os.path.exists(ride_path) and os.path.getsize(ride_path) > 0:
            with open(ride_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # Bỏ qua header, lấy dữ liệu cũ
                for line in lines[1:]:
                    parts = line.strip().split(",")
                    if len(parts) >= 5:
                        # Lưu lại: [cid, did, dist, fare] (bỏ ID cũ vì lát nữa sẽ đánh số lại)
                        old_rides.append(parts[1:]) 

        # Bước 2: Chuẩn bị danh sách dữ liệu tổng hợp
        # Lấy dữ liệu mới từ hàng đợi (chỉ lấy cid, did, dist, fare)
        processed_new_data = [[item[0], item[2], item[4], item[5]] for item in new_data_list]
        
        # Đảo ngược danh sách mới để cái nhập sau cùng lên đầu (nếu nhập nhiều cùng lúc)
        processed_new_data.reverse()

        # CHÈN LÊN ĐẦU: Kết hợp [Dữ liệu mới] + [Dữ liệu cũ]
        final_data = processed_new_data + old_rides

        # Bước 3: Ghi đè lại toàn bộ file với ID được đánh số lại từ 1
        with open(ride_path, "w", encoding="utf-8") as f:
            f.write("RideID,CustomerID,DriverID,Distance,Fare\n")
            
            for index, item in enumerate(final_data, 1):
                # index chính là RideID (bắt đầu từ 1, 2, 3...)
                # item là [cid, did, dist, fare]
                f.write(f"{index},{item[0]},{item[1]},{item[2]},{item[3]}\n")







                


