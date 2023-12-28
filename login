from register_page import register
from admin_page import admin_page
from user_page import user_page
from convert_dic import turn_dic


# Request user to go register page
def go_register():
    perform = input("Do you want to register? (yes/no): ")
    perform = perform.lower()
    while True:
        if perform == "yes":
            print("")
            register()
            login()
        elif perform == "no":
            print("")
            login()
        else:
            print("Wrong input! Please type again!")
            perform = input("Do you want to exit? (yes/no): ")


def login():
    print("----Login Page----")
    print("")

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

    # To know which text file we should refer
    role = input("Enter as (admin/user): ")
    while True:
        if role == "admin":
            file_name = "admin_info.txt"
            break

        elif role == "user":
            file_name = "user_info.txt"
            break

        else:
            print("Invalid candidate!!")
            print("")
            role = input("Enter as (admin/user): ")

    username = input("Enter username: ")
    password = input("Enter password: ")

    # To direction the user to their page
    my_dic = turn_dic(file_name)
    found = False
    for info in my_dic:
        if info["Username"] == username and info["Password"] == password:
            authorise = info["Admin"]
            print("---Login success---")
            print("")
            found = True
            if "no" in authorise:
                user_page(username)
            elif "yes" in authorise:
                admin_page()
            break

    # When they cannot log in, request them to go register page
    if not found:
        print("Username or password incorrect")
        print("")
        go_register()
