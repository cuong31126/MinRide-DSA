import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.lines import Line2D # Thêm dòng này để dùng được Line2D

def plot_customers_and_drivers(drivers, customers):
    # 1. Định nghĩa bảng màu (Nên để ở đầu để dễ quản lý)
    COLOR_CUSTOMER = "#1E90FF"  # Xanh dương
    COLOR_DRIVER = "#FF4500"    # Đỏ cam
    COLOR_BOTH = "#FFD700"      # Vàng (Điểm chung)

    # Khởi tạo hình ảnh
    plt.figure(figsize=(10, 7))
    point_map = defaultdict(lambda: {"customers": [], "drivers": []})

    # Gom nhóm dữ liệu
    for c in customers:
        point_map[(c.x, c.y)]["customers"].append(c)
    for d in drivers:
        point_map[(d.x, d.y)]["drivers"].append(d)

    # 2. Vẽ các điểm dữ liệu
    for (x, y), data in point_map.items():
        c_list = data["customers"]
        d_list = data["drivers"]
        
        # Logic chọn màu điểm
        if len(c_list) > 0 and len(d_list) > 0:
            point_color = COLOR_BOTH
        elif len(c_list) > 0:
            point_color = COLOR_CUSTOMER
        else:
            point_color = COLOR_DRIVER

        # Vẽ điểm scatter
        size = 150 + (len(c_list) + len(d_list) > 1) * 150
        plt.scatter(x, y, s=size, c=point_color, alpha=0.7, edgecolors='black', zorder=3)

        # Xử lý nhãn tên tại điểm
        labels = [(d.name, "black") for d in d_list] + [(c.name, "red") for c in c_list]
        for idx, (name, text_color) in enumerate(labels):
            plt.text(x + 0.1, y + 0.1 + idx * 0.2, name, fontsize=9, 
                    color=text_color, fontweight='bold', zorder=4)

    # 3. CHỈNH SỬA TẠI ĐÂY: Đưa chú thích ra NGOÀI vòng lặp for
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Khách hàng',
               markerfacecolor=COLOR_CUSTOMER, markersize=12),
        Line2D([0], [0], marker='o', color='w', label='Tài xế',
               markerfacecolor=COLOR_DRIVER, markersize=12),
        Line2D([0], [0], marker='o', color='w', label='Điểm chung',
               markerfacecolor=COLOR_BOTH, markersize=12, markeredgecolor='black')
    ]
    plt.legend(handles=legend_elements, loc='upper right', shadow=True, title="Danh mục")

    # 4. Các thiết lập hiển thị khác
    plt.xlabel("Tọa độ X")
    plt.ylabel("Tọa độ Y")
    plt.title("Bản đồ phân bố MinRide")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.axis('equal') # Giúp bản đồ không bị méo tỉ lệ
    plt.savefig("distribution_plot.png")
    plt.show()