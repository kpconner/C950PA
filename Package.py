import datetime


# Package class, initializes package objects with details from package table csv file and sets initial delivery and
# departure times to none.  Also sets initial address index and status to none.
class Package:
    def __init__(self, pid, address, city, state, zipcode, deadline, weight, notes):
        self.pid = pid
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zipcode = zipcode
        self.state = state
        self.weight = weight
        self.notes = notes
        self.delivery_time = None
        self.departure_time = None
        self.address_index = None
        self.status = None

    # Method used to set package's delivery address index to index value from address indexes csv file that matches the
    # packages address value
    def set_address_index(self, addresses):
        for address in addresses:
            if self.address == address:
                self.address_index = addresses.index(address)

    # Method to update a packages delivery address
    def update_address(self, address, city, zipcode):
        self.address = address
        self.city = city
        self.zipcode = zipcode

    # Method to determine a packages status at a given time variable.  Checks if package is delayed from packages
    # additional notes and sets status to delayed time variable is less than 9:05.  If time is less than departure time
    # status is set to 'At hub'. If time is after departure time, but before delivery time, status is set to 'En route',
    # otherwise status is set to delivered.
    def calc_status(self, time):
        if 'Delayed' in self.notes and time < datetime.timedelta(hours=9, minutes=5):
            self.status = 'Delayed'
        elif self.departure_time >= time:
            self.status = "At hub"
        elif self.delivery_time >= time:
            self.status = "En route"
        else:
            self.status = "Delivered"

    # Method to print package objects. Checks if status is 'Delivered', if true the packages delivery time is included.
    def __str__(self):
        if self.status == 'Delivered':
            return f'Package ID: {self.pid}, Address: {self.address}, {self.city}, {self.state}, {self.zipcode} \n' \
                   f'Weight: {self.weight}, Delivery Deadline: {self.deadline}, Additional Notes: {self.notes} \n' \
                   f'Status: {self.status} at {self.delivery_time} \n'
        else:
            return f'Package ID: {self.pid}, Address: {self.address}, {self.city}, {self.state}, {self.zipcode} \n' \
                   f'Weight: {self.weight}, Delivery Deadline: {self.deadline}, Additional Notes: {self.notes} \n' \
                   f'Status: {self.status} \n'
