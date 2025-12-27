# models/customer.py
class Customer:
    def __init__(self, id, name, district, x, y):
        self.id = id
        self.name = name
        self.district = district
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.id} | {self.name} | {self.district} | ({self.x}, {self.y})"