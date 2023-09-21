from datetime import datetime
from create_inventory import read_inventory

# calculate if a product is expired or not
def is_expired(date_string):
    date = datetime.strptime(date_string, '%Y-%m-%d')
    inventory = read_inventory('inventory_file.csv')
    expired_items = []

    if inventory is None:
        return expired_items

    for item in inventory:
        if len(item) < 4:
            continue

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
    expired_items = is_expired(args.date)

    if expired_items:
        for item in expired_items:
            print(item)
    else:
        print("No items have expired.")


