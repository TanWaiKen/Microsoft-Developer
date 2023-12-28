import re
from datetime import datetime
from convert_dic import turn_dic


# Check the format of the email to identify user
def check_user_email(email):
    if not re.match(r"^[a-z0-9]+@+[a-z]+[.][a-z]{2,3}$", email):
        return False
    return True


# Check the format of the email to identify admin
def check_admin_email(email):
    if not re.match(r"^[a-z0-9]+@+mail.apu.edu.my", email):  # \w any word character
        return False
    return True


# Check the format of the user input in birthday section
def check_birth(birth_day):
    try:
        valid_date = datetime.strptime(birth_day, "%d/%m/%Y")  # Validate date format
        if valid_date < datetime.now():
            return True
    except ValueError:
        return False


def register():

    # Giving user instruction
    print("----Register Page----")
    print("Only APU email will be given authorization to act as admin.")
    print("For security reason, please don't put the same characters for your username and password.")
    print("")
    f_user = open("user_info.txt", 'r').read()
    f_admin = open("admin_info.txt", 'r').read()

    # Allow user to back to previous page
    while True:
        print("(Press enter key) to continue" "\n"
              "(Type 'back') to back to previous page" "")
        user_perform = input("Continue or Back: ")
        if user_perform.lower() == "back":
            print("")
            return
        elif len(user_perform) < 1:
            break
        else:
            print("Please perform only the action that has listed.")
            print("")

    print("")

    # Ask username
    while True:
        username = input("Username: ")
        if len(username) > 1:
            while username in f_user or username in f_admin:
                print("Username exist.")
                username = input("Username: ")
            break
        else:
            pass

    # Ask password
    while True:
        password = input("Password: ")
        password2 = input("Retype the password: ")
        if len(password) < 1:   # User couldn't blank this section
            print("Please write your password and don't make it blank.")
        elif password != password2:     # Make sure user type same password twice
            print("Passwords do not match.")
        elif username == password:  # User are not allow to have same characters for username and password
            print("Please avoid using your password same as username!!!")
        else:
            break

    # Ask first name
    while True:
        first_name = input("First Name: ")
        no_space = first_name.replace(" ", "")
        if not no_space.isalpha():
            print("Please enter only alphabets.")
        else:
            first_name = no_space.title()
            break

    # Ask last name
    while True:
        last_name = input("Last Name: ")
        no_space = last_name.replace(" ", "")
        if not no_space.isalpha():
            print("Please enter only alphabets.")
        else:
            last_name = last_name.title()
            break

    # Ask user birthday
    birth_day = input("Birthday (dd/mm/yyyy): ")
    while not check_birth(birth_day):
        print("Please follow the format with / and type the number.")
        print("And do not write the future date.")
        print("")
        birth_day = input("Birthday (dd/mm/yyyy): ")

    # Ask user contact number
    contact_num = input("Phone Number: ")

    # Ask user email address and check its format to know whether is admin or user
    email = input("Email: ")
    while not check_user_email(email) and not check_admin_email(email):
        print("Invalid email.")
        email = input("Email: ")

    if check_admin_email(email):
        admin = "yes"
        file_name = 'admin_info.txt'

    else:
        admin = "no"
        file_name = 'user_info.txt'

    data = {
        "Username": username,
        "Password": password,
        "First Name": first_name,
        "Last Name": last_name,
        "Birthday": birth_day,
        "Phone Number": contact_num,
        "Email": email,
        "Admin": admin
    }

    my_dic = turn_dic("user_info.txt")
    my_dic.append(data)

    with open(file_name, 'w') as f:
        f.write(str(my_dic))

    print("----Register successful----" "\n")
