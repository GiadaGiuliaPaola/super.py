# SUPERPY -A GUIDE TO USE IT

## TIME TRAVEL

***CLI*** advance / days
`python super.py advance 1`
return > Advanced the internal day by 1 days. New day is: 2023-09-29

***CLI*** go-back / days
`python super.py go-back 1`
Going back in time by 1 days. The date today is 2023-09-28
## BUY A PRODUCT

**CLI**: _buy / name of the product / quantity / price / expire-date_

`python super.py buy Apple 10 0.5 2023-12-31`
return > You bought 10 Apple.

-save the item on [bought.cvs] with the date of acquisition and add a unique identity number >
Bought Date,Product Name,Count,Cost Price,Expiration Date,ID number
-add the item on the inventory_file.csv > Product Name,Count,Buy Price,Expiration Date, ID number

You can check the report of how many product you bought today or previous days:

**CLI** : *bought_report/ --today or --days-ago=days_*

`python super.py bought_report --today bought_file.csv`

`python super.py bought_report --days-ago=3 bought_file.csv`

---

## SELL A PRODUCT

**CLI**: *sell / name of the product / quantity / selling price*

`python super.py sell Apple 3`

-if the product is available return > You sold 3 Apple.
If the product is not available return > Product Apple is not available.

-save the item on [sold.csv] with the date of selling, the price with the surplus of a markup 0f 50% of the cost price and the id of the item >
Sell Date,Product Name,Count,Sell Price,Expiration Date,ID number
-remove the item from the [inventory_file.csv]

You can check the report of how many product you sold today or previous days:

**CLI**: *sold_report / --today or --days-ago=days*

`python super.py sold_report --today sold_file.csv`

`python super.py sold_report --days-ago=1 sold_file.csv`

---

## INVENTORY FILE

All the product are getting update from the moment you buy or sell a product,
to know what you have in your supermarket you can print the inventory_file:

**CLI**: *inventory / --now*

`python super.py inventory --now inventory_file.csv`

return > inventory_file in a tabulate

---

## REVENUE

To have the sum of the items you sold in a certain date:

If you want to check the revenue of today:
**CLI**: *revenue / --today*

`python super.py revenue sold.csv --today`

-return> Today's revenue so far: 0

If is a previous date:
**CLI**: *revenue/ --date YYYY-MM-DD*

`python super.py revenue sold.csv --date 2023-09-18`

-return> Revenue from 2023-09-18: 0

---

## PROFIT

Is given by the sell price (price+markup) multiplied for the items sold.

If you want to check the profit of today:
**CLI**: *profit / --today*

`python super.py profit sold.csv --today`

-return> Today's profit so far: 0

If is a previous date:
**CLI**:* profit/ --date YYYY-MM-DD*

`python super.py profit sold.csv --date 2023-09-18`

return> Profit from 2023-09-18: 0

---

## CHECK IF EXPIRED
**CLI** check_expired / inventory-file / date to check

`python super.py check_expired --inventory_file inventory.csv --date 2021-12-31`

return> No items have expired.
if an item is expired return> Product_name expired on date: expiration_date

---

## MATPLOT
**CLI**:*matplot file /  day you want to check / sold file*

`python matplot_graph.py --today --sold-file sold.csv`

return > A graph containing how many items as been selling during a day, is calculated on the revenue 

