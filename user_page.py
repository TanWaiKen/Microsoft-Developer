from register_page import check_birth
from convert_dic import turn_dic


# Check the booking date and time is been booked or not
def check_crush(new_start, new_end, hall_id):
    from datetime import datetime

    booking_info = turn_dic("booking_info.txt")
    for info in booking_info:
        if info["Hall ID"] == hall_id:
            old_start = info["Start"]
            old_end = info["End"]

            new_end = datetime.strptime(new_end, '%d-%m-%Y %H%M')
            old_start = datetime.strptime(old_start, '%d-%m-%Y %H%M')
            old_end = datetime.strptime(old_end, '%d-%m-%Y %H%M')

            if old_start <= new_start <= old_end:
                return False
            elif old_start <= new_end <= old_end:
                return False
            elif new_start < old_start and new_end > old_end:
                return False

        else:
            pass

    return True


# Use to search the correct rent_rate for booking
def rent_rate(hall_id):
    hall_info = turn_dic("hall_info.txt")
    for info in hall_info:
        if info["Hall ID"] == hall_id:
            return int(info["Hall Price per hour"])
    return None


# Page for user perform add booking
def add_book(username):
    from datetime import datetime, timedelta

    # Ask about the event and booking info
    event_name = input("Enter your event name: ")
    event_des = input("Enter the description of the event: ")

    # Check the number of pax is a positive number
    while True:
        num_pax = input("Enter number of pax: ")
        if num_pax.isdigit():
            num_pax = int(num_pax)
            if num_pax < 1:
                print("Please enter a positive number." "\n")
            elif num_pax > 1000:
                print("No hall is suitable for this number of pax.")
            else:
                break
        else:
            print("Please enter only number." "\n")

    # Show all the hall information
    hall_info = turn_dic("hall_info.txt")
    id_list = []
    for info in hall_info:
        if int(info["Hall pax"]) > num_pax:    # Display only the hall type that can afford the number of pax
            print(f"Hall ID: {info['Hall ID']}\n"
                  f"Hall Type: {info['Hall name']}\n"
                  f"Rate per hour: {info['Hall Price per hour']}RM/h\n"
                  f"Number of pax: {info['Hall pax']}pax\n"
                  f"Unavailable date: {info['Unavailable date']}\n"
                  f"Hall description: {info['Hall Description']}\n")
            id_list.append(info['Hall ID'])     # Collect the hall id that user can book

    booking_info = turn_dic("booking_info.txt")
    # Check whether the booking is expired or not
    for index, info in enumerate(booking_info):
        booking_date = datetime.strptime(info["End"], "%d-%m-%Y %H%M")
        if datetime.now() > booking_date:
            booking_info.pop(index)
            # Give the new unique ID
            for data in booking_info:
                booking_id = str(booking_info.index(data))
                data["Booking ID"] = booking_id

    # Create a unique booking id
    booking_id = str(len(booking_info))

    # Ask which hall they want to book using hall id
    while True:
        hall_id = input("Enter Hall ID: ")
        found = False
        for ids in id_list:
            if hall_id not in ids:
                continue
            else:
                found = True

        if not found:
            print("Couldn't found the ID!")
            print("")
        else:
            break

    # To inform the user about the booked slots for the selected hall
    print("")
    print("Booking session that has been booked:")
    for info in booking_info:
        if info["Hall ID"] == hall_id:
            old_start = info["Start"]
            old_end = info["End"]
            print(f'{old_start} to {old_end}')
    print("")

    while True:
        found = True
        valid_date = ""

        # Read booking start time
        while True:
            start = input("Enter your booking date (DD-MM-YYYY HHMM): ")
            try:
                valid_date = datetime.strptime(start, "%d-%m-%Y %H%M")
                opened = datetime.strptime("0800", "%H%M").time()
                closed = datetime.strptime("1800", "%H%M").time()
                unavailable_date = []

                for info in hall_info:
                    if info["Hall ID"] == hall_id:
                        unavailable_date.extend(info["Unavailable date"])
                        break

                if opened <= valid_date.time() <= closed:   # Check whether the time is within operating hour
                    if valid_date > datetime.now():     # Check it is future date or not
                        if len(unavailable_date) < 1:
                            found = False
                            break
                        else:
                            for date in unavailable_date:
                                date = datetime.strptime(date, "%d-%m-%Y").date()
                                if valid_date.date() != date:   # Check whether the date is in the unavailable date list
                                    found = False
                                    break
                                else:
                                    print("We are closed that day.")
                    else:
                        print("Please enter future date.")
                else:
                    print("Invalid time. Please enter a time between 0800 and 1800 in 24-hour format.")

            except ValueError:
                print("Invalid date format. Please enter date as 'DD-MM-YYYY HHMM'.")

            if not found:
                break

        # Read booking slots duration
        while True:
            duration = input("Enter your booking duration in increments of 1 hour (e.g., '1', '2', '3', etc.): ")
            end = valid_date + timedelta(hours=int(duration))
            formatted_end = end.strftime("%d-%m-%Y %H%M")

            valid_time = end.time()
            closed = datetime.strptime("1800", "%H%M").time()

            if duration.isdigit() and int(duration) > 0:
                if valid_time > closed:
                    print("Our operating hour end at 1800.")
                else:
                    break
            else:
                print("Invalid duration. Please enter a positive whole number.")

        # Check is the booking session has been booked or not
        if not check_crush(valid_date, formatted_end, hall_id):
            print("This booking session has been booked already." "\n")

        else:
            break

    # Display the booking details
    total_price = int(duration) * rent_rate(hall_id)
    print("")
    print(f"You have successfully booked the hall for {duration} hours at {start}.")
    print(f"Your booking session will end at {formatted_end}")
    print(f"Fees that you need to pay is RM{total_price}.")
    print("")

    # Write the information gathered into txt file
    my_dic = {
        "Username": username,
        "Hall ID": hall_id,
        "Duration": duration,
        "Total Price": total_price,
        "Start": start,
        "End": formatted_end,
        "Event Name": event_name,
        "Number of pax": num_pax,
        "Event Description": event_des,
        "Booking ID": booking_id
    }

    print("This is your booking details 😘😘")
    for key, info in my_dic.items():
        print(f"{key}: {info}")
    print("")

    booking_info.append(my_dic)

    with open("booking_info.txt", "w") as w:
        w.write(str(booking_info))
        w.close()


def search_book(username, area):
    booking_info = turn_dic("booking_info.txt")

    # Check if the file is empty or not, if yes user are not allow to continue
    if not booking_info:
        print("No booking yet!")
        user_page(username)

    found = False

    for info in booking_info:
        found = True
        info_text = (f"Hall ID: {info['Hall ID']}\n"
                     f"Duration: {info['Duration']} hours\n"
                     f"Total Price: RM{info['Total Price']}\n"
                     f"Start: {info['Start']}\n"
                     f"End: {info['End']}\n"
                     f"Event Name: {info['Event Name']}\n"
                     f"Event description: {info['Event Description']}\n"
                     f"Number of pax: {info['Number of pax']} person\n"
                     f"Booking ID: {info['Booking ID']}\n")

        # User can press enter key to get all the booking information
        if len(area) < 1 and info["Username"] == username:
            print(info_text)

        # User can only found the filtered booking information
        elif info["Username"] == username and area.lower() in str(info).lower():
            print(info_text)
            break

        # Area that user searched show nothing
        else:
            print("There is no information related based on your searching area.")
            print("Your search result is nothing......." "\n")

    if not found:
        print("You haven't booked anything yet!")


def delete_book(username):
    print("Search the information that you want to delete!")
    print("Remember there is no refund for the canceled booking!!")
    print("")
    area = input("Search bar (Enter to show all booking): ")    # Use search to let user check the booking information
    search_book(username, area)
    booking_info = turn_dic("booking_info.txt")

    while True:
        # User must write down the booking ID
        while True:
            booking_id = input("Please write down the booking ID of the order that you want to delete: ")
            if len(booking_id) < 1:
                continue
            else:
                break

        for index, info in enumerate(booking_info):
            # Check the user account have the booking id or not
            if info["Booking ID"] == booking_id and info["Username"] == username:
                while True:
                    # Confirm again with the user
                    check = input("Do you want to delete this booking information? (yes/no/back): ")
                    check = check.lower()
                    if check == "yes":
                        print("The booking information is deleted!\n")
                        print("Sorry! No refund will be given!\n")

                        # Delete the dictionary in a dictionary list
                        booking_info.pop(index)
                        with open("booking_info.txt", 'w') as w:
                            w.write(str(booking_info))
                        return
                    elif check == "no":
                        pass
                    elif check == "back":
                        return
                    else:
                        print("Please choose only the listed selection!!!")

            else:
                print("The booking ID is not yours!")
                break


def edit_profile(username):
    print("")
    print("----Profile page----")
    print("")
    user_info = turn_dic("user_info.txt")

    # Show the profile information
    for data in user_info:
        if data['Username'] == username:
            info = (f"First Name: {data['First Name']}\n"
                    f"Last Name: {data['Last Name']}\n"
                    f"Birthday: {data['Birthday']}\n"
                    f"Phone Number: {data['Phone Number']}\n")
            print(info)
            print("")
            print("1 Edit first name\n"
                  "2 Edit last name\n"
                  "3 Edit password\n"
                  "4 Edit birthday\n"
                  "5 Edit phone number\n"
                  "6 Exit")

            # Perform something based on user input
            while True:
                # Change their first name
                user_perform = input("Enter the command number: ")
                if user_perform == "1":
                    data["First Name"] = input("Enter your first name: ")
                    break

                # Change their last name
                elif user_perform == "2":
                    data["Last Name"] = input("Enter your last name: ")
                    break

                # Change their password
                elif user_perform == "3":
                    while True:
                        password = input("Enter your current password: ")
                        if data["Password"] == password:
                            while True:
                                new_password = input("Enter new password: ")
                                new_password2 = input("Retype the new password: ")
                                if len(new_password) < 1:  # User couldn't skip this section
                                    print("Please write your password and don't make it blank.")
                                elif new_password != new_password2:  # Make sure user types same password twice
                                    print("Passwords do not match.")
                                elif new_password == password:  # Avoid same password with old password
                                    print("This is your old password. Please type a new one!!!")
                                else:
                                    data["Password"] = new_password2
                                    break
                            break
                        else:
                            print("Incorrect password. Please try again.")
                    break

                # Check user birthday date format and it cannot be a future date
                elif user_perform == "4":
                    birth_day = input("Birthday (dd/mm/yyyy): ")
                    while not check_birth(birth_day):
                        print("Please follow the format with / and type the number.")
                        print("And do not write the future date.")
                        print("")
                        birth_day = input("Birthday (dd/mm/yyyy): ")
                    data["Birthday"] = birth_day
                    break

                elif user_perform == "5":
                    data["Phone Number"] = input("Enter your new phone number: ")
                    break

                elif user_perform == "6":
                    return

                else:
                    print("Wrong command number!! Please type again! ")

    with open(r"user_info.txt", 'w') as f:
        f.write(str(user_info))
        f.close()
        return


# Main page
def user_page(username):
    while True:
        print("-----Home page-----")
        print("Operating hour: 8am-6pm" "\n")
        print("1 Add Booking" "\n"
              "2 Search Booking" "\n"
              "3 Delete Booking" "\n"
              "4 Update profile information" "\n"
              "5 Exit" "\n"
              "6 Log Out" "\n")

        # Ask for user input to know what to perform
        user_perform = input("Enter the command number: ")
        if user_perform == "1":
            add_book(username)

        elif user_perform == "2":
            area = input("Search bar (Enter to show all booking): ")
            while True:
                search_book(username, area)
                user_perform = input("Do you want to continue? (yes/no): ")
                if user_perform == "yes":
                    area = input("Search bar: ")
                    search_book(username, area)
                    break

                elif user_perform == "no":
                    break

                else:
                    print("You can only type yes or no!!!")

        elif user_perform == "3":
            delete_book(username)

        elif user_perform == "4":
            edit_profile(username)

        elif user_perform == "5":
            print("Existing application......")
            exit()

        elif user_perform == "6":
            print("")
            return

        else:
            print("Wrong command number")
            user_page(username)
