import csv
import tabulate
from datetime import datetime, timedelta
from generate_id import generate_product_id
from read_day import read_current_day


current_day_file = r'C:\Users\marti\Desktop\Winc\superpy\current_day.txt'
inventory_file = 'inventory_file.csv'

# ADD A PRODUCT FUNCTION
def add_product(product_name, count, buy_price, expiration_date):
    product_id = generate_product_id()  # generate unique id for the product
    # get today date as bought date for the product
    bought_date = datetime.now().strftime('%Y-%m-%d')

# Check if the product is expired
    if expiration_date <= bought_date:
        print(f"Sorry, the product is expired! You can't purchase it")
        return

# read the inventory file to check row by row
    with open(inventory_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)

# add the items count if the product name matches
    for row in rows:
        if row[0] == product_name:
            row[1] = str(int(row[1]) + int(count))
            break

# write  new item on the inventory file
    with open(inventory_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)

    with open(inventory_file, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([product_name, count, buy_price,
                        expiration_date, product_id])

# write new item on the bought file with the bought date
    with open('bought.csv', 'a', newline='') as bought_file:
        writer = csv.writer(bought_file)
        if bought_file.tell() == 0:
            writer.writerow(['Bought Date', 'Product Name', 'Count',
                            'Cost Price', 'Expiration Date', 'ID number'])
        writer.writerow([bought_date, product_name, count,
                        buy_price, expiration_date, product_id])

    print(f'You bought {count} {product_name}.')

# this function help to read the items that have been bought in a certain date


def read_bought(bought_file, days_ago=0, current_date=None):
    
    if current_date is None:
        current_date = read_current_day(current_day_file)

    choose_date = datetime.now() - timedelta(days=days_ago)
    choose_date_str = current_date

    item_bought_in_date = []

    with open('bought.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        for row in csv_reader:
            if row[0] == choose_date_str:
                item_bought_in_date.append(row)

    if not item_bought_in_date:
        return f"No items bought on {choose_date_str}."


# print the result in a table for redability
    table_bought = tabulate.tabulate(item_bought_in_date, headers=[
                                     'Bought_date', 'Product Name', 'Count', 'Bought Price', 'Expiration Date', 'ID number'], tablefmt='pipe')
    return table_bought


def print_bought(table_bought):
    print(table_bought)
