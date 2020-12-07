from login import user_login, admin_login
from borrower import borrower_rent_vehicle, borrower_rate_trip, borrower_view_history
from lender import lender_list_unlist, lender_add_vehicle, lender_remove_vehicle, lender_check_vehicle_info, lender_check_trip_status, lender_view_history
from admin import admin_verify_user, admin_search_database, admin_approve_vehicle
from extras import ask_for_int

# Define static menu options
main_options = ('Menu', 'I am a borrower', 'I am a lender', 'Administrator login', 'Quit')
borrower_options = ('Borrower', 'Rent a vehicle', 'Rate a trip', 'View borrowing history', 'Log out')
lender_options = ('Lender', 'List a vehicle', 'Drop a vehicle listing', 'Add a new vehicle', 'Remove a vehicle', 'Check vehicle info', 'Check trip status', 'View lending history', 'Log out')
admin_options = ('Administrator', 'Verify a user', 'Approve a vehicle', 'Search the database', 'Log out')

# -------------------------------------------------------------------------------------------------

def display_menu(option_tuple):
    print('\n' + '*' * 3, option_tuple[0], 'Options:', '*' * 3)
    for x in range(1, len(option_tuple)):
        print(x, '-', option_tuple[x])

# -------------------------------------------------------------------------------------------------

def ask_to_repeat_menu():
    # Allow the user to display the menu, hide the menu, or quit the program
    while True:
        see_menu = input('Would you like to see the menu options again? (Y/N/Q): ').upper()
        if see_menu == 'Y' or see_menu == 'N' or see_menu == 'Q':
            break
        else:
            print('Invalid input! Try again.')

    if see_menu == 'N':
        return False
    elif see_menu == 'Y':
        return True
    elif see_menu == 'Q':
        return 'quit'

    # If the program goofs up for some reason, stop it.
    else:
        print('Something bad happened. Abort mission!')
        exit(1)

# -------------------------------------------------------------------------------------------------

def main_menu(cursor):
    repeat_menu = True
    while True:
        # Give the user the option during the second iteration and beyond to show the menu or not
        if repeat_menu:
            display_menu(main_options)

        print()
        choice = ask_for_int('Enter a menu option', 1, len(main_options) - 1)

        if choice == 1:
            borrower_id = user_login(1, cursor)
            if (borrower_id != -1):
                borrower_menu(borrower_id, cursor)
            break
        elif choice == 2:
            lender_id = user_login(2, cursor)
            if (lender_id != -1):
                lender_menu(lender_id, cursor)
            break
        elif choice == 3:
            admin_verif = admin_login()
            if (admin_verif):
                admin_menu(cursor)
            break
        elif choice == 4:
            break

        # If the program goofs up for some reason, stop it.
        else:
            print('Something bad happened. Abort mission!')
            exit(1)

# -------------------------------------------------------------------------------------------------

def borrower_menu(borrower_id, cursor):
    repeat_menu = True
    while True:
        # Give the user the option during the second iteration and beyond to show the menu or not
        if repeat_menu:
            display_menu(borrower_options)

        print()
        choice = ask_for_int('Enter a menu option', 1, len(borrower_options) - 1)

        if choice == 1:
            borrower_rent_vehicle(borrower_id, cursor)
        elif choice == 2:
            borrower_rate_trip(borrower_id, cursor)
        elif choice == 3:
            borrower_view_history(borrower_id, cursor)
        elif choice == 4:
            break

        # If the program goofs up for some reason, stop it.
        else:
            print('Something bad happened. Abort mission!')
            exit(1)

        repeat_menu = ask_to_repeat_menu()
        if (repeat_menu == 'quit'):
            break

# -------------------------------------------------------------------------------------------------

def lender_menu(lender_id, cursor):
    repeat_menu = True
    while True:
        # Give the user the option during the second iteration and beyond to show the menu or not
        if repeat_menu:
            display_menu(lender_options)

        print()
        choice = ask_for_int('Enter a menu option', 1, len(lender_options) - 1)

        if choice == 1:
            lender_list_unlist(1, lender_id, cursor)
        elif choice == 2:
            lender_list_unlist(2, lender_id, cursor)
        elif choice == 3:
            lender_add_vehicle(lender_id, cursor)
        elif choice == 4:
            lender_remove_vehicle(lender_id, cursor)
        elif choice == 5:
            lender_check_vehicle_info(lender_id, cursor)
        elif choice == 6:
            lender_check_trip_status(lender_id, cursor)
        elif choice == 7:
            lender_view_history(lender_id, cursor)
        elif choice == 8:
            break

        # If the program goofs up for some reason, stop it.
        else:
            print('Something bad happened. Abort mission!')
            exit(1)

        repeat_menu = ask_to_repeat_menu()
        if (repeat_menu == 'quit'):
            break

# -------------------------------------------------------------------------------------------------

def admin_menu(cursor):
    repeat_menu = True
    while True:
        # Give the user the option during the second iteration and beyond to show the menu or not
        if repeat_menu:
            display_menu(admin_options)

        print()
        choice = ask_for_int('Enter a menu option', 1, len(admin_options) - 1)

        if choice == 1:
            admin_verify_user(cursor)
        elif choice == 2:
            admin_approve_vehicle(cursor)
        elif choice == 3:
            admin_search_database(cursor)
        elif choice == 4:
            break

        # If the program goofs up for some reason, stop it.
        else:
            print('Something bad happened. Abort mission!')
            exit(1)

        repeat_menu = ask_to_repeat_menu()
        if (repeat_menu == 'quit'):
            break
