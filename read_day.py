import os
import datetime

current_day_file = r'current_day.txt'

"""create a new day file that will be set as today,
and can be used on assotiation with
read the bought or the sold file"""

# Function to read the current day from a text file or return the current system date
def read_current_day(filename):
    try:
        with open(filename, 'r') as file:
            current_day_str = file.read().strip()
            if current_day_str:
                try:
                    return datetime.datetime.strptime(current_day_str, '%Y-%m-%d').date()
                except ValueError:
                    pass
    except FileNotFoundError:
        pass
    # If the file is empty or has an invalid date, return the current system date
    return datetime.date.today()

# Function to save the current day to a text file
def save_current_day(filename, current_day):
    with open(filename, 'w') as file:
        file.write(current_day.strftime('%Y-%m-%d'))

# Function to advance time by a specified number of days
def advance_time(days_to_advance):
    current_day = read_current_day(current_day_file)  
    new_day = current_day + datetime.timedelta(days=days_to_advance)
    save_current_day(current_day_file, new_day)  
    message = f"Advanced the internal day by {days_to_advance} days. New day is: {new_day}"
    print(message)
    return message 

# Function to go back in time by a specified number of days
def go_back_in_time(days_to_go_back):
    current_day = read_current_day(current_day_file) 
    new_day = current_day - datetime.timedelta(days=days_to_go_back)
    save_current_day(current_day_file, new_day)  
    message = f"Going back in time by {days_to_go_back} days. The date today is {new_day}"
    print(message)
    return message
