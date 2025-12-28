# main.py
from services.driver_service import DriverService
from services.customer_service import CustomerService
from services.ride_service import RideService
from services.matching_service import MatchingService

from models.driver import Driver
from models.customer import Customer

from structures.queue import Queue
from utils.file_io import save_request_to_file
from utils.display import print_table
from utils.visualize import plot_customers_and_drivers 


# ================= MENU CHÍNH =================
def main_menu():
    print("\n╔" + "═" * 38 + "╗")
    print("║        🚗  MINRIDE SYSTEM  🚗        ║")
    print("╠" + "═" * 38 + "╣")
    print("║  1. 👷 Quản lý tài xế                ║")
    print("║  2. 👥 Quản lý khách hàng            ║")
    print("║  3. 📑 Quản lý chuyến đi             ║")
    print("║  4. 🔍 Tìm tài xế phù hợp            ║")
    print("║  5. 🎫 Đặt xe ngay                   ║")
    print("║  6. 🤖 Tự động ghép cặp (Auto)       ║")
    print("║  7. ⏳  Hiển thị hàng đợi khách hàng ║")
    print("║  8. 🗺️  Xem bản đồ hệ thống           ║")
    print("║  0. ❌ Thoát ứng dụng                ║")
    print("╚" + "═" * 38 + "╝")
    print("👉 Vui lòng chọn chức năng: ", end="")

# ================= CÁC MENU CON =================
# ================= QUẢN LÝ TÀI XẾ =================
def driver_menu():    
    print("\n┌" + "─" * 30 + "┐")
    print("│     👷 QUẢN LÝ TÀI XẾ        │")
    print("├" + "─" * 30 + "┤")
    print("│ 1. 📋 Danh sách tài xế       │")
    print("│ 2. ➕ Thêm tài xế mới        │")
    print("│ 3. 📝 Cập nhật thông tin     │")
    print("│ 4. 🗑️  Xóa tài xế             │")
    print("│ 5. 🔎 Tìm kiếm (ID/Tên)      │")
    print("│ 6. 📈 Sắp xếp theo Rating    │")
    print("│ 7. 🏆 Hiển thị Top K         │")
    print("│ 8. ↩️  Hoàn tác thao tác      │") 
    print("│ 0. 🔙 Quay lại               │")
    print("└" + "─" * 30 + "┘")

def driver_menu_loop(driver_service):
    while True:
        driver_menu()
        choice = input("Chọn chức năng: ").strip()
        if choice == "1":
            driver_service.show_all()
        elif choice == "2":
            while True:
                id_input = input("ID (Để trống để tự động lấy ID tiếp theo): ").strip()
                if id_input == "".strip():
                    driver_id = driver_service.get_next_id()
                    print(f"➡️ ID tự động được cấp: {driver_id}")
                    break
                else:
                    if id_input.isdigit():
                        driver_id = int(id_input)
                        if driver_service.exists(driver_id):
                            print("❌ ID đã tồn tại!")
                            continue
                        break
                    print("❌ ID phải là số hoặc để trống!")
            
            # --- Nhập Tên (Chuẩn hóa) ---
            while True:
                name_input = input("Tên: ").strip()
                # Thu hẹp khoảng trắng: "  Cường  " -> "Cường"
                # "Lê    Cường" -> "Lê Cường"
                name = " ".join(name_input.split())
                
                if not name:
                    print("❌ Tên không được để trống!")
            # Kiểm tra nếu chuỗi chỉ toàn số (ví dụ: "123")
                elif name.isdigit():
                    print("❌ Tên không được chỉ chứa chữ số!")
                # Kiểm tra nâng cao: Tên không được chứa bất kỳ chữ số nào (ví dụ: "Cường123")
                elif any(char.isdigit() for char in name):
                    print("❌ Tên không được chứa chữ số!")
                else:
                    break
                    

            while True:
                try:
                    rating = float(input("Rating (0-5): "))
                    if 0 < rating <= 5: break
                    else: print("❌ Rating không hợp lệ!")
                except ValueError: print("❌ Rating phải là số!")
            
            # --- Nhập Tọa độ X (Bắt nhập lại nếu sai) ---
            while True:
                try:
                    x = float(input("Nhập tọa độ x: "))
                    break
                except ValueError:
                    print("❌ Tọa độ x phải là số!")

            # --- Nhập Tọa độ Y (Bắt nhập lại nếu sai) ---
            while True:
                try:
                    y = float(input("Nhập tọa độ y: "))
                    break
                except ValueError:
                    print("❌ Tọa độ y phải là số!")


            driver_service.add_driver(Driver(driver_id, name, round(rating,2), x, y))
            print("✔ Đã thêm tài xế")
        
        elif choice == "3":
            key_input = input("Nhập tên tài xế hoặc ID cần cập nhật: ").strip()
            # Chuẩn hóa đầu vào để tìm kiếm chính xác hơn
            search_key = " ".join(key_input.split())
            if not search_key:
                print("❌ Vui lòng không để trống!")
                continue
                
            drivers = driver_service.search_driver(search_key)
            
            # --- Bước 1: Xác định tài xế cần cập nhật ---
            target_driver = None
            if isinstance(drivers, list):
                if not drivers:
                    print("❌ Không tìm thấy tài xế!")
                    continue
                
                print(f"\n🔍 Tìm thấy {len(drivers)} tài xế khớp với '{search_key}':")
                headers = ["ID", "Tên Tài Xế", "Rating Hiện Tại", "Tọa độ (X, Y)"]
                rows = [[d.id, d.name, d.rating, f"({d.x}, {d.y})"] for d in drivers]
                print_table(headers, rows)
                # sau khi đã hiển thị các tài xế trùng id 
                
                try:
                    update_id = int(input("👉 Nhập ID chính xác của tài xế cần cập nhật: "))
                    # Tìm đối tượng driver có ID vừa nhập trong danh sách kết quả
                    target_driver = next((d for d in drivers if d.id == update_id), None)
                    if not target_driver:
                        print("❌ ID bạn nhập không nằm trong danh sách tìm thấy!")
                        continue
                except ValueError:
                    print("❌ ID phải là số!")
                    continue
            elif drivers:
                target_driver = drivers
            else:
                print("❌ Không tìm thấy tài xế!")
                continue

            # --- Bước 2: Nhập thông tin mới ---
            print(f"\n🛠 Đang cập nhật cho tài xế: {target_driver.name} (ID: {target_driver.id})")
            while True:
                try:
                    new_rating = float(input("Rating mới (0-5): "))
                    if not (0 <= new_rating <= 5):
                        print("❌ Rating phải từ 0 đến 5!")
                        continue
                        
                    new_x = float(input("Tọa độ X mới: "))
                    new_y = float(input("Tọa độ Y mới: "))
                    break
                except ValueError:
                    print("❌ Vui lòng nhập số hợp lệ!")

            # --- Bước 3: Thực hiện cập nhật và Hiển thị kết quả ---
            driver_service.update_driver(target_driver.id, round(new_rating, 2), new_x, new_y)
            
            print("\n✅ CẬP NHẬT THÀNH CÔNG!")
            res_headers = ["Thông tin", "Giá trị mới"]
            res_rows = [
                ["ID", target_driver.id],
                ["Tên", target_driver.name],
                ["Rating", round(new_rating, 2)],
                ["Vị trí mới", f"({new_x}, {new_y})"]
            ]
            print_table(res_headers, res_rows)


        elif choice == "4":
            try:
                id = int(input("Nhập ID cần xóa: "))
                if driver_service.exists(id):
                    driver_service.delete_driver_by_id(id)
                    print("✔ Đã xóa")
                else: print("❌ ID không tồn tại!")
            except ValueError: print("❌ ID phải là số!")
        elif choice == "5":
            # --- Nhập và Chuẩn hóa từ khóa tìm kiếm ---
            key_input = input("Nhập ID hoặc Tên: ").strip()
            
            # Xử lý khoảng trắng thừa ở giữa: "   cuong    " -> "cuong"
            # Nếu nhập "le   cuong" -> "le cuong"
            clean_key = " ".join(key_input.split())
            if not clean_key:
                print("❌ Vui lòng không để trống từ khóa tìm kiếm!")
                continue
            # Tự động viết hoa chữ cái đầu nếu người dùng nhập tên thường 
            # "cuong" -> "Cuong", "le cuong" -> "Le Cuong"
            # Điều này giúp khớp với dữ liệu trong hệ thống thường lưu Tên viết hoa
            search_key = clean_key.lower() if not clean_key.isdigit() else clean_key
            print(f"🔍 Đang tìm kiếm với từ khóa: '{search_key}'...")
            result = driver_service.search_driver(search_key)
            
            # Xử lý dữ liệu để in bảng
            drivers_to_print = []
            if isinstance(result, list):
                drivers_to_print = result
            elif result: # Nếu trả về 1 đối tượng đơn lẻ
                drivers_to_print = [result]

            if not drivers_to_print:
                print("❌ Không tìm thấy tài xế!")
            else:
                # 1. Định nghĩa Tiêu đề bảng
                headers = ["ID", "Tên Tài Xế", "Rating", "Tọa độ (X, Y)"]
                
                # 2. Chuyển đổi list đối tượng Driver thành list dữ liệu thô
                rows = []
                for d in drivers_to_print:
                    # Tạo một hàng tương ứng với các cột trong headers
                    rows.append([d.id, d.name, d.rating, f"({d.x}, {d.y})"])
                
                # 3. Gọi hàm in bảng từ display.py
                print(f"\n🔍 Kết quả tìm kiếm cho: '{search_key}'")
                print_table(headers, rows)

        elif choice == "6":
            print("✔ Đã sắp xếp")
            driver_service.show_all(sorted_view=True) 

        elif choice == "7":
            try:
                k = int(input("Nhập số lượng tài xế (K): "))
                pos = input("Nhấn 'C' để xem top thấp nhất, phím khác để xem top cao nhất: ").upper()
                top = False if pos == "C" else True
                
                # Lấy danh sách đối tượng tài xế từ service
                top_drivers = driver_service.show_top_k(k, top)
                
                if not top_drivers:
                    print("ℹ️ Danh sách tài xế trống.")
                else:
                    # Chuẩn bị tiêu đề và dữ liệu cho bảng
                    title = "TOP CAO NHẤT" if top else "TOP THẤP NHẤT"
                    headers = ["ID", "Tên Tài Xế", "Rating", "Tọa độ X", "Tọa độ Y"]
                    
                    # Chuyển đổi list đối tượng Driver thành dữ liệu thô
                    rows = [[d.id, d.name, f"{d.rating} ⭐", d.x, d.y] for d in top_drivers]
                    
                    print(f"\n🏆 BẢNG XẾP HẠNG {k} TÀI XẾ {title}")
                    # Gọi hàm in bảng để hiển thị dữ liệu đẹp mắt
                    print_table(headers, rows)
                    
            except ValueError:
                print("❌ Lỗi: K phải là một số nguyên!")
        elif choice == "8":
            driver_service.undo()
        elif choice == "0":
            
            break




# ================= QUẢN LÝ KHÁCH HÀNG =================
def customer_menu():
    print("\n┌" + "─" * 30 + "┐")
    print("│    👥 QUẢN LÝ KHÁCH HÀNG     │")
    print("├" + "─" * 30 + "┤")
    print("│ 1. 📜 Danh sách khách hàng   │")
    print("│ 2. ➕ Thêm khách hàng mới    │")
    print("│ 3. ✍️  Cập nhật khách hàng    │")
    print("│ 4. 🗑️  Xóa khách hàng         │")
    print("│ 5. 🔎 Tìm kiếm khách hàng    │")
    print("│ 6. 📍 Liệt kê theo Quận      │")
    print("│ 7. ↩️  Hoàn tác thao tác      │") 
    print("│ 0. 🔙 Quay lại menu          │")
    print("└" + "─" * 30 + "┘")
def customer_menu_loop(customer_service):
    while True:
        customer_menu()
        choice = input("Chọn chức năng: ").strip()
        if choice == "1":
            customer_service.show_all()


        elif choice == "2":
            # --- Nhập ID tự động hoặc thủ công ---
            while True:
                id_input = input("ID (Để trống để tự động lấy ID tiếp theo): ").strip()
                if id_input == "":
                    customer_id = customer_service.get_next_id()
                    print(f"➡️ ID tự động được cấp: {customer_id}")
                    break
                else:
                    if id_input.isdigit():
                        customer_id = int(id_input)
                        if customer_service.exists(customer_id):
                            print("❌ ID đã tồn tại!")
                            continue
                        break
                    print("❌ ID phải là số hoặc để trống!")

            # --- Nhập Tên (Chuẩn hóa khoảng trắng) ---
            while True:
                name_input = input("Tên: ").strip()
                name = " ".join(name_input.split()) # Xử lý khoảng trắng thừa
                if name:
                    break
                print("❌ Tên không được để trống!")

            # --- Nhập Quận (Chuẩn hóa định dạng Qx) ---
            while True:
                dist_input = input("Quận hoặc Thành Phố(khu vực HCM) (Ví dụ: Thủ Đức): ").strip().upper()
                # Loại bỏ tất cả khoảng trắng bên trong để "Q    12" -> "Q12"
                
                if dist_input.startswith("Q") and dist_input[1:].isdigit():
                    q_num = int(dist_input[1:])
                    if 1 <= q_num <= 12 and q_num != 9:
                        district = f"Q{q_num}" # Đảm bảo định dạng chuẩn Q1, Q2...
                        break

                dist_input = " ".join(dist_input.split())
                if dist_input in ["THỦ ĐỨC", "BÌNH TÂN", "BÌNH THẠNH", "GÒ VẤP", "PHÚ NHUẬN", "TÂN BÌNH", "TÂN PHÚ"]:
                    district = dist_input
                    break
                print("❌ Lỗi: Quận phải nằm trong thành phố Hồ Chí Minh!")

            # --- Nhập Tọa độ X ---
            while True:
                try:
                    x = float(input("x: "))
                    break
                except ValueError:
                    print("❌ Tọa độ x phải là một số!")

            # --- Nhập Tọa độ Y ---
            while True:
                try:
                    y = float(input("y: "))
                    break
                except ValueError:
                    print("❌ Tọa độ y phải là một số!")
            customer_service.add_customer(Customer(customer_id, name, district, x, y))
            print(f"✔ Đã thêm khách hàng: {name} tại {district}")


        elif choice == "3":
            try:
                # --- Kiểm tra ID ---
                while True:
                    try:
                        id_input = input("Nhập ID cần cập nhật: ").strip()
                        if not id_input: break # Cho phép thoát nếu nhấn Enter trống (tùy chọn)
                        target_id = int(id_input)
                        if not customer_service.exists(target_id):
                            print("❌ Không tìm thấy khách hàng có ID này!")
                            continue
                        break
                    except ValueError: print("❌ ID phải là số nguyên!")

                # --- Nhập Tên mới ---
                while True:
                    name_input = input("Tên mới: ").strip()
                    new_name = " ".join(name_input.split())
                    if new_name: break
                    print("❌ Tên không được để trống!")

                # --- Nhập Quận mới (Q1-Q12) ---
                while True:
                    dist_input = input("Quận hoặc Thành Phố(khu vực HCM) (Ví dụ: Thủ Đức): ").strip().upper()
                    # Loại bỏ tất cả khoảng trắng bên trong để "Q    12" -> "Q12"
                    if dist_input.startswith("Q") and dist_input[1:].isdigit():
                        q_num = int(dist_input[1:])
                        if 1 <= q_num <= 12 and q_num != 9:
                            new_district = f"Q{q_num}" # Đảm bảo định dạng chuẩn Q1, Q2...
                            break
                    dist_input = " ".join(dist_input.split())
                    if dist_input in ["THỦ ĐỨC", "BÌNH TÂN", "BÌNH THẠNH", "GÒ VẤP", "PHÚ NHUẬN", "TÂN BÌNH", "TÂN PHÚ"]:
                        new_district = dist_input
                        break
                    print("❌ Lỗi: Quận phải nằm trong thành phố Hồ Chí Minh!")

                # --- Nhập X mới ---
                while True:
                    try:
                        new_x = round(float(input("Nhập tọa độ x mới: ")), 3)
                        break
                    except ValueError: print("❌ Tọa độ x phải là số!")

                # --- Nhập Y mới ---
                while True:
                    try:
                        new_y = round(float(input("Nhập tọa độ y mới: ")), 3)
                        break
                    except ValueError: print("❌ Tọa độ y phải là số!")

                # Gọi hàm update
                customer_service.update_customer(target_id, new_name, new_district, new_x, new_y)
                print(f"✔ Đã cập nhật thành công khách hàng ID {target_id}")

            except Exception as e:
                print(f"❌ Có lỗi xảy ra: {e}")

        elif choice == "4":
            try:
                id = int(input("ID cần xóa: "))
                customer_service.delete_customer(id)
                print("✔ Đã xóa")
            except ValueError: print("❌ ID phải là số!")

        elif choice == "5":
            while True:
                key_input = input("🔍 Nhập ID hoặc Tên cần tìm: ").strip()
                
                if not key_input:
                    print("❌ Vui lòng không để trống ô tìm kiếm!")
                    continue
                
                # Chuẩn hóa đầu vào
                if key_input.isdigit():
                    key = int(key_input)
                    if key <= 0:
                        print("❌ ID phải là số dương!")
                        continue
                else:
                    key = " ".join(key_input.split()).title()
                
                # Thực hiện tìm kiếm
                result = customer_service.search(key)
                
                # --- PHẦN NÂNG CẤP IN BẢNG ĐẸP ---
                customers_to_show = []
                if isinstance(result, list):
                    customers_to_show = result # result đã là danh sách khách hàng
                elif result:
                    customers_to_show = [result] # Bỏ đối tượng đơn lẻ vào list để duyệt

                if not customers_to_show:
                    print(f"❌ Không tìm thấy khách hàng nào khớp với '{key}'")
                    cont = input("Bạn có muốn tìm lại không? (y/n): ").lower()
                    if cont != 'y':
                        break
                else:
                    headers = ["ID", "Tên Khách Hàng", "Quận", "Tọa độ X", "Tọa độ Y"]
                    # Chuyển đổi danh sách đối tượng thành danh sách các hàng dữ liệu thô
                    rows = [[c.id, c.name, c.district, c.x, c.y] for c in customers_to_show]
                    
                    print(f"\n✅ Tìm thấy {len(customers_to_show)} kết quả cho '{key}':")
                    # Gọi hàm in bảng chuyên nghiệp
                    print_table(headers, rows)
                    break

        elif choice == "6":
            while True:
                dist_input = input("Quận hoặc Thành Phố(khu vực HCM) (Ví dụ: Thủ Đức): ").strip().upper()
                # Loại bỏ tất cả khoảng trắng bên trong để "Q    12" -> "Q12"
                
                if dist_input.startswith("Q") and dist_input[1:].isdigit():
                    q_num = int(dist_input[1:])
                    if 1 <= q_num <= 12 and q_num != 9:
                        district = f"Q{q_num}" # Đảm bảo định dạng chuẩn Q1, Q2...
                        break
                dist_input = " ".join(dist_input.split())
                if dist_input in ["THỦ ĐỨC", "BÌNH TÂN", "BÌNH THẠNH", "GÒ VẤP", "PHÚ NHUẬN", "TÂN BÌNH", "TÂN PHÚ"]:
                    district = dist_input
                    break
                print("❌ Lỗi: Quận phải nằm trong thành phố Hồ Chí Minh!")

            # Thực hiện lọc
            result = customer_service.customers_by_district(district)
            
            if not result:
                print(f"ℹ️ Không có khách hàng nào ở {district}.")
            else:
                print(f"\n📍 DANH SÁCH KHÁCH HÀNG TẠI {district}")
                print(f"(Tổng số: {len(result)} khách hàng)")
                
                # --- PHẦN NÂNG CẤP IN BẢNG ĐẸP ---
                headers = ["ID", "Tên Khách Hàng", "Quận/Thành Phố", "Tọa độ X", "Tọa độ Y"]
                
                i = 0
                step = 10 # Số lượng khách hàng hiển thị mỗi trang
                while i < len(result):
                    # Lấy một nhóm khách hàng (tối đa 10 người)
                    current_batch = result[i : i + step]
                    
                    # Chuyển đổi đối tượng Customer thành danh sách dữ liệu thô để in bảng
                    rows = [[c.id, c.name, c.district, c.x, c.y] for c in current_batch]
                    
                    # Gọi hàm in bảng từ display.py
                    print_table(headers, rows)
                    
                    i += step
                    if i < len(result):
                        cont = input(f"👉 Đã hiển thị {i}/{len(result)}. Xem tiếp {step} người nữa? (y/n): ").lower()
                        if cont != "y":
                            break
                print("✅ Đã hiển thị xong danh sách.")
        elif choice == "7":
            customer_service.customers = customer_service.undo()
        
        elif choice == "0":
            break




# ================= QUẢN LÝ CHUYẾN ĐI =================
def ride_menu():
    print("\n┌" + "─" * 35 + "┐")
    print("│      📑 LỊCH SỬ CHUYẾN ĐI         │")
    print("├" + "─" * 35 + "┤")
    print("│ 1. 🗂️ Xem chuyến đi theo ID Tài xế │")
    print("│ 0. 🔙 Quay lại                    │")
    print("└" + "─" * 35 + "┘")

def ride_menu_loop(ride_service):
    while True:
        ride_menu()
        choice = input("Chọn: ").strip()
        if choice == "1":
            try:
                driver_id = int(input("Nhập ID tài xế: "))
                rides = ride_service.get_rides_by_driver(driver_id)
                if not rides:
                    print("❌ Tài xế chưa có chuyến đi")
                    continue
                print(f"✔ Tổng số chuyến: {len(rides)}")
                ride_service.show_rides(rides)
            except ValueError: print("❌ ID phải là số!")
        elif choice == "0": 
            
            break




# ================= MAIN =================
def main():
    # Khởi tạo service tại đây để dùng chung dữ liệu
    driver_service = DriverService()
    customer_service = CustomerService()
    ride_service = RideService()
    matching_service = MatchingService(driver_service, customer_service, ride_service)
    booking_queue = Queue()


    while True:
        main_menu()
        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            driver_menu_loop(driver_service)
        elif choice == "2":
            customer_menu_loop(customer_service)
        elif choice == "3":
            ride_menu_loop(ride_service)

        elif choice == "4":
            try:
                # --- Nhập và kiểm tra ID khách hàng ---
                while True:
                    cid_input = input("Nhập ID khách hàng: ").strip()
                    
                    # 1. Kiểm tra định dạng số
                    if not cid_input.isdigit():
                        print("❌ Lỗi: ID phải là số nguyên!")
                        continue
                    
                    cid = int(cid_input)
                    
                    # 2. Kiểm tra sự tồn tại trong hệ thống
                    customer = customer_service.get_by_id(cid)
                    if not customer:
                        print(f"❌ Không tìm thấy khách hàng có ID: {cid}. Vui lòng thử lại.")
                        continue
                    
                    # Nếu vượt qua cả 2 bước trên thì thoát vòng lặp
                    break

                # --- Nhập bán kính ---
                while True:
                    try:
                        R = float(input(f"Nhập bán kính tìm kiếm quanh {customer.name} (km): "))
                        min_dist = [100] # min khoảng cách hiện tại là 100km :))
                        matches = matching_service.find_nearby_drivers(cid, R,min_dist)
                        if R > 0 and matches: break
                        if not matches:
                            print(f"❌ Trong bán kính {R}km không có tài xế nào, vui lòng nhập lại!!")
                            print(f"hiện tại trong phạm vi {min_dist} mới có tài xế")
                        else:
                            print("❌ Bán kính phải > 0!")
                    except ValueError: print("❌ Vui lòng nhập số!")



                # --- Hiển thị thông tin khách hàng (Dạng khung) ---
                print("\n" + "="*60)
                print(f"🔍 THÔNG TIN TÌM KIẾM")
                print(f"👤 Khách hàng : {customer.name:<20} | ID: {customer.id}")
                print(f"🏠 Khu vực    : {customer.district:<20} | Tọa độ: ({customer.x}, {customer.y})")
                print(f"📡 Phạm vi    : {R} km")
                print("="*60)

                # --- Hiển thị bảng tài xế ---
                headers = ["ID", "Tên tài xế", "Rating", "Khoảng cách (km)"]
                rows = []
                for d, dist in matches:
                    rows.append([
                        d.id, 
                        d.name, 
                        f"{d.rating:.2f} ⭐", 
                        f"{dist:.2f}"
                    ])
                
                # Gọi hàm in bảng của bạn
                
                print(f"\n✅ Tìm thấy {len(matches)} tài xế phù hợp:")
                print_table(headers, rows)
                
                print("="*60 + "\n")

            except Exception as e:
                print(f"❌ Lỗi hệ thống: {e}")


        elif choice == "5":
            try:
                cid = int(input("ID khách hàng: "))
                did = int(input("ID tài xế: "))
                
                # Tìm đối tượng Customer và Driver thực tế
                cust = customer_service.get_by_id(cid)
                driv = driver_service.get_by_id(did)
                

                if cust and driv:
                    trip_dist = float(input("Quãng đường chuyến đi: "))

                    # Tính phí trước để người dùng xem
                    ride = ride_service.book_ride(cust, driv, trip_dist)
                    print(f"💰 Phí dự kiến cho khách {cust.name}: {ride.fare} VND")

                    
                
                # 2. Ghi từ Queue vào file requests.txt theo đúng thứ tự
                    # Tạo đối tượng ride tạm thời
                    if input("Xác nhận đặt xe? (y/n): ").lower() == "y":
                        # 1. Đưa vào hàng đợi RAM (Thêm cả tên vào tuple để quản lý)
                        booking_queue.enqueue((cust.id, cust.name, driv.id, driv.name, trip_dist, ride.fare))

                        # Gọi hàm confirm_ride đã sửa ở bước 
                        
                        print("✔ Chuyến đi mới đã được đặt thành công (ID: 1)!")
                        print(f"✅ Đã thêm khách hàng {cid} vào hàng đợi")
                        
                        save_request_to_file(cust.id, cust.name, driv.id, driv.name, trip_dist, ride.fare)
                        print("✅ Đã thêm vào hàng đợi.")
                else:
                    print("❌ Lỗi: ID khách hàng hoặc tài xế không tồn tại.")
            except Exception as e: 
                print(f"❌ Lỗi: {e}")

        elif choice == "6":
            try:
                # 1. Nhập và kiểm tra ID khách hàng
                cid_input = input("Nhập ID khách hàng muốn đặt xe tự động: ").strip()
                if not cid_input.isdigit():
                    print("❌ Lỗi: ID phải là số nguyên!")
                    continue
                
                cid = int(cid_input)
                customer = customer_service.get_by_id(cid)
                if not customer:
                    print(f"❌ Không tìm thấy khách hàng ID: {cid}")
                    continue

                # 2. Nhập bán kính giới hạn (R)
                try:
                    R = float(input(f"Nhập bán kính giới hạn để tìm tài xế gần nhất (km): "))
                    if R <= 0:
                        print("❌ Bán kính phải lớn hơn 0!")
                        continue
                except ValueError:
                    print("❌ Vui lòng nhập số cho bán kính!")
                    continue

                # 3. Tìm tài xế gần nhất trong bán kính R
                # matching_service.find_nearby_drivers thường trả về list [(driver, distance), ...] đã sắp xếp theo khoảng cách
                min_dist_box = [100] # Hộp chứa khoảng cách nhỏ nhất tìm được nếu không thấy trong R
                matches = matching_service.find_nearby_drivers(cid, R, min_dist_box)

                if not matches:
                    print(f"❌ Không tìm thấy tài xế nào trong phạm vi {R}km.")
                    print(f"💡 Tài xế gần nhất hiện tại đang ở cách {min_dist_box[0]:.2f}km.")
                    continue

                # Lấy người gần nhất (phần tử đầu tiên của danh sách matches)
                best_driver, distance_to_cust = matches[0]
                
                print(f"\n🤖 Đã tìm thấy tài xế tốt nhất cho bạn:")
                print(f"   - Tài xế: {best_driver.name} (ID: {best_driver.id})")
                print(f"   - Khoảng cách đến bạn: {distance_to_cust:.2f} km")
                print(f"   - Đánh giá: {best_driver.rating} ⭐")

                # 4. Nhập quãng đường chuyến đi (Trip Distance)
                try:
                    trip_dist = float(input("Nhập quãng đường di chuyển của chuyến đi (km): "))
                except ValueError:
                    print("❌ Quãng đường không hợp lệ!")
                    continue

                # 5. Tiến hành đặt xe tự động
                ride = ride_service.book_ride(customer, best_driver, trip_dist)  # hàm tình tiến 
                print(f"💰 Phí dự kiến: {ride.fare} VND")
                
                confirm = input("Xác nhận tự động đặt tài xế này? (y/n): ").lower()
                if confirm == "y":
                    # Lưu vào Queue và File requests.txt
                    booking_queue.enqueue((customer.id, customer.name, best_driver.id, best_driver.name, trip_dist, ride.fare))
                    # lưu vào file request.txt 
                    save_request_to_file(customer.id, customer.name, best_driver.id, best_driver.name, trip_dist, ride.fare)
                    print(f"✅ Đã thêm {best_driver.name} vào hàng đợi cho khách {customer.name}")
                    

                    print(f"✔ Chúc mừng! Tài xế {best_driver.name} đang đến đón bạn.")
                else:
                    print("🔄 Đã hủy đặt xe tự động.")

            except Exception as e:
                print(f"❌ Lỗi hệ thống khi ghép cặp: {e}")
    
        elif choice == "7":
            matching_service.process_and_show_requests()
        elif choice == "8":
            drivers = driver_service.drivers
            customers = customer_service.customers
            
            plot_customers_and_drivers(drivers, customers)

        elif choice == "0":
            print("Thoát hệ thống MinRide.")
            
            
            customer_service.save()
            driver_service.save()
            
            break
        else: print("❌ Lựa chọn không hợp lệ")

if __name__ == "__main__":
    main()

    