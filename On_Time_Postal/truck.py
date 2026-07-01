
# creates truck class
class Truck:
    def __init__(self, capacity, speed, load, packages, milage, address, departure_time, truck_number):
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.milage = milage
        self.address = address
        self.departure_time = departure_time
        self.time = departure_time
        self.truck_number = truck_number

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.capacity, self.speed, self.load, self.packages, self.milage, self.address, self.departure_time)
