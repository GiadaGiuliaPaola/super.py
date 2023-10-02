import csv 
from datetime import datetime
from create_inventory import read_inventory

iventory_file='inventory_file.csv'

# calculate if a product is expired or not and check if the inventory file have some expire product
def is_expired(date_string, inventory_file):
    date = datetime.strptime(date_string, '%Y-%m-%d')
    expired_items = []

    with open('inventory_file.csv', 'r') as csv_file:
            csv_reader =csv.reader(csv_file)
            next(csv_reader, None)

            for item in csv_reader:
                product_name = item[0]
                expiration_date = item[3]

                if not expiration_date:
                    continue

                expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d')

                if expiration_date <= date:
                    expired_items.append(
                        f"{product_name} expired on date: {expiration_date.strftime('%Y-%m-%d')}")

    return expired_items


def check_expired_items(date, inventory_file):
    expired_items = is_expired(date, inventory_file)

    if expired_items:
        for item in expired_items:
            print(item)
    else:
        print("No items have expired.")


