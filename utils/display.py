# utils/display.py

def print_line(widths):
    print("+" + "+".join("-" * w for w in widths) + "+")


def print_row(values, widths):
    row = "|"
    for val, w in zip(values, widths):
        row += str(val).ljust(w) + "|"
    print(row)

# join(): Dùng để nối các phần tử trong một danh sách thành một chuỗi duy nhất, ngăn cách bởi ký tự đại diện
# ljust(w) (Left Justify): Dùng để căn lề trái một chuỗi. Nó sẽ thêm khoảng trắng vào bên phải chuỗi đó cho đến khi đạt được độ dài w
# zip(values, widths): Dùng để ghép đôi các phần tử tương ứng của hai danh sách lại với nhau để duyệt cùng lúc
# Ví dụ: Nếu có values = ["Cường", 5] và widths = [10, 5], zip sẽ tạo ra các cặp ("Cường", 10) và (5, 5)

def print_table(headers, rows):
    """
    headers: list[str]
    rows: list[list]
    """
    widths = [max(len(str(h)), 12) for h in headers]

    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)) + 2)
            

    print_line(widths)
    print_row(headers, widths)
    print_line(widths)  # trang trí tiêu đề 

    for row in rows:
        print_row(row, widths)

    print_line(widths)
