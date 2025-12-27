# 🚗 MinRide System - Ride-Sharing Management (DSA Focus)

MinRide là một hệ thống quản lý đặt xe thông minh, được xây dựng tập trung vào việc áp dụng các cấu trúc dữ liệu và giải thuật (DSA) tối ưu để giải quyết bài toán kết nối giữa Khách hàng và Tài xế trong thời gian thực.

---

## 🏗️ Kiến trúc hệ thống (System Architecture)

Dự án được thiết kế theo mô hình phân tầng chức năng, tách biệt giữa dữ liệu, logic nghiệp vụ và các thuật toán nền tảng:

1. **Models**: Định nghĩa các thực thể dữ liệu cơ bản như Driver, Customer, Ride.
2. **Services**: Điều hướng logic nghiệp vụ gồm Matching, Booking và Undo.
3. **Algorithms**: Thư viện các thuật toán tìm kiếm và sắp xếp tùy chỉnh.
4. **Structures**: Các cấu trúc dữ liệu tự định nghĩa như Queue và Stack.

---

## 🛠️ Cấu trúc dữ liệu & Giải thuật áp dụng

Hệ thống tận dụng tối đa sức mạnh của DSA để tối ưu hóa hiệu suất xử lý:

### 1. Thuật toán Sắp xếp (Sorting Algorithms)
- **Radix Sort**: Sử dụng trong `DriverService` để sắp xếp tài xế theo Rating[cite: 4]. Thuật toán đạt độ phức tạp O(nk), hiệu quả hơn các thuật toán so sánh thông thường khi xử lý dữ liệu số thực đã chuẩn hóa.
- **Quick Sort**: Áp dụng trong `CustomerService` để duy trì danh sách khách hàng theo ID tăng dần. Độ phức tạp trung bình đạt O(n log n).

### 2. Thuật toán Tìm kiếm (Searching Algorithms)
- **Binary Search**: Sử dụng cho các truy vấn theo ID cho Tài xế và Khách hàng. Giảm thời gian truy xuất xuống O(log n) nhờ duy trì dữ liệu ở trạng thái sắp xếp.
- **Linear Search**: Sử dụng khi tìm kiếm theo Tên (Keyword) cho các trường dữ liệu không có tính chất sắp xếp.

### 3. Cấu trúc dữ liệu tuyến tính (Linear Structures)
- [cite_start]**Queue (FIFO)**: Quản lý hàng đợi đặt xe tại `data/requests.txt`. Đảm bảo tính công bằng theo nguyên tắc First-Come, First-Served.
- **Stack (LIFO)**: Cốt lõi của tính năng Undo. [cite_start]Lưu trữ trạng thái dữ liệu (deepcopy) trước mỗi thay đổi để khôi phục nhanh chóng[cite: 4].

### 4. Giải thuật Hình học (Geometric Algorithm)
- **Euclidean Distance**: Tính toán khoảng cách đường chim bay giữa tọa độ (x, y) để tìm kiếm trong bán kính R và tính giá cước.

---

## 🚀 Các tính năng chính

- [cite_start]**Quản lý Thực thể**: CRUD (Thêm, Sửa, Xóa) Tài xế và Khách hàng với cơ chế ID tự động.
- **Matching thông minh**: Tìm kiếm tài xế trong bán kính R và tự động tính toán "Tiền tiết kiệm".
- **Hàng đợi Requests**: Lưu trữ tạm thời các yêu cầu đặt xe chưa xác nhận vào `requests.txt`, hỗ trợ xử lý hàng loạt.
- [cite_start]**Hệ thống Undo**: Cho phép hoàn tác các thao tác quản lý dữ liệu sai sót thông qua Stack.
- **Visualize**: Trực quan hóa vị trí thực tế của các đối tượng trên bản đồ tọa độ XY.

---

## 📁 Cấu trúc thư mục

MinRide/
├── main.py              # Entry point và Menu điều khiển
├── config.py            # Cấu hình đường dẫn file dữ liệu
├── models/              # Định nghĩa lớp đối tượng (Driver, Customer, Ride)
├── services/            # Logic xử lý nghiệp vụ (Matching, Ride, v.v.)
├── algorithms/          # Thuật toán tìm kiếm & sắp xếp (Radix, Quick, Binary)
├── structures/          # Cấu trúc dữ liệu Stack & Queue
├── utils/               # File IO, hiển thị bảng, tính khoảng cách
└── data/                # File lưu trữ dữ liệu txt (drivers, customers, rides, requests)

---

## 💻 Hướng dẫn sử dụng

1. **Khởi chạy**: Thực thi file `main.py` để bắt đầu chương trình.
2. **Nhập liệu**: Tuân thủ định dạng số cho ID, tọa độ và Rating (0-5).
3. **Lưu trữ**: Dữ liệu tự động đồng bộ vào các file `.txt` khi thoát ứng dụng hoặc xác nhận giao dịch.



---

## 📊 Phân tích hiệu năng Thuật toán (Complexity Analysis)

Hệ thống được tối ưu hóa dựa trên các chỉ số độ phức tạp thời gian (Time Complexity):

| Chức năng             | Thuật toán    | Độ phức tạp   | Lý do chọn                                                                |
| :---                  | :---          | :---          | :---                                                                      |
| **Tìm theo ID**       | Binary Search | O(log n)      | Dữ liệu được duy trì sắp xếp sẵn, cực nhanh khi tập dữ liệu lớn.          |
| **Sắp xếp Rating**    | Radix Sort    | O(nk)         | Hiệu quả hơn QuickSort ($n \log n$) khi phạm vi giá trị Rating hẹp (0-5). |
| **Sắp xếp Khách**     | Quick Sort    | O(n log n)    | Thuật toán phân hoạch chia để trị, ổn định cho việc quản lý danh mục.     |
| **Tính khoảng cách**  | Euclidean     | O(1)          | Công thức toán học thuần túy, thực hiện tức thời.                         |
| **Hàng đợi**          | FIFO Queue    | O(1)          | Thao tác Enqueue/Dequeue trên List Python tối ưu cho luồng đặt xe.        |

---

## 🔄 Quy trình nghiệp vụ (Workflow Simulation)

1. **Giai đoạn Nhập liệu**:
   - Dữ liệu từ file `.txt` được nạp vào bộ nhớ (RAM) thông qua `file_io.py`.
   - `CustomerService` và `DriverService` khởi tạo, tự động sắp xếp danh sách để sẵn sàng cho Binary Search.

2. **Giai đoạn Ghép cặp (Matching)**:
   - Hệ thống quét danh sách tài xế trong bán kính R.
   - Sử dụng công thức Euclidean để lọc và Radix Sort để đề xuất tài xế có Rating cao nhất ở gần nhất.

3. **Giai đoạn Giao dịch & Undo**:
   - Mỗi thay đổi (Thêm/Xóa) đều được đẩy vào `Stack` (LIFO).
   - Khi chọn Undo, hệ thống `pop()` trạng thái gần nhất để khôi phục dữ liệu mà không cần load lại file từ đĩa.

4. **Giai đoạn Kết thúc**:
   - Khi thoát ứng dụng (`choice == "0"`), hệ thống thực hiện đồng bộ ngược từ RAM xuống các file dữ liệu trong thư mục `data/` để lưu trữ bền vững.

---

## 🛠 Yêu cầu hệ thống (Prerequisites)

* **Ngôn ngữ**: Python 3.8+
* **Thư viện**: `matplotlib` (để visualize bản đồ)
* **Dữ liệu**: Thư mục `data/` phải chứa các file `.txt` có định dạng header chuẩn.