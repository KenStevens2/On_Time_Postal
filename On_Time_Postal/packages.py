import datetime

# creates class Package
class Package:
    def __init__(self, package_id, address, city, state, zip_code, delivery_deadline, weight, notes, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.departure_time = None
        self.delivery_time = None
        self.truck_number = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.address, self.city, self.state, self.zip_code, self.delivery_deadline, self.weight, self.status, self.delivery_time, self.truck_number)

    # sets status of a package
    def get_status(self, check_time):

        # if the user enters a time after the delivery_time it shows delivered
        if check_time > self.delivery_time:
            self.status = "Delivered"

        # if the user enters a time after the package's departure_time but before delivery_time it will show en route
        elif self.departure_time <= check_time < self.delivery_time:
            self.status = "En route"

        # else it will show package at hub
        else:
            self.status = "At the hub"

        # updates package 9 information at 10:20
        if self.package_id == 9:

            if check_time > datetime.timedelta(hours=10, minutes=20):
                self.address = "410 S State St"
                self.zip_code = "84111"

            else:
                self.address = "300 State St"
                self.zip_code = "84103"

        # for packages 6, 25, 28, and 32 they will be marked as delayed until after 9:05
        if self.package_id in [6, 25, 28, 32]:

            if check_time < datetime.timedelta(hours=9, minutes=5):
                self.status = "DELAYED"

