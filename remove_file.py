import csv
import tabulate
from datetime import datetime, timedelta
from generate_id import generate_product_id
from read_day import read_current_day

inventory_file = 'inventory_file.csv'

#REMOVE PRODUCT FUNCTION
def remove_product(product_name, count, selling_price):
    product_id = generate_product_id()
    sell_date = datetime.now().strftime('%Y-%m-%d') #get today date as selling date for the product

    with open(inventory_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)

    found = False # the item is declare not found
    updated_rows = []
    removed_rows = []
    removed_quantity = 0

 # Check if there are enough item in inventory to sell
    available_count = sum(int(row[1]) for row in rows if row[0] == product_name)
    if int(count) > available_count:
        print(f"Sorry, We only have {available_count} {product_name} available.")
        return

    for row in rows:
        if row[0] == product_name: #take product name in inventory file
           found = True
           if int(row[1]) <= int(count): # row[1] take count in inventory
                    removed_quantity += int(row[1])
                    removed_rows.append(row)
           else:
               row[1] = str(int(row[1]) - int(count))
               removed_quantity += int(count)
               removed_rows.append([row[0], count, row[2], row[3]])
        updated_rows.append(row)

    if found:
        with open(inventory_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(updated_rows)  
        
        with open('sold.csv', 'a', newline='') as sold_file:
            writer = csv.writer(sold_file)
            if sold_file.tell() == 0: 
                writer.writerow(['Sell Date', 'Product Name', 'Count', 'Sell Price', 'Expiration Date', 'ID number'])
            for removed_row in removed_rows:
                writer.writerow([sell_date] + removed_row + [product_id])  

        print(f'You sold {removed_quantity} {product_name}.')
    else:
        print(f'Product {product_name} is not available.')
    

# this function help to read the items that have been sell in a certain date
def read_sold(sold_file, days_ago=0, current_date=None):

    if current_date is None:
        current_date = read_current_day(current_day_file)

    choose_date = datetime.now() - timedelta(days=days_ago)
    choose_date_str = current_date
  
    item_sold_in_date = []

    with open('sold.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        for row in csv_reader:
            if row[0] == choose_date_str:
                item_sold_in_date.append(row)

    if not item_sold_in_date:
        return f"No items sold on {choose_date_str}."

    table_sold = tabulate.tabulate(item_sold_in_date, headers=['Sell date', 'Product Name', 'Count', 'Sell Price','Expiration Date', 'ID number'], tablefmt='pipe')
    return table_sold

def print_sold(table_sold):
    print(table_sold)