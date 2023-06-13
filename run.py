import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get figures of sales from a user.
    A while loop will keep requesting data untill the user
    enters valid data. Data must be 6 figues and must be
    seperated by commas.
    """
    while True:
        print("Please enter sales data from the last market")
        print("Data should be six figures seperated by commas")
        print("Example: 10, 20, 30, 40, 50, 60 \n")

        data_str = input("Enter your data here:\n")
    
        sales_data = data_str.split(",")
        
        if(validate_data(sales_data)):
            print("Data is valid")
            break
    return sales_data

def validate_data(values):
    """
    Inside the try, convert all strings into intergers. 
    If the string can't be converted to int raise an exception
    or if they aren't exactly 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
        f"Exactly 6 values required. Your provided {len(values)}")
    except ValueError as e:
        print(f"Invalid data: {e}. Please try again \n")
        return False

    return True

def update_worksheet(data, worksheet):
    """
    Receives data to be inserted to our worksheet
    Adds an additional row of data to relevan sheet.
    """
    print(f"Updating {worksheet} worksheet....\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.")

def calculate_surplus_data(sales_row):
    """
    Compare sales and stoc and calculate the surplus for each type.
    The surplus is defined as the sales figure subtracted from the stock:
    -postive surplus indicates waste
    -Negative surplus indicates extra made when stock was sold out
    """
    print("Calculating surplus data...") 
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def get_last_5_entries_sales():
    """
    Collects colums of data from sales worksheet,
    collecting the last 5 entries for each sandwich and returns
    the data as a list of list.
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    """
    Calculate the average of 5 last sales for each 
    item type and add 10%
    """

    print(f"Calculating next stock data..\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column)/len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data

def main():
    """
    Run all program functions
    """
    data = get_sales_data() 
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

print("Welcome to Sand Wiches Data Automation\n")
main()
