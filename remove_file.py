import csv
import tabulate
from datetime import datetime, timedelta
from generate_id import generate_product_id
from read_day import read_current_day

current_day_file = r'current_day.txt'
inventory_file = 'inventory_file.csv'

"""All of the functions that have to deal with a selling process:
 sell an item with a price, read how many items have been sold"""

def remove_product(product_name, count, selling_price):
    product_id = generate_product_id()
    sell_date = datetime.now().strftime('%Y-%m-%d')  # Get today's date as the selling date for the product
    inventory = []

    with open(inventory_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Read and store the header
        for row in csv_reader:
            inventory.append(row)


    found = False  # Declare the item as not found
    removed_quantities = {}  # Store removed quantities for each product_id

    # Check if there are enough items in inventory to sell
    available_count = sum(int(row[1]) for row in inventory if row[0] == product_name)
    if int(count) > available_count:
        print(f"Sorry, We only have {available_count} {product_name} available.")
        return

    updated_rows = []

    for row in inventory:
        if row[0] == product_name:
            found = True
            product_id = generate_product_id()  # Generate a unique product_id for each sell

            if int(row[1]) <= int(count):
                removed_quantities[product_id] = int(row[1])
                row[1] = '0'  # Set quantity to 0
            else:
                removed_quantities[product_id] = int(count)
                row[1] = str(int(row[1]) - int(count))

        updated_rows.append(row)

    if found:
        with open(inventory_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(updated_rows)

        with open('sold.csv', 'a', newline='') as sold_file:
            writer = csv.writer(sold_file)
            if sold_file.tell() == 0:
                writer.writerow(['Sell Date', 'Product Name', 'Count', 'Sell Price', 'Expiration Date', 'ID number'])
            for product_id, removed_quantity in removed_quantities.items():
                writer.writerow([sell_date, product_name, removed_quantity, selling_price, '2023-12-31', product_id])

        print(f'You sold {sum(removed_quantities.values())} {product_name}.')
    else:
        print(f'Product {product_name} is not available.')


# this function help to read the items that have been sell in a certain date, it also works with internal day
def read_sold(sold_file, days_ago=0, current_date=None):

    if current_date is None:
        current_date = read_current_day(current_day_file)

    choose_date = datetime.now() - timedelta(days=days_ago)
    choose_date_str = (current_date - timedelta(days=days_ago)).strftime('%Y-%m-%d')

  
    item_sold_in_date = []

    with open('sold.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        for row in csv_reader:
            if str(row[0]) == str(choose_date_str):
                item_sold_in_date.append(row)

    if not item_sold_in_date:
        return f"No items sold on {choose_date_str}."

    table_sold = tabulate.tabulate(item_sold_in_date, headers=['Sell date', 'Product Name', 'Count', 'Sell Price','Expiration Date', 'ID number'], tablefmt='pipe')
    return table_sold

def print_sold(table_sold):
    print(table_sold)