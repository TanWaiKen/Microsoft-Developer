from register_page import register
from login import login


# Where the code start
def main_page():

    while True:
        print("💕💕WELCOME TO HALL SYMPHONY INC 💕💕")
        # Tell the user what they can do
        print('1 Register')
        print('2 Login')
        print('3 Exit'"\n")

        user_input = input("Enter your command number🤔: ")
        # Check what to perform

        if user_input == '1':
            print("")
            register()
            print("")
            login()

        elif user_input == '2':
            print("")
            login()

        elif user_input == '3':
            print("Exiting the application...👋👋")
            exit()

        else:
            print("")
            print("Invalid input")
            print("Please only choose from the listed number!")


if __name__ == "__main__":
    main_page()
