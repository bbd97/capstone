from extras import ask_for_int, ask_for_search

tables = ('lender', 'borrower', 'vehicle', 'trip')
borrower_table = 'borrower'
lender_table = 'lender'
vehicle_table = 'vehicle'
trip_table = 'trip'

borrower_values = ('BorrowerID', 'BorrowerFirst', 'BorrowerLast', 'BorrowerEmail', 'BorrowerPassword', 'BorrowerPhone', 'BorrowerDOB', 'BorrowerSex', 'BorrowerAddress', 'BorrowerCity', 'BorrowerState', 'BorrowerZip', 'BorrowerIsVerified', 'BorrowerCredit', 'BorrowerExpiration', 'BorrowerCVV', 'BorrowerPaypal', 'BorrowerLicense', 'BorrowerInsurance', 'BorrowerRating', 'BorrowerNumOfTrips')
lender_values = ('LenderID', 'LenderFirst', 'LenderLast', 'LenderEmail', 'LenderPassword', 'LenderPhone', 'LenderDOB', 'LenderSex', 'LenderAddress', 'LenderCity', 'LenderState', 'LenderZip', 'LenderIsVerified', 'LenderAccount', 'LenderRouting', 'LenderPaypal', 'LenderLicense', 'LenderInsurance', 'LenderRating', 'LenderTimesLended')
vehicle_values = ('VehicleVIN', 'VehicleMake', 'VehicleModel', 'VehicleYear', 'VehicleColor', 'VehiclePlateNum', 'VehicleCapacity', 'VehicleMileage', 'VehicleMPG', 'VehicleType', 'VehicleTransmission', 'VehicleIsSmoking', 'VehicleCondition', 'VehicleTimesBorrowed', 'VehicleRentalPrice', 'VehicleIsListed', 'VehicleIsApproved', 'LenderID')
trip_values = ('TripID', 'BorrowerID', 'LenderID', 'VehicleVIN', 'TripDate', 'TripIsCompleted', 'BorrowerRating', 'LenderRating')

# Option 1
# -------------------------------------------------------------------------------------------------

def admin_verify_user(cursor):
    table_selection = ''
    table_count = 1
    table_list = []
    table_list_order = []
    user_selection = ''
    user_count = 1
    user_list = []
    user_list_order = []
    print()
    for x in range (1, 3):
        if (x == 1):
            table = borrower_table
        else:
            table = lender_table

        cursor.execute('SELECT {}ID FROM {} WHERE {}IsVerified = 0'.format(table.title(), table.upper(), table.title()))
        result = cursor.fetchall()
        
        if (len(result) != 0):
            print(table_count, '-', 'Verify a', table)
            table_list.append(table)
            table_list_order.append(table_count)
            if (table_count != 2):
                table_count += 1

    if (len(result) != 0):
        admin_choice = ask_for_int('\nEnter a menu option', 1, table_count)
        print()
        for x in range(0, 2):
            if (admin_choice == table_list_order[x]):
                table_selection = table_list[x]
            
        cursor.execute('SELECT {}ID FROM {} WHERE {}IsVerified = 0'.format(table_selection.title(), table_selection.upper(), table_selection.title()))
        result = cursor.fetchall()

        if (len(result) != 0):
            for x in range(0, len(result)):
                print('(' + str(user_count) + ')', result[x][0])
                user_list.append(result[x][0])
                user_list_order.append(user_count)
                if (user_count != len(result)):
                    user_count += 1

            admin_choice = ask_for_int('\nWhich ' + table_selection + ' would you like to verify? (enter 0 to go back)', 1, len(result))
            
            if (admin_choice != 0):
                for x in range(0, len(result)):
                    if (admin_choice == user_list_order[x]):
                        user_selection = user_list[x]

                cursor.execute('UPDATE {} SET {}IsVerified = 1 WHERE {}ID = \'{}\''.format(table_selection.upper(), table_selection.title(), table_selection.title(), user_selection.upper()))

                if (table_selection == 'borrower'):
                    user_action = 'renting'
                elif (table_selection == 'lender'):
                    user_action = 'listing'
                    
                # If the program goofs up for some reason, stop it.
                else:
                    print('Something bad happened. Abort mission!')
                    exit(1)

                print(user_selection.upper(), 'has now been verified and can start', user_action, 'vehicles.')

            else:
                print('Returning to the admin menu.')
        else:
            print('All', table_selection + 's in the system are verified. Returning to the admin menu.')
    else:
        print('All users in the system are verified. Returning to the admin menu.')

# Option 2
# -------------------------------------------------------------------------------------------------

def admin_approve_vehicle(cursor):
    lender = ''
    vehicle = ''
    lender_selection = ''
    vehicle_selection = ''
    vehicle_count = 1
    # LenderID, VehicleVIN
    vehicle_list = []
    vehicle_list_order = []
    print() 

    cursor.execute('SELECT LenderID, VehicleVIN FROM VEHICLE WHERE VehicleIsApproved = 0 ORDER BY LenderID ASC')
    result = cursor.fetchall()
    
    if (len(result) != 0):
        for x in range(0, len(result)):
            for y in range (0, len(result[x])):
                if (y == 0):
                    lender = result[x][y]
                else:
                    vehicle = result[x][y]
            vehicle_list.append([lender, vehicle])
            vehicle_list_order.append(vehicle_count)
            print('(' + str(vehicle_count) + ')', vehicle_list[x][0], '—', vehicle_list[x][1])
            if (vehicle_count != len(result)):
                vehicle_count += 1

        admin_choice = ask_for_int('\nEnter a menu option', 1, vehicle_count)
        print()
        if (admin_choice != 0):
            for x in range(0, len(result)):
                if (admin_choice == vehicle_list_order[x]):
                    for y in range(0, 2):
                        if (y == 0):
                            lender_selection = vehicle_list[x][y]
                        else:
                            vehicle_selection = vehicle_list[x][y]
            cursor.execute('UPDATE VEHICLE SET VehicleIsApproved = 1 WHERE LenderID = \'{}\' AND VehicleVIN = \'{}\';'.format(lender_selection.upper(), vehicle_selection.upper()))
            print('Vehicle', vehicle_selection.upper(), 'has now been verified for lender', lender_selection.upper() + '.')
        else:
            print('Returning to the admin menu.')
    else:
        print('All vehicles in the system are approved. Returning to the admin menu.')

# Option 3
# -------------------------------------------------------------------------------------------------

def admin_search_database(cursor):
    table_name = ask_for_search('Please enter a table to view', tables, 0)
    table_values = ()
    if (table_name == borrower_table):
        table_values = borrower_values
    elif (table_name == lender_table):
        table_values = lender_values
    elif (table_name == vehicle_table):
        table_values = vehicle_values
    elif (table_name == trip_table):
        table_values = trip_values

    # If the program goofs up for some reason, stop it.
    else:
        print('Something bad happened. Abort mission!')
        exit(1)

    value_name = ask_for_search('Please enter a variable to view (leave blank to search all)', table_values, 1)
    cursor.execute('SELECT {} FROM {}'.format(value_name, table_name.upper()))
    result = cursor.fetchall()
    for x in result:
        print(x)
