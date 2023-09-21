import argparse
import matplotlib.pyplot as plt
import csv
from datetime import datetime
from revenue_profit import calculate_revenue

#argaparse valid only for matplot_graph file
parser = argparse.ArgumentParser(description="Plot revenue data")

parser.add_argument("--today", action="store_true", help="Use today's date")
parser.add_argument("--date", type=str, help="Specify a date in YYYY-MM-DD format")
parser.add_argument("--sold-file", type=str, help="Path to the sold items CSV file")

args = parser.parse_args()

# function to define the data 
def calculate_revenue(args):
    target_date = None

    if args.today:
        target_date = datetime.today()
    elif args.date:
        target_date = datetime.strptime(args.date, "%Y-%m-%d")

    if target_date is None:
        print("Invalid date format, please insert the date in YYYY-MM-DD.")
        return {} 

    revenue_data = {
        datetime(2023, 9, 1): 1.0,
        datetime(2023, 9, 2): 3.0,
        datetime(2023, 9, 3): 8.0,
        datetime(2023, 9, 4): 15.0,
        datetime(2023, 9, 5): 9.0,
    }
    with open('sold.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            item_date = datetime.fromisoformat(row[0])
            if item_date.date() == target_date.date():
                total_revenue = float(row[2])
                revenue_data[item_date.date()] = total_revenue

    return revenue_data 

def plot_revenue(args):
    target_date = None

    if args.today:
        target_date = datetime.today()
    elif args.date:
        target_date = datetime.strptime(args.date, "%Y-%m-%d")

    if target_date is None:
        print("Invalid date format, please insert the date in YYYY-MM-DD.")
        return

    revenue = calculate_revenue(args)

    dates = list(revenue.keys())
    revenue_values = list(revenue.values())

    fig, ax = plt.subplots()
    ax.bar(dates, revenue_values)
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.title("Revenue Report")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

plot_revenue(args)
