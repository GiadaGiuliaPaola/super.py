# Imports
import argparse
import csv
import tabulate
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import uuid

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
inventory_file = 'inventory_file.csv' 
date_file = 'date_file.txt'
sold_file = 'sold.csv'
bought_file = 'bought.csv'

#id generator


def generate_product_id():
    new_id = str(uuid.uuid4())[-4:] 
    return new_id

# ADD A PRODUCT FUNCTION
def add_product(product_name, count, buy_price, expiration_date):
    product_id = generate_product_id()
    bought_date = datetime.now().strftime('%Y-%m-%d')

    with open(inventory_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        rows=list(reader)

    for row in rows:
            if row[0] == product_name:
                row[1] = str(int(row[1]) + int(count))
                break    
    

    with open(inventory_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)

    with open(inventory_file, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([product_name, count, buy_price, expiration_date, product_id])

    with open('bought.csv', 'a', newline='') as bought_file:
            writer = csv.writer(bought_file)
            if bought_file.tell() == 0: 
                writer.writerow(['Bought Date', 'Product Name', 'Count', 'Cost Price', 'Expiration Date', 'ID number'])
            writer.writerow([bought_date, product_name, count, buy_price, expiration_date, product_id])
    
    print(f'You bought {count} {product_name}.')

def read_bought(bought_file, days_ago=0):
    choose_date = datetime.now() - timedelta(days=days_ago)
    choose_date_str = choose_date.strftime('%Y-%m-%d')
  
    item_bought_in_date = []

    with open('bought.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        for row in csv_reader:
            if row[0] == choose_date_str:
                item_bought_in_date.append(row)

    if not item_bought_in_date:
        return f"No items bought on {choose_date_str}."

    table_bought = tabulate.tabulate(item_bought_in_date, headers=['Bought_date', 'Product Name', 'Count', 'Bought Price'], tablefmt='pipe')
    return table_bought

def print_bought(table_bought):
    print(table_bought)

#REMOVE PRODUCT FUNCTION
def remove_product(product_name, count):
    product_id = generate_product_id(product_name)
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

#REVENUE SOLD PRODUCTS
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

    table_sold = tabulate.tabulate(item_sold_in_date, headers=['sell_date', 'Product Name', 'Count', 'Sell Price'], tablefmt='pipe')
    return table_sold

def print_sold(table_sold):
    print(table_sold)

#CALCULATE THE REVENUE
def calculate_revenue(args):
    target_date = None

    if args.today:
        target_date = datetime.today()
    elif args.date:
        target_date = datetime.strptime(args.date, "%Y-%m-%d")

    if target_date is None:
        print("Invalid date format, please insert the date in YYYY-MM-DD.")
        return 0  

    total_revenue = 0

    with open(args.sold_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            item_date = datetime.fromisoformat(row[0]) 
            if item_date == target_date:
                total_revenue += float(row[2])  

    return total_revenue


def read_revenue(args):
    total_revenue = calculate_revenue(args)

    if args.today:
        print(f"Today's revenue so far: {total_revenue}")
    elif args.date:
        print(f"Revenue from {args.date}: {total_revenue}")
    else:
        print(f"Yesterday's revenue: {total_revenue}")

#CALCULATE THE PROFIT PER DAY
def calculate_profit(args):
    target_date = None

    if args.today:
        target_date = datetime.today()
    elif args.date:
        target_date = datetime.strptime(args.date, "%Y-%m-%d")

    if target_date is None:
        print("Invalid date format or missing date argument.")
        return 0  

    total_profit = 0

    with open(args.sold_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            item_date = datetime.fromisoformat(row[0]) 
            if item_date == target_date:
                total_profit += (float(row[3])*float(row[2]) ) 

    return total_profit


def read_profit(args):
    total_profit = calculate_profit(args)

    if args.today:
        print(f"Today's profit so far: {total_profit}")
    elif args.date:
        print(f"Profit from {args.date}: {total_profit}")
    else:
        print(f"Yesterday's profit: {total_profit}")


def plot_revenue(sold_items):

    dates = set(item[1] for item in sold_items)
    revenue_data = {}
    for date in dates:
        revenue_data[date] = calculate_revenue(sold_items, date)

    dates = list(revenue_data.keys())
    revenue = [revenue_data[date] for date in dates]

    fig, ax = plt.figure()
    plt.bar(dates, revenue)
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.title("Revenue Report")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

plot_revenue(sold_file)


#CREATE_INVENTORY
def create_inventory_csv():
    header = ['Product Name', 'Count', 'Buy Price', 'Expiration Date', 'ID number']
    product_name=''
    count=0
    buy_price=0
    expiration_date= datetime
    product_id = generate_product_id(product_name)
    inventory = [
        [product_name, count, buy_price, expiration_date, product_id]
        ['Orange', 1, 0.8, '2024-01-01',3],
        ['Apple', 2, 1.2, '2024-02-01',1],
        ['Bruxell Sprout', 1, 3.3, '2024-03-01',4],
    ]

    with open(inventory_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)  # Write the header row
        csv_writer.writerows(inventory)    # Write the data rows


def read_inventory(inventory_file):
    with open(inventory_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        inventory = [row for row in csv_reader]

    table = tabulate.tabulate(inventory, headers='firstrow', tablefmt='pipe')
    return table


def print_inventory(table):
    print(table)

# calculate if a product is expired or not
def is_expired(date_string, inventory_file):
    date = datetime.strptime(date_string, '%Y-%m-%d')
    inventory = read_inventory(inventory_file)
    expired_items = []

    for item in inventory:
        product_name = item[0]
        expiration_date = item[3]

        if not expiration_date:
            continue

        expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d')

        if expiration_date <= date:
            expired_items.append(
                f"{product_name} expired on date: {expiration_date.strftime('%Y-%m-%d')}")

    return expired_items


def check_expired_items(args):
    date_string = args.date_string
    inventory_file = args.inventory_file

    if not inventory_file:
        print("Inventory file path is not provided.")
        return

    inventory = read_inventory(inventory_file)

    if inventory is None:
        print("Failed to read inventory data.")
        return

    expired_items = is_expired(date_string, inventory)

    if expired_items:
        for item in expired_items:
            print(item)
    else:
        print("No items have expired.")


def main():
# Create a CLI parser e subparser
    parser = argparse.ArgumentParser(description='Superpy command line')
    subparsers = parser.add_subparsers(
        dest='command', help='Available commands')

# ADD PRODUCT WHEN PURCHASED
    add_parser = subparsers.add_parser(
        'buy', help='Add the product you buy on the inventory')
    add_parser.add_argument(
        'product_name', help='Name of the product to add')
    add_parser.add_argument('count', help='Count of the product')
    add_parser.add_argument('buy_price', help='Buy price of the product')
    add_parser.add_argument(
        'expiration_date', help='Expiration date YYYY-MM-DD ')
    add_parser.set_defaults(func=add_product)

#REMOVE PRODUCT WHEN SOLD
    remove_parser = subparsers.add_parser(
        'sell', help='Remove the product you sold from the inventory')
    remove_parser.add_argument(
        'product_name', help='Name of the product to remove')
    remove_parser.add_argument('count', help='Count of the product')
    remove_parser.set_defaults(func=remove_product)

# display the inventory
    report_parser = subparsers.add_parser(
        'inventory', help='Display the inventory')
    report_parser.add_argument(
        'inventory_file', default='inventory_file.csv', help='Path to the inventory CSV file')
    report_parser.add_argument(
        '--now', help='Include this flag to display the inventory', action='store_true')
    report_parser.set_defaults(func=read_inventory)

#display sold report
    report_parser = subparsers.add_parser(
        'sold_report', help='Display all the items sold')
    report_parser.add_argument(
        'sold_file', default='sold.csv', help='Path to the sold items CSV file')
    report_parser.add_argument(
        '--today', help='Include this flag to display the item sold today', action='store_true')
    report_parser.add_argument(
    '--days-ago', type=int, default=0, help='Specify the number of days ago to check what as been previously sold.')
    report_parser.set_defaults(func=read_sold)

#display bought report
    bought_parser = subparsers.add_parser(
        'bought_report', help='Display all the items sold')
    bought_parser.add_argument(
        'bought_file', default='bought.csv', help='Path to the sold items CSV file')
    bought_parser.add_argument(
        '--today', help='Include this flag to display the item sold today', action='store_true')
    bought_parser.add_argument(
    '--days-ago', type=int, default=0, help='Specify the number of days ago to check what as been previously sold.')
    bought_parser.set_defaults(func=read_bought)
 
#display revenue report
    report_parser = subparsers.add_parser('revenue', help='Display revenue')
    report_parser.add_argument('sold_file', default='sold.csv', help='Path to the sold items CSV file')
    report_parser.add_argument('--today', help='Include this flag to display today revenue', action='store_true')
    report_parser.add_argument('--date', help='Specify a date in YYYY-MM format.')
    report_parser.set_defaults(func=read_revenue)

 
#display profit report
    profit_parser = subparsers.add_parser('profit', help='Display profit')
    profit_parser.add_argument('sold_file', default='sold.csv', help='Path to the sold items CSV file')
    profit_parser.add_argument('--today', help='Include this flag to display today profit', action='store_true')
    profit_parser.add_argument('--date', help='Specify a date in YYYY-MM format.')
    profit_parser.set_defaults(func=read_profit)

# check if expired
    check_expired_parser = subparsers.add_parser(
        'check_expired', help="Check if item is expired")
    check_expired_parser.add_argument(
        '--inventory_file', default='inventory_file.csv', help='Path to the inventory CSV file')
    check_expired_parser.add_argument(
        '--date', type=str, help="Date in YYYY-MM-DD format")
    check_expired_parser.set_defaults(func=check_expired_items)

    args = parser.parse_args()



    if hasattr(args, 'func'):
        if args.command == 'buy':
            args.func(args.product_name, args.count,
                      args.buy_price, args.expiration_date)
        elif args.command == 'sell':
            args.func(args.product_name, args.count)

        elif args.command == 'inventory':
            inventory = args.func(args.inventory_file)
            if args.now:
                print_inventory(inventory)
        
        elif args.command == 'sold_report':
            inventory = args.func(args.sold_file)
            if args.today:
                table_sold = read_sold(args.sold_file)
                print_sold(table_sold) 
            elif args.days_ago is not None:
                table_sold = read_sold(args.sold_file, days_ago=args.days_ago)
                print_sold(table_sold)
            else:
                 table_sold = read_sold(args.sold_file)
                 print_sold(table_sold)

        elif args.command == 'bought_report':
            inventory = args.func(args.bought_file)
            if args.today:
                table_bought = read_bought(args.bought_file)
                print_bought(table_bought) 
            elif args.days_ago is not None:
                table_bought = read_bought(args.bought_file, days_ago=args.days_ago)
                print_bought(table_bought)
            else:
                 table_bought = read_bought(args.bought_file)
                 print_bought(table_bought)
                 
        elif args.command == 'revenue':
            read_revenue(args)
        elif args.command == 'profit':
            read_profit(args)
        

        elif args.command == 'check_expired':
            args.func(args)


if __name__ == "__main__":
    main()
