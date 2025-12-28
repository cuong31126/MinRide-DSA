# services/customer_service.py
from utils.file_io import load_customers, save_customers
from algorithms.search import *
from algorithms.sort import quick_sort_customers_by_id 
from config import CUSTOMERS_FILE
from utils.display import print_table
from structures.stack import Stack 
import copy

class CustomerService:

    def __init__(self):
        self.customers = load_customers(CUSTOMERS_FILE) # Gọi hàm từ file_io.py để đọc dữ liệu khách hàng
        self.undo_stack = Stack()


    def show_all(self):  # chức năng 1 
        headers = ["ID", "Tên", "Quận", "X", "Y"]
        rows = [[c.id, c.name, c.district, c.x, c.y] for c in self.customers]
        print_table(headers, rows)

    def get_next_id(self):  # chức năng 2 
        # Nếu danh sách trống, bắt đầu từ ID 1
        if not self.customers: 
            return 1
        # Tìm ID lớn nhất hiện có và cộng thêm 1
        max_id = max(d.id for d in  self.customers) 
        return max_id + 1
    
    def exists(self, id):  # chức năng 2     chức năng 3 
        return any(d.id == id for d in self.customers)

    def add_customer(self, customer):  # chức năng 2 
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
        

    def update_customer(self, cid, new_name, new_district, new_x, new_y):  # chức năng 3 
        self.save_state()
        c = binary_search_customer_by_id(self.customers, cid)
        if c:
            c.name = new_name
            c.district = new_district
            c.x = new_x
            c.y = new_y

    def delete_customer(self, cid):   # chức năng 4 
        self.save_state()
        self.customers = [c for c in self.customers if c.id != cid]

    def search(self, keyword):   # chức năng 5 
        # Nếu keyword đã là số (do main.py ép kiểu)
        if isinstance(keyword, int):
            return binary_search_customer_by_id(self.customers, keyword)
        
        # Nếu keyword là chuỗi
        if isinstance(keyword, str):
            return linear_search_customer_by_name(self.customers, keyword)
        return None
    
    def customers_by_district(self, district): # chức năng 6 
    # Lọc khách hàng theo quận
        filtered = [c for c in self.customers if c.district.lower() == district.lower()]
        filtered = quick_sort_customers_by_id(filtered)
        return filtered
        
    def undo(self):
        if not self.undo_stack.is_empty():
            print("↩️ Đã quay lại trạng thái trước đó.")
            # Lấy trạng thái gần nhất ra khỏi Stack và cập nhật lại danh sách chính
            self.customers = self.undo_stack.pop()
            return self.customers
        else:
            print("❌ Không có trạng thái nào để quay lại.")
            return self.customers



    def list_by_district(self, district, start=0, limit=10):
        filtered = [c for c in self.customers if c.district.lower() == district.lower()]
        filtered = (filtered)
        return filtered, filtered[start:start+limit]

    def save(self):#lưu trạng thái vô file    # chức năng 0 trong def main 
        save_customers(CUSTOMERS_FILE, self.customers)

    def get_by_id(self, cid):   # dùng trong def main 
        return next((c for c in self.customers if c.id == cid), None)
    

    
    def save_state(self):
        # Lưu bản sao sâu của danh sách khách hàng vào Stack
        self.undo_stack.push(copy.deepcopy(self.customers))

    
