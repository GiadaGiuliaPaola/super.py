import csv
import tabulate
from datetime import datetime, timedelta

sold_file = 'sold.csv'
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
            if item_date.date() == target_date.date():
                total_revenue += float(row[2])  

    return total_revenue

def read_revenue(args):
    total_revenue = calculate_revenue(args)

    if args.today:
        print(f"Today's revenue so far: {total_revenue}")
    elif args.date:
        print(f"Revenue from {args.date}: {total_revenue}")

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
            if item_date.date() == target_date.date():
                total_profit += (float(row[3])*float(row[2]) ) 

    return total_profit


def read_profit(args):
    total_profit = calculate_profit(args)

    if args.today:
        print(f"Today's profit so far: {total_profit}")
    elif args.date:
        print(f"Profit from {args.date}: {total_profit}")
