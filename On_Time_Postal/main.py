"""

Code created by KenStevens2

"""
#import dependencies
import csv
import datetime

import truck
from hashtable import HashTable
from packages import Package

# assign csv files to local variables
addresses_csv = list(csv.reader(open('csv/Addresses.csv')))
distance_csv = list(csv.reader(open('csv/Distance.csv')))
packages_csv = list(csv.reader(open('csv/Packages.csv')))

# define initial package information
def initial_package_data(filename):
    with open(filename) as packages_info:
        package_data = csv.reader(packages_info)
        for package in package_data:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDelivery_deadline = package[5]
            pWeight = package[6]
            pNotes = package[7]
            pStatus = "At the hub"
            p = Package(pID, pAddress, pCity, pState, pZip, pDelivery_deadline, pWeight, pNotes, pStatus)

            packages_hashtable.insert(pID, p)

# initialize hashtable
packages_hashtable = HashTable()

# convert distance data from cvs file to integer values
def convert_addresses(address):
    for row in addresses_csv:
        if address in row[2]:
            return int(row[0])
    return None


# calculate distance between two addresses and if empty defines them as 0.0
def distance_calculation(address1, address2):
    distance = distance_csv[address1][address2]
    if distance == '':
        distance = distance_csv[address2][address1]
    return float(distance)

# loads csv file information into package data
initial_package_data('csv/Packages.csv')

# manually creating loading trucks and setting parameters
truck1 = truck.Truck(16, 18, None, [1, 2, 4, 7, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East", datetime.timedelta(hours = 8), 1)
truck2 = truck.Truck(16, 18, None, [3, 5, 6, 18, 23, 24, 25, 27, 28, 32, 35, 36, 37, 38, 39], 0.0, "4001 South 700 East", datetime.timedelta(hours = 9, minutes = 10), 2)
truck3 = truck.Truck(16, 18, None, [8, 9, 10, 11, 12, 17, 21, 22, 26, 33], 0.0, "4001 South 700 East", datetime.timedelta(hours = 11), 3)

# Nearest Neighbor algorithm for selecting the closest package to deliver next
def truck_delivery(truck):

    # loads packages into en_route
    en_route = []
    for package_id in truck.packages:
        package = packages_hashtable.get(package_id)
        en_route.append(package)
    truck.packages.clear()

    # sorts the packages from en route
    while len(en_route) > 0:
        next_address = 2000
        next_package = None
        for package in en_route:
            if distance_calculation(convert_addresses(truck.address), convert_addresses(package.address)) <= next_address:
                next_address = distance_calculation(convert_addresses(truck.address), convert_addresses(package.address))
                next_package = package

        next_package.truck_number = truck.truck_number
        truck.packages.append(next_package.package_id)
        en_route.remove(next_package)

        # adds milage based on next address distance then assigns next address
        truck.milage += next_address
        truck.address = next_package.address

        #updates departure and delivery time based on truck objects time
        truck.time += datetime.timedelta(hours=next_address / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.departure_time

# load truck objects
truck_delivery(truck1)
truck_delivery(truck2)

# ensures that at least one driver has returned before departure time of truck 3
driver_free = min(truck1.time, truck2.time)
truck3.departure_time = max(truck3.departure_time, driver_free)
truck_delivery(truck3)

# prints the hashtable with headers and adjustable column widths for easy reading
def print_package_hashtable(packages_hashtable):
    headers = ["ID", "Address", "City", "State", "Zip Code", "Delivery Deadline", "Weight", "Status", "Delivery Time", "Truck Number"]
    widths = [5, 40, 20, 10, 10, 20, 10, 15, 15, 10]

    header_row = ""
    for header, width in zip(headers, widths):
        header_row += f"{header:<{width}} "
    print(header_row)
    print("-" * len(header_row))

    for package_id in range(1, 41):
        package = packages_hashtable.get(package_id)
        row_values = [package.package_id, package.address, package.city, package.state,package.zip_code, package.delivery_deadline, package.weight, package.status, package.delivery_time, package.truck_number]

        row = ""
        for value, width in zip(row_values, widths):
            row += f"{str(value):<{width}} "
        print(row)

# main ui for user input
def main():

    # while loop so that unless the user selects option 4 the program will re prompt for inquires
    while True:

        # prints departure times and total milage of all trucks combined
        print("\nWelcome to On Time Postal")
        print("Truck 1 departed at:", truck1.departure_time)
        print("Truck 2 departed at:", truck2.departure_time)
        print("Truck 3 departed at:", truck3.departure_time)
        print("Milage for today's trucks are:", (truck1.milage + truck2.milage + truck3.milage), " miles.")

        # prompts user for input while rejecting invalid inputs
        user_input = input("What would you like to do?"
                       "\n 1 - View all package information"
                       "\n 2 - View all packages' delivery status at a given time"
                       "\n 3 - View an individual package's information"
                       "\n 4 - Exit\n")

        # option one will print a string of all the initial package information
        if user_input == '1':
            print_package_hashtable(packages_hashtable)

        # option 2 prints a string of all package information at a given time
        elif user_input == '2':
            try:
                time_input = input("At what time would you like to check? Please enter in HH:MM format\n")
                (hh, mm) = time_input.split(":")
                check_time = datetime.timedelta(hours = int(hh), minutes= int(mm))
                for package_id in range(1, 41):
                    package = packages_hashtable.get(package_id)
                    package.get_status(check_time)
                print_package_hashtable(packages_hashtable)

            except ValueError:
                print("Please enter a valid time\n")

        # option three first prompts for a package ID then prompts for time to check the package information at
        elif user_input == '3':
            try:
                package_id = input("What package would you like to check? Please enter package ID\n")
                time_input = input("At what time would you like to check? Please enter in HH:MM format\n")
                (hh, mm) = time_input.split(":")
                check_time = datetime.timedelta(hours = int(hh), minutes= int(mm))
                package = packages_hashtable.get(int(package_id))
                package.get_status(check_time)
                print(str(package))

            except ValueError:
                print("Please enter a valid package ID and time.\n")

        # option for breaks out of the while loop and ends the program
        elif user_input == '4':
            print("Thank you for your time")
            break
        else:
            print("Please enter a valid input")

# runs the program main()
if __name__ == "__main__":
    main()
