import csv
import tabulate
from datetime import datetime, timedelta
from generate_id import generate_product_id

inventory_file = 'inventory_file.csv'
#CREATE_INVENTORY
def create_inventory_csv():
    header = ['Product Name', 'Count', 'Buy Price', 'Expiration Date', 'ID number']
    product_id = generate_product_id()
    inventory = [
        ['Orange', 1, 0.8, '2024-01-01',product_id],
        ['Apple', 2, 1.2, '2024-02-01',product_id],
        ['Bruxell Sprout', 1, 3.3, '2024-03-01',product_id],
    ]

    with open(inventory_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header) 
        csv_writer.writerows(inventory)


def read_inventory(inventory_file):
    with open(inventory_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        inventory = [row for row in csv_reader]

    table = tabulate.tabulate(inventory, headers='firstrow', tablefmt='pipe')
    return table


def print_inventory(table):
    print(table)

