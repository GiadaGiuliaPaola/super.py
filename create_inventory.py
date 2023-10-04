import csv
from collections import defaultdict
import tabulate

"""This function is used to generate a inventory
file csv taking in consideration ONLY the name of the product and the expiracy day.
Is only used to check how many items are still in stock, not the cost (that is set to 0.00)"""

def create_inventory_csv(bought_file, sold_file, output_file):
    # Create dictionaries to store bought and sold items
    bought_items = defaultdict(int)
    sold_items = defaultdict(int)

    # Read and process the bought items
    with open(bought_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            product_name = row['Product Name']
            count = int(row['Count'])
            expiration_date = row['Expiration Date']
            bought_items[(product_name, expiration_date)] += count

    # Read and process the sold items
    with open(sold_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            product_name = row['Product Name']
            count = int(row['Count'])
            expiration_date = row['Expiration Date']
            sold_items[(product_name, expiration_date)] += count

    # Calculate the remaining count in inventory
    inventory = {}
    for (product_name, expiration_date), count in bought_items.items():
        sold_count = sold_items.get((product_name, expiration_date), 0)
        remaining_count = count - sold_count

        # Create an inventory entry for this product and expiration date
        if remaining_count >= 0:
            inventory[(product_name, expiration_date)] = {
                'Count': remaining_count,
                'Cost Price': row.get('Cost Price', '0.00'),  # Replace with the actual Cost Price or zero
                'ID number': row.get('ID number', 'inv1')  # Replace with the actual ID number or "inv1"
            }

    # Write the result to the output CSV file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Product Name', 'Count', 'Cost Price', 'Expiration Date', 'ID number']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for (product_name, expiration_date), item_data in inventory.items():
            writer.writerow({
                'Product Name': product_name,
                'Count': item_data['Count'],
                'Cost Price': item_data['Cost Price'],
                'Expiration Date': expiration_date,
                'ID number': item_data['ID number']
            })

# Example usage:
create_inventory_csv('bought.csv', 'sold.csv', 'inventory_file.csv')

#CREATE AND PRINT A TABLE FOR REDABILITY
def read_inventory(inventory_file):
    with open(inventory_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        inventory = [row for row in csv_reader]

    table = tabulate.tabulate(inventory, headers='firstrow', tablefmt='pipe')
    return table


def print_inventory(table):
    print(table)
