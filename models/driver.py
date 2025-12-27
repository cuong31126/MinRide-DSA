# models/driver.py
class Driver:
    def __init__(self, id, name, rating, x, y):
        self.id = id
        self.name = name
        self.rating = rating
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.id} | {self.name} | {self.rating} | ({self.x}, {self.y})"
