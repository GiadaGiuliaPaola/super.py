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
        next(reader) #skip header row to avoid problems with reading data 
        for row in reader:
            item_date = datetime.fromisoformat(row[0]) 
            if item_date.date() == target_date.date():
                selling_price = float(row[3]) #take the selling price
                count = int(row[2])
                revenue = selling_price * count  # Calculate revenue for the item
                total_revenue += revenue 

    return total_revenue

#function to read the revenue from today or other dates
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

    total_revenue = calculate_revenue(args)
    total_cost = 0

    # read and calculating the cost from the bought.cvs file
    cost_price_data = {}
    with open('bought.csv', 'r') as cost_file:
        reader = csv.reader(cost_file)
        next(reader)  # Skip head row
        for row in reader:
            purchase_date = datetime.fromisoformat(row[0])
            if purchase_date.date() <= target_date.date():
                product_name = row[1] #take the product name
                cost_price = float(row[3])  # take the cost price
                if product_name in cost_price_data:
                    cost_price_data[product_name] += cost_price
                else:
                    cost_price_data[product_name] = cost_price

#read the sold file to get the selling price
    with open(args.sold_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            item_date = datetime.fromisoformat(row[0]) 
            if item_date.date() == target_date.date():
                selling_price = float(row[3])  # take the selling price
                count = int(row[2])
                # Check if the product name is in the cost_price_data dictionary
                if product_name in cost_price_data:
                    cost_price = cost_price_data[product_name]
                    total_cost += cost_price * count  # Calculate total cost for the item

    profit = total_revenue - total_cost  # Calculate profit by removing total cost from revenue
    return profit


def read_profit(args):
    total_profit = calculate_profit(args)

    if args.today:
        print(f"Today's profit so far: {total_profit}")
    elif args.date:
        print(f"Profit from {args.date}: {total_profit}")
