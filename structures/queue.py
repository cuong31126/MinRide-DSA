# structures/queue.py
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        """Thêm yêu cầu vào cuối hàng đợi"""
        self.items.append(item)

    def dequeue(self):
        """Lấy yêu cầu đầu tiên ra để xử lý"""
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def is_empty(self):
        return len(self.items) == 0