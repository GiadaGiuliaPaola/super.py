import csv
import tabulate
from datetime import datetime, timedelta
from generate_id import generate_product_id

inventory_file = 'inventory_file.csv'
#REMOVE PRODUCT FUNCTION
def remove_product(product_name, count):
    product_id = generate_product_id()
    sell_date = datetime.now().strftime('%Y-%m-%d')

    with open(inventory_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)

    found = False 
    updated_rows = []
    removed_rows = []
    removed_quantity = 0

    for row in rows:
        if row[0] == product_name:
           found = True
           if int(row[1]) <= int(count):
                    removed_quantity += int(row[1])
                    removed_rows.append(row)
                    # count -= int(row[1])
                    continue
           else:
               row[1] = str(int(row[1]) - int(count))
               removed_quantity += int(count)
               removed_rows.append([row[0], count, row[2], row[3]])
               cost_price = float(row[2])
               selling_price = cost_price * (1 + 50 / 100)
               removed_rows[-1][2] = selling_price
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


def read_sold(sold_file, days_ago=0):

    choose_date = datetime.now() - timedelta(days=days_ago)
    choose_date_str = choose_date.strftime('%Y-%m-%d')
  
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