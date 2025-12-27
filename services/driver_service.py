# services/driver_service.py
from utils.file_io import load_drivers, save_drivers 
from algorithms.search import *
from algorithms.sort import *
from config import DRIVERS_FILE
from utils.display import print_table
import copy


class DriverService:

    def __init__(self):
        # Load dữ liệu và đảm bảo nó luôn ở thứ tự ID tăng dần ngay từ đầu
        self.drivers = load_drivers(DRIVERS_FILE)
        self.drivers.sort(key=lambda d: d.id) 
        self.undo_stack = []

    def show_all(self, sorted_view=False):   # giúp show hết hoặc sắp xếp theo rating chức năng 1  và 6 trong ql tài xế 
        """
        Mặc định hiển thị theo thứ tự ID (danh sách chính).
        Nếu sorted_view=True mới hiển thị theo Rating.
        """
        headers = ["ID", "Tên", "Rating", "X", "Y"]
        
        # Quyết định danh sách nào sẽ được in ra
        
        display_list = self.sort_by_rating() if sorted_view else self.drivers
        
        rows = [[d.id, d.name, d.rating, d.x, d.y] for d in display_list]
        print_table(headers, rows)
    
    def add_driver(self, driver):     # lựa chọn 2 
        self.save_state()
        """Tự động chèn tài xế mới vào đúng vị trí để ID luôn tăng dần"""
        inserted = False
        for i in range(len(self.drivers)):
            if self.drivers[i].id > driver.id:
                self.drivers.insert(i, driver)
                inserted = True
                break
        if not inserted:
            self.drivers.append(driver)

    def get_next_id(self):   # lựa chọn 3 
        # Nếu danh sách trống, bắt đầu từ ID 1
        if not self.drivers: # (Sửa thành self.customers đối với CustomerService)
            return 1
        # Tìm ID lớn nhất hiện có và cộng thêm 1
        max_id = max(d.id for d in self.drivers)
        return max_id + 1

    def search_driver(self, keyword):  # lựa chọn 3    lựa chọn 5 
        if keyword.isdigit():
            return binary_search_driver_by_id(self.drivers, int(keyword))
        return linear_search_driver_by_name(self.drivers, keyword)

    def update_driver(self, driver_id, new_rating,new_x,new_y):  # lựa chọn 3 
        self.save_state()
        d = binary_search_driver_by_id(self.drivers, driver_id)
        if d:
            d.rating = new_rating
            d.x = new_x
            d.y = new_y

    def delete_driver_by_id(self, driver_id):  # lựa chọn 4   
        self.save_state()
        self.drivers = [d for d in self.drivers if d.id != driver_id]

    def exists(self, id):  # lựa chọn 4 
        return any(d.id == id for d in self.drivers)

    def sort_by_rating(self):  # chức năng 6 
        
        """Sắp xếp để xem nhưng KHÔNG gán lại vào self.drivers chính"""
        # Tạo bản sao để sắp xếp mà không ảnh hưởng danh sách gốc
        temp_list = quick_sort_drivers_by_id(list(self.drivers), reverse=True)
        return radix_sort_drivers_by_rating(temp_list)

    def show_top_k(self, k, top=True):   # lựa chọn 7 
        """Hiển thị Top K từ bản sao đã sắp xếp"""
        sorted_temp = self.sort_by_rating()
        return sorted_temp[:k] if top else sorted_temp[-k:]

    def save(self):
        save_drivers(DRIVERS_FILE, self.drivers)

    def get_by_id(self, driver_id): # choice 5 
        for d in self.drivers:
            if d.id == driver_id:
                return d
        return None
    
    def save_state(self):#lưu trạng thái để quay lại      lựa chon 2 ,3, 4  
        self.undo_stack.append(copy.deepcopy(self.drivers))

    def undo(self):  # lựa chọn 8 

        if self.undo_stack:

            print("↩️ Đã quay lại trạng thái trước đó.")
            return self.undo_stack.pop()
        else:
            print("❌ Không có trạng thái nào để quay lại.")
            return self.drivers