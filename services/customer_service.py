# services/customer_service.py
from utils.file_io import load_customers, save_customers
from algorithms.search import *
from algorithms.sort import quick_sort_customers_by_id 
from config import CUSTOMERS_FILE
from utils.display import print_table
import copy

class CustomerService:

    def __init__(self):
        self.customers = load_customers(CUSTOMERS_FILE) # Gọi hàm từ file_io.py để đọc dữ liệu khách hàng
        self.undo_stack = []


    def show_all(self):
        headers = ["ID", "Tên", "Quận", "X", "Y"]
        rows = [[c.id, c.name, c.district, c.x, c.y] for c in self.customers]
        print_table(headers, rows)

    def add_customer(self, customer):
        self.save_state()
        """Chèn khách hàng vào danh sách theo đúng thứ tự ID tăng dần"""
        inserted = False
        for i in range(len(self.customers)):
            # Nếu tìm thấy ID lớn hơn ID đang chèn, thì chèn vào ngay vị trí đó
            if self.customers[i].id > customer.id:
                self.customers.insert(i, customer)
                inserted = True
                break
        
        # Nếu duyệt hết danh sách mà ko thấy ID nào lớn hơn, thì thêm vào cuối
        if not inserted:
            self.customers.append(customer)
        
        # Lưu vào file ngay sau khi chèn để cập nhật requests.txt hoặc customers.txt
        

    def update_customer(self, cid, new_name, new_district, new_x, new_y):
        self.save_state()
        c = binary_search_customer_by_id(self.customers, cid)
        if c:
            c.name = new_name
            c.district = new_district
            c.x = new_x
            c.y = new_y

    def delete_customer(self, cid):
        self.save_state()
        self.customers = [c for c in self.customers if c.id != cid]

    def search(self, keyword):  
        # Nếu keyword đã là số (do main.py ép kiểu)
        if isinstance(keyword, int):
            return binary_search_customer_by_id(self.customers, keyword)
        
        # Nếu keyword là chuỗi
        if isinstance(keyword, str):
            if keyword.isdigit():
                return binary_search_customer_by_id(self.customers, int(keyword))
            else:
                # Tìm kiếm theo tên
                return linear_search_customer_by_name(self.customers, keyword)
        return None



    def top_k(self, k, top=True):
        sorted_list = quick_sort_customers_by_id(self.customers)
        return sorted_list[:k] if top else sorted_list[-k:]

    def list_by_district(self, district, start=0, limit=10):
        filtered = [c for c in self.customers if c.district.lower() == district.lower()]
        filtered = (filtered)
        return filtered, filtered[start:start+limit]

    def save(self):#lưu trạng thái vô file
        save_customers(CUSTOMERS_FILE, self.customers)

    def customers_by_district(self, district):
    # Lọc khách hàng theo quận
        filtered = [c for c in self.customers if c.district.lower() == district.lower()]

        # Sắp xếp theo ID tăng dần (dùng Quick Sort bạn đã viết)
        
        filtered = quick_sort_customers_by_id(filtered)

        return filtered
    
    def exists(self, id):
        return any(d.id == id for d in self.customers)
    
    def get_by_id(self, cid):
        return next((c for c in self.customers if c.id == cid), None)
    
    def get_next_id(self):
        # Nếu danh sách trống, bắt đầu từ ID 1
        if not self.customers: # (Sửa thành self.customers đối với CustomerService)
            return 1
        # Tìm ID lớn nhất hiện có và cộng thêm 1
        max_id = max(d.id for d in  self.customers) 
        return max_id + 1

    def save_state(self):#lưu trạng thái để quay lại
        self.undo_stack.append(copy.deepcopy(self.customers))

    def undo(self):

        if self.undo_stack:

            print("↩️ Đã quay lại trạng thái trước đó.")
            return self.undo_stack.pop()
        else:
            print("❌ Không có trạng thái nào để quay lại.")
            return self.customers
