# Truck class, initial location index is set to 0, representing trucks beginning delivery route at the shipping hub.
class Truck:
    def __init__(self, speed, miles, packages, depart_time, current_time):
        self.speed = speed
        self.miles = miles
        self.packages = packages
        self.depart_time = depart_time
        self.current_time = current_time
        self.locationIndex = 0
