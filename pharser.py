import argparse
from add_file import add_product, read_bought, print_bought
from remove_file import remove_product, read_sold, print_sold
from create_inventory import read_inventory, print_inventory
from revenue_profit import read_revenue, read_profit
from expired_file import check_expired_items

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