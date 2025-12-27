class Ride:
    def __init__(self, ride_id, customer_id, driver_id, distance, fare):
        self.ride_id = ride_id
        self.customer_id = customer_id
        self.driver_id = driver_id
        self.distance = distance
        self.fare = fare

    def __str__(self):
        return (f"Ride {self.ride_id} | Customer {self.customer_id} | "
                f"Distance {self.distance}km | Fare {self.fare} ")
