# Ken Conner
# Student ID - 011062828

from HashTable import *
from Package import *
from Truck import *

import datetime
import csv


def main():

    # Reads in distances from csv file
    with open('distance_table.csv', 'r') as distance_file:
        reader = csv.reader(distance_file)
        distances_table = list(reader)

    # Reads in package information from csv file
    with open('package_table.csv', 'r') as package_file:
        reader = csv.reader(package_file)
        packages_table = list(reader)

    # Reads in a list of addresses from a csv file to create easily addressable indexes for each package's address
    with open('address_indexes.csv', 'r') as index_file:
        reader = csv.reader(index_file)
        address_indexes = list(reader)
        address_indexes_list = []
        for address in address_indexes:
            address_indexes_list.append(address[0])

    # Creates a hash table with 40 empty indexes for package objects
    packages_hash_table = HashTable(40)

    # Assigns package IDs to each truck which will be used to assign each trucks load of packages
    truck1_package_load = [14, 15, 16, 34, 20, 21, 31, 40, 19, 1, 7, 29, 30, 37, 13, 39]
    truck2_package_load = [18, 12, 23, 11, 36, 27, 35, 38, 9, 8, 10, 5, 3]
    truck3_package_load = [25, 26, 24, 32, 6, 17, 4, 2, 33, 28, 22]

    # Iterates through package table, previously read from csv file, and creates package objects for each entry in the
    # table.  Assigns a delivery address index for each package by checking the packages delivery address against the
    # address indexes list created from the address indexes csv file.
    # Each package object is inserted into the package hash table using the packages ID number as a key.
    # A sequence of if statements then assigns a departure time based on the trucks package load list that the packages
    # ID falls in.
    for package in packages_table:
        new_package = Package(int(package[0]), package[1], package[2], package[3], package[4], package[5],
                              package[6], package[7])
        new_package.set_address_index(address_indexes_list)
        packages_hash_table.insert_item(new_package.pid, new_package)
        if new_package.pid in truck1_package_load:
            new_package.departure_time = datetime.timedelta(hours=8)
        elif new_package.pid in truck2_package_load:
            new_package.departure_time = datetime.timedelta(hours=10, minutes=20)
        elif new_package.pid in truck3_package_load:
            new_package.departure_time = datetime.timedelta(hours=9, minutes=5)

    # Creates three truck objects with pre-specified package loads and assigned departure times
    truck1 = Truck(18.0, 0.0, truck1_package_load, datetime.timedelta(hours=8), datetime.timedelta(hours=8))
    truck2 = Truck(18.0, 0.0, truck2_package_load, datetime.timedelta(hours=10, minutes=20),
                   datetime.timedelta(hours=10, minutes=20))
    truck3 = Truck(18.0, 0.0, truck3_package_load, datetime.timedelta(hours=9, minutes=5),
                   datetime.timedelta(hours=9, minutes=5))

    # Function to deliver packages for a truck object.  Uses nearest neighbor algorithm to check a trucks load for the
    # package with the next closest delivery address.  Moves truck index to next closest address and adds both time and
    # mileage required for the move.  Checks truck's carried packages for delivery address indexes matching the truck's
    # current location index.  All packages with a delivery index matching the current location index are removed and
    # their delivery time is updated to match the current time tracked by the truck.  After emptying the trucks package
    # load list, the truck returns to the hub and calculates its final mileage and time.
    def deliver_packages(truck):
        while len(truck.packages) > 0:
            min_distance = 100.0              # Assigns an initial min distance greater than any value in distance table
            next_delivery_index = 0
            for package_id in truck.packages:
                # Checks for min distance of one of the trucks packages in distance table. If the value is empty, the
                # indexes are swapped and rechecked
                truck_package = packages_hash_table.get_item(package_id)
                if distances_table[truck_package.address_index][truck.locationIndex] == '':
                    distance = float(distances_table[truck.locationIndex][truck_package.address_index])
                else:
                    distance = float(distances_table[truck_package.address_index][truck.locationIndex])

                # If the packages distance is nearer than the previous closest package, the min distance is set to the
                # new packages distance and the next delivery index is updated to the new packages address index
                if distance <= min_distance:
                    min_distance = distance
                    next_delivery_index = truck_package.address_index

            # Adds distance to next delivery to truck's mileage and adds the time required to travel to the next
            # delivery to the trucks current time.  Sets truck's current index to new delivery address index
            truck.miles += min_distance
            truck.current_time += datetime.timedelta(hours=float(min_distance/truck.speed))
            truck.locationIndex = next_delivery_index
            # Checks each packages carried by the truck. If the package's delivery address index matches the truck's
            # current address the package is considered delivered and removed from the package list after updating
            # its delivery time.
            for package_id in truck.packages:
                delivered_package = packages_hash_table.get_item(package_id)
                if delivered_package.address_index == truck.locationIndex:
                    delivered_package.delivery_time = truck.current_time
                    truck.packages.remove(int(package_id))

        # Calculates the return distance and travel time to hub after all packages are delivered and updates truck's
        # mileage, current time and location index.
        return_distance = float(distances_table[truck.locationIndex][0])
        truck.miles += return_distance
        truck.current_time += datetime.timedelta(hours=float(return_distance/truck.speed))
        truck.locationIndex = 0

    # Calls package delivery function for trucks 1 and 3
    deliver_packages(truck1)
    deliver_packages(truck3)

    # Accesses package 9 object from package hash table and updates address information with the correct address
    packages_hash_table.get_item(9).update_address('410 S State St', 'Salt Lake City', '84111')
    packages_hash_table.get_item(9).set_address_index(address_indexes_list)

    # Calls package delivery function for truck 2
    deliver_packages(truck2)

    # Loop for user interface.  User will be prompted to view truck mileage and single or all package details until
    # entering q to exit the loop.  Any invalid user inputs will generate a message to the user indicating the input
    # was not accepted and the loop returns to the start.
    while True:
        user_input = input("Type 'Individual' to search for a single package's details, 'All' to return all package's "
                           "details, 'Mileage' to view total truck mileage or 'q' to exit the program: ")
        user_input = user_input.lower()

        if user_input == 'q':
            break

        # If user enters mileage total truck mileage is added together and returned with at most 2 decimal places
        elif user_input == 'mileage':
            print(f"Total truck mileage: {truck1.miles + truck2.miles + truck3.miles:.2f}")

        # If user enters individual prompts for a package id and time are given and corresponding packages information
        # and delivery status are returned.  If the user entered time is after the packages delivery time, the delivery
        # time of the package is returned as well.
        elif user_input == 'individual':
            try:
                search_package = int(input("Enter a package id to search for: "))
                if 0 < search_package <= 40:
                    search_package = packages_hash_table.get_item(search_package)
                    search_hour = int(input("Enter an hour: "))
                    search_minute = int(input("Enter a minute: "))
                    if 0 <= search_hour < 24 and 0 <= search_minute < 60:   # Input validation for user search time
                        search_time = datetime.timedelta(hours=search_hour, minutes=search_minute)
                        search_package.calc_status(search_time)
                        print(search_package)

                    else:
                        print("Invalid time.")
                        continue
                else:
                    print("Invalid package id.")
                    continue
            except Exception:
                print("Invalid input.")

        # If user enters all the interface prompts the user to enter a specific time and returns all packages
        # information and status at the specified time.  The user entered time is used to set each packages status
        # before package information is returned.  Packages delivered before the user entered time will display the
        # packages time of delivery.
        elif user_input == 'all':
            try:
                search_hour = int(input("Enter an hour: "))
                search_minute = int(input("Enter a minute: "))
                if 0 <= search_hour < 24 and 0 <= search_minute < 60:
                    search_time = datetime.timedelta(hours=search_hour, minutes=search_minute)
                    for i in range(1, 41):
                        packages_hash_table.get_item(i).calc_status(search_time)
                        print(packages_hash_table.get_item(i))
                else:
                    print("Invalid time.")
            except Exception:
                print("Invalid input.")

        else:
            print('Invalid input.')


if __name__ == "__main__":
    main()
