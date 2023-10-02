## Report three technical elements:

# INTERNAL CURRENT DAY
> Read_day.py rovides a set of functions for managing and manipulating a "current day" date stored in a text file. It primarily serves as a tool for simulating changes in time. The read_current_day function reads the current day from a specified text file or returns the system date if the file is empty or contains an invalid date format. The save_current_day function saves a given date back to the text file.

Two additional functions, advance_time and go_back_in_time, allow the user to manipulate the current day by advancing it forward or going back in time by a specified number of days, respectively. Each function updates the text file and provides feedback on the action taken. This script could be useful for scenarios that require managing a simulated timeline or date tracking.

# PHARSER WITH TIME TRAVEL:

-example bought report: 

`elif args.command == 'bought_report':
            inventory = args.func(args.bought_file)
            if args.today:
                table_bought = read_bought(args.bought_file)
                print_bought(table_bought) 
            elif args.days_ago is not None:
                table_bought = read_bought(args.bought_file, days_ago=args.days_ago)
                print_bought(table_bought)
            else:
                 table_bought = read_bought(args.bought_file)
                 print_bought(table_bought)`

> this pharser permits to check the bought inventory now or in the past, on testing I found that insert a date for checking the what I have sold yesterday and the day before was annoying so I choose a different approach: days-ago. In order to make it work I used datetime and timedelta(days = days_ago). I think is working for this code because is fast, intuitive and easy to check. I took inspiration from my previous job as retail supervisor, when it was important to check the sale of the week (for replenishment as example). I replicate the same logic for the sold report.
# REMOVE FILE

`def remove_product(product_name, count):``
    

> This function will found the item you want to sell, remove the file when sold from the inventory, register new file in a new cvs file name sold.csv, add a sell date to the item, register the sell price and also will stop the sale if the item is not available in the inventory. 

# MATPLOT_GRAPH

`def plot_revenue(args):
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

plot_revenue(args)`

> I dedicate a page with pharser to this function. From the command line it will show the graph with the function of the revenue. In order to make it work during my test I had to create an extra function called 'calculate_revenue' which with a pre insert dictionary with the needed values. The result is histogram of how many product where sold. The code is set to detect today and also previos date (such months or years ago), and to be able to access the data of the sold.csv file.