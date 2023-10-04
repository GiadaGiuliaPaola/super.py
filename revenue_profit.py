import csv
from datetime import datetime, timedelta

current_day_file = r'current_day.txt'
sold_file = 'sold.csv'


"""revenue work on today or a given day in the past,
check the sold file and return the selling price * items sold"""
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


"""profit calculate the total cost on the bought file and
again the revenue and return the profit made in a day"""
#CALCULATE THE PROFIT PER DAY
def calculate_profit(args):
    target_date = None

    if args.today:
        target_date = datetime.today()
    elif args.date:
        target_date = datetime.strptime(args.date, "%Y-%m-%d")

    if target_date is None:
        print("Invalid date format.")
        return 0  

    total_selling_price=0
    total_cost = 0


    # Read and calculate the cost from the bought.csv file
    with open('bought.csv', 'r') as cost_file:
        reader = csv.reader(cost_file)
        next(reader)  # Skip header row
        for row in reader:
            purchase_date = datetime.fromisoformat(row[0])
            if purchase_date.date() == target_date.date():
                cost_price = float(row[3])  # take the cost price
                count = int(row[2])  # Take the quantity
                
                total_cost += cost_price * count  # Calculate total cost for this entry
               

#read the sold file to get the selling price
    with open('sold.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            item_date = datetime.fromisoformat(row[0]) 
            if item_date.date() == target_date.date():
                selling_price = float(row[3])  # take the selling price
                count = int(row[2])
                
                total_selling_price += selling_price * count 

    total_profit = total_selling_price - total_cost  # Calculate profit by subtracting total cost from revenue
    return total_profit
    


def read_profit(args):
    total_profit = calculate_profit(args)

    if args.today:
        print(f"Today's profit so far: {total_profit}")
    elif args.date:
        print(f"Profit from {args.date}: {total_profit}")
