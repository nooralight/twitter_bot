from datetime import datetime
import re

# Global Constants
## Values
MAX_ATTEMPTS = 3
CURRENT_YEAR = datetime.today().year

## Messages
SELECTION_MESSAGE = "Enter selection: "

## Errors
DOB_ERROR = "Date of Birth should follow the DD/MM/YYYY format."
PASSWORD_ERROR = "Password must start with letters, either '@' or '&', and end with digit(s)."
INVALID_SELECTION_ERROR = "Item not within valid menu options."
PASSWORD_EXIST_ERROR = "You cannot use one of your previous passwords."

# Global Variables
## Data Stores
users = []

# Main Functions
def main_selection():
    """Main function called to run the mobile ordering application."""
    while True:
        print_title("Welcome to the Mobile Ordering application")
        print("To start, select from the following options:\n1 - Sign Up\n2 - Sign In\n3 - Quit Application\n")

        selection_str = input(SELECTION_MESSAGE)

        # Checks validity of the provided selection
        if not selection_str.isdigit():
            print_error(INVALID_SELECTION_ERROR)
            continue

        # Checks which menu item is selected
        selection = int(selection_str)

        if selection == 1:
            # Invoke sign_up function
            sign_up()
        elif selection == 2:
            # Captures the sign_in return values of user record and a flag to determine
            # if login_reset_password() should be called.
            (user, to_reset) = sign_in()

            if user is not None and not to_reset:
                home(user)
        elif selection == 3:
            # Exits application
            print("Thank you for using the Mobile Ordering application.")
            break
        else:
            print_error(INVALID_SELECTION_ERROR)

def sign_up():
    # Constants
    LEGAL_AGE = 21

    print_title("Sign Up")
    print("To start with the registration process, please provide the following details:")

    while True:
        name = input("Please enter your name: ")
        address = input("Please enter your address or press enter to Skip.")
        mobile_number = input("Please enter your Mobile Number: ")
        
        password = input("Please enter your Password: ")
        confirm_password = input("Please enter your Password: ")
        dob = input("Please Enter your Date of Birth # DD/MM/YYYY (No Space) ")
        

        # Checks validity of Full Name (Consists of one first name and one last name)
        name_list = name.split(' ')

        if len(name_list) != 2:
            print_error("Valid Full Name must be provided (with First Name and Last Name).", True)
            continue

        # Checks validity of Mobile Number
        if not is_mobile(mobile_number):
            print_error("Mobile Number should be 10 digits starting with 0.", True)
            continue

        # Checks validity of Date of Birth
        if not is_dob(dob):
            print_error(DOB_ERROR, True)
            continue

        # Calculate age based on Date of Birth
        year = int(dob.split('/').pop())
        age = CURRENT_YEAR - year

        # Checks if user is eligible for sign up
        if age < LEGAL_AGE:
            print_error(f"You must be at least {LEGAL_AGE} years old to sign up.", True)
            continue

        if is_user_exists(mobile_number) is not None:
            print_error(f"User record with mobile number {mobile_number} already exists.", True)
            continue

        # Checks validity of Password
        if not is_password(password):
            print_error(PASSWORD_ERROR, True)
            continue

        # Checks validity of Confirm Password
        if confirm_password != password:
            print_error("Passwords do not match.", True)
            continue

        # Store user details in memory, then exits function
        store_user(name,address, mobile_number, dob, password)
        print("You have Successfully Signed up.")
        break

def sign_in():
    print_title("Sign In")

    attempts = MAX_ATTEMPTS
    to_reset = False

    while attempts > 0:
        username = input("Please enter your Username (Mobile Number): ")
        password = input("Please enter your password: ")

        # Checks if user exists on record
        #print(users)
        user = is_user_exists(username)

        if user is None:
            # User does not exist on record, thus force-exits function to return to main_selection()
            print_error("You have not signed up with this Mobile Number. Please sign up first.")
            break
        else:
            # Retrieves latest password (active) from list
            user_password = user[-1][-1]

            # Checks validity of Password
            if password != user_password:
                attempts -= 1
                to_retry = attempts > 0

                print_error(f"Password is incorrect. {attempts} attempt(s) left.", to_retry)
                continue
            else:
                print("You have successfully Signed in")
                break

    # Checks if user exhausted allowable attempts to sign in
    if attempts == 0:
        to_reset = True

    return (user, to_reset)

def home(user):
    while True:
        
        print(" Please Enter 2.1 to Start Ordering.\n Please Enter 2.2 to Print Statistics.\n Please Enter 2.3 or Logout.\n")

        selection_str = input(SELECTION_MESSAGE)

        # Checks validity of the provided selection
        if not selection_str.isdigit():
            print_error(INVALID_SELECTION_ERROR)
            continue

        choose = int(selection_str)

        if choose == 2.1:
            start_ordering(user)
        elif choose == 2.2:
            print_statistics(user)
            break
        elif choose == 2.3:
            break

# TODO
def start_ordering(user):
    pass
# TODO
def print_statistics(user):
    pass

# def logout(user):
#     pass


# Utility Functions
def is_mobile(mobile):
    """Checks whether mobile number is of valid format."""
    return re.match('^0([0-9]{9})$', mobile) is not None

def is_dob(dob):
    """Checks whether date of birth is of valid format."""
    return re.match('^[\d]{2}/[\d]{2}/[\d]{4}$', dob) is not None

def is_password(password):
    """Checks whether password provided is of valid format."""
    return re.match('^[a-zA-Z]+(@|&)[0-9]+$', password) is not None

def print_error(error, to_retry = False):
    """Prints out error messages with additional formatting.
    Has an option to display an additional message for input retries."""
    print(f"* {error}\n")

    if to_retry:
        print("Please start again:")

def print_title(title):
    """Prints out screen titles with additional formatting."""
    print(f"\n===== {title} =====\n")

def store_user(full_name,address, mobile_number, dob, password):
    """Function to store user details as a tuple in a global list in memory.
    Password is stored as a list to accommodate password history,
    wherein the last item is the most recent one."""
    user = (full_name,address, mobile_number, dob, [password])

    users.append(user)

def is_user_exists(username):
    """Checks if user records exists by looking up its username (mobile number)."""
    for user in users:
        if username == user[2]:
            return user

    return None

def is_user_password_exists(user, password):
    """Checks if provided password is already in user's password history."""
    return password in user[-1]

if __name__ == '__main__':
    main_selection()
