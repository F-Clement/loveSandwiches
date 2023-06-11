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

        data_str = input("Enter your data here:")
    
        sales_data = data_str.split(",")
        
        if(validate_data(sales_data)):
            print("Data is valid")
            break
    return sales_data

def validate_data(values):
    """
    Inside the try, convert all strings into intergers. 
    If the string can't be converted to in raise an exception
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

def update_sales_worksheet(data):
    """
    Update sales work sheet by adding one new row with
    list data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")

data = get_sales_data() 
sales_data = [int(num) for num in data]
update_sales_worksheet(sales_data)