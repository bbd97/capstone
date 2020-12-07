from extras import ask_for_int, ask_for_float, ask_for_input
vehicle_values = ('VIN', 'Make', 'Model', 'Year', 'Color', 'License Plate Number', 'Capacity', 'Mileage', 'Miles Per Gallon', 'Type', 'Transmission', 'Smoking', 'Condition', 'Times Borrowed', 'Rental Price', 'Listed', 'Approved', 'Lender ID')
vehicle_tuple = (('VIN', 'char', 17), ('Make', 'char', 20), ('Model', 'char', 20),
                  ('Year', 'int', 4), ('Color', 'char', 20), ('License Plate Number', 'char', 10),
                  ('Capacity', 'int', 2), ('Mileage', 'int', 10), ('Miles Per Gallon', 'int', 3),
                  ('Type (Gas, Electric, Hybrid)', 'char', 20), ('Transmission (Automatic, Manual)', 'char', 20), ('Smoking (Yes, No)', 'char', 3),
                  ('Condition (New, Excellent, Very Good, Good, Fair, Poor)', 'char', 20), ('Times Borrowed', 'int', 5), ('Rental Price', 'int', 5),
                  ('Listed', 'int', 1), ('Approved', 'int', 1), ('Lender ID', 'char', 10))
trip_values = ('Trip ID', 'Borrower Username', 'User ID', 'Vehicle', 'Date Of Trip', 'Completed', 'Borrower\'s Rating For You', 'Your Rating For Borrower')

# Options 1 & 2
# -------------------------------------------------------------------------------------------------

def lender_list_unlist(listing_type, lender_id, cursor):
    if (listing_type == 1):
        first_query_num = 0
        second_query_num = 1
        prefix = ''
        opposite_prefix = 'un'
    elif (listing_type == 2):
        first_query_num = 1
        second_query_num = 0
        prefix = 'un'
        opposite_prefix = ''
        
    # If the program goofs up for some reason, stop it.
    else:
        print('Something bad happened. Abort mission!')
        exit(1)

    cursor.execute('SELECT LenderIsVerified FROM LENDER WHERE LenderID = \'{}\''.format(lender_id))
    lender_is_verified = cursor.fetchall()[0][0]
    if (lender_is_verified == 1):
        cursor.execute('SELECT VehicleVIN FROM VEHICLE WHERE LenderID = \'{}\' AND VehicleIsListed = {}'.format(lender_id, first_query_num))
        vehicle_list = cursor.fetchall()
        max = len(vehicle_list)

        if (max > 0):
            print('\nHere are your', opposite_prefix + 'listed vehicles:')
            for x in range(0, max):
                print('(' + str(x + 1) + ')', vehicle_list[x][0])

            lender_option = ask_for_int('\nWhich vehicle would you like to ' + prefix + 'list? (enter 0 to go back)', 1, max)
            if (lender_option > 0):
                cursor.execute('SELECT VehicleIsApproved FROM VEHICLE WHERE LenderID = \'{}\' AND VehicleVIN = \'{}\''.format(lender_id, vehicle_list[lender_option - 1][0]))
                vehicle_is_approved = cursor.fetchall()[0][0]
                if (vehicle_is_approved == 1):
                    cursor.execute('SELECT TripIsCompleted FROM TRIP WHERE LenderID = \'{}\' AND VehicleVIN = \'{}\''.format(lender_id, vehicle_list[lender_option - 1][0]))
                    vehicle_status = cursor.fetchall()
                    vehicle_is_being_rented = 0
                    for x in range(0, len(vehicle_status)):
                        for y in range(0, len(vehicle_status[x])):
                            if (vehicle_status[x][y] == 1):
                                vehicle_is_being_rented += 1
                    if (vehicle_is_being_rented == 0):
                        cursor.execute('UPDATE VEHICLE SET VehicleIsListed = {} WHERE LenderID = \'{}\' AND VehicleVIN = \'{}\''.format(second_query_num, lender_id, vehicle_list[lender_option - 1][0]))
                        print('Vehicle #' + str(lender_option), 'has been', prefix + 'listed.')
                    else:
                        print('Vehicle is currently under rent.')
                else:
                    print('Vehicle has not yet been approved. Please wait for administrative approval.')
            else:
                print('Returning to the menu screen.')
        else:
            print('You currently have no', prefix + 'listed vehicles.')
    else:
        print('User is not yet verified. Please verify your account before listing a vehicle.')

# Option 3
# -------------------------------------------------------------------------------------------------

def lender_add_vehicle(lender_id, cursor):
    cursor.execute('SELECT LenderIsVerified FROM LENDER WHERE LenderID = \'{}\''.format(lender_id))
    lender_is_verified = cursor.fetchall()[0][0]
    if (lender_is_verified == 1):
        vehicle_vin = ask_for_input('Please enter the VIN of the vehicle (enter 0 to go back)', 'char', 17, 17).upper()
        if (vehicle_vin != '0'):
            cursor.execute('SELECT EXISTS(SELECT * FROM VEHICLE WHERE VehicleVIN = \'{}\')'.format(vehicle_vin))
            vehicle_exists = cursor.fetchall()[0][0]
            if (vehicle_exists == 0):
                sql_add_vehicle = 'INSERT INTO VEHICLE VALUES'
                sql_add_vehicle += ('\n(\'' + vehicle_vin + '\', ')
                for x in range(1, len(vehicle_tuple)):
                    if (vehicle_tuple[x][1] == 'char'):
                        sql_add_vehicle += ('\'')

                    if (vehicle_tuple[x][0] == 'Listed' or vehicle_tuple[x][0] == 'Approved' or vehicle_tuple[x][0] == 'Times Borrowed'):
                        sql_add_vehicle += str(0)
                    elif (vehicle_tuple[x][0] == 'Lender ID'):
                        sql_add_vehicle += lender_id
                    else:
                        sql_add_vehicle += ask_for_input(vehicle_tuple[x][0], vehicle_tuple[x][1], 1, vehicle_tuple[x][2])

                    if (vehicle_tuple[x][1] == 'char'):
                        sql_add_vehicle += ('\'')

                    if (x != len(vehicle_tuple) - 1):
                        sql_add_vehicle += ', '

                sql_add_vehicle += (')')
                
                cursor.execute(sql_add_vehicle)
                print('Vehicle has been registered to the database.')
            else:
                print('This vehicle has already been registered to the database.')
        else:
            print('Returning to the main menu.')
    else:
        print('User is not yet verified. Please verify your account before adding a vehicle.')

# Option 4
# -------------------------------------------------------------------------------------------------

def lender_remove_vehicle(lender_id, cursor):
    cursor.execute('SELECT LenderIsVerified FROM LENDER WHERE LenderID = \'{}\''.format(lender_id))
    lender_is_verified = cursor.fetchall()[0][0]
    if (lender_is_verified == 1):
        cursor.execute('SELECT VehicleVIN FROM VEHICLE WHERE LenderID = \'{}\''.format(lender_id))
        vehicle_list = cursor.fetchall()
        max = len(vehicle_list)

        if (max > 0):
            print('\nHere are your vehicles:')
            for x in range(0, max):
                print('(' + str(x + 1) + ')', vehicle_list[x][0])

            lender_option = ask_for_int('\nWhich vehicle would you like to remove? (enter 0 to go back)', 1, max)
            if (lender_option > 0):
                cursor.execute('DELETE FROM VEHICLE WHERE LenderID = \'{}\' AND VehicleVIN = \'{}\''.format(lender_id, vehicle_list[lender_option - 1][0]))
                print('Vehicle #' + str(lender_option), 'has been removed.')
            else:
                print('Returning to the menu screen.')
        else:
            print('You currently have no added vehicles.')
    else:
        print('User is not yet verified. Please verify your account before adding a vehicle.')

# Option 5
# -------------------------------------------------------------------------------------------------

def lender_check_vehicle_info(lender_id, cursor):
    cursor.execute('SELECT VehicleVIN FROM VEHICLE WHERE LenderID = \'{}\''.format(lender_id))
    vehicle_list = cursor.fetchall()
    max = len(vehicle_list)

    if (max > 0):
        print('\nHere are your vehicles:')
        for x in range(0, max):
            print('(' + str(x + 1) + ')', vehicle_list[x][0])

        lender_option = ask_for_int('\nWhich vehicle would you like to check the information of? (enter 0 to go back)', 1, max)
        if (lender_option > 0):
            cursor.execute('SELECT * FROM VEHICLE WHERE LenderID = \'{}\' AND VehicleVIN = \'{}\''.format(lender_id, vehicle_list[lender_option - 1][0]))
            vehicle_info = cursor.fetchall()
            for x in vehicle_info:
                for y in range(0, len(x)):
                    if (x[y] == 1):
                        output = 'Yes'
                    elif (x[y] == 0):
                        output = 'No'
                    else:
                        output = x[y]

                    print(vehicle_values[y] + ':', output)
        else:
            print('Returning to the menu screen.')
    else:
        print('You currently have no vehicles in the database.')

# Option 6
# -------------------------------------------------------------------------------------------------

def lender_check_trip_status(lender_id, cursor):
    cursor.execute('SELECT * FROM TRIP WHERE LenderID = \'{}\' AND TripIsCompleted = 0 ORDER BY TripDate ASC'.format(lender_id))
    trip_list = cursor.fetchall()
    max = len(trip_list)

    if (max > 0):
        print('\nHere are your active trips:')
        for x in range(0, max):
            print('(' + str(x + 1) + ') Trip', trip_list[x][0], 'with borrower', trip_list[x][1], 'and vehicle', trip_list[x][3])

        lender_option = ask_for_int('\nWhich trip would you like to mark complete? (enter 0 to go back)', 1, max)
        if (lender_option > 0):
            cursor.execute('UPDATE TRIP SET TripIsCompleted = 1 WHERE LenderID = \'{}\' AND TripID = \'{}\''.format(lender_id, trip_list[lender_option - 1][0]))
            lender_rating = ask_for_float('\nWhat is your preferred rating for the borrower? (enter 0 to go back)', 1, 5)
            cursor.execute('UPDATE TRIP SET LenderRating = {} WHERE LenderID = \'{}\' AND TripID = \'{}\''.format(lender_rating, lender_id, trip_list[lender_option - 1][0]))
            cursor.execute('UPDATE VEHICLE SET VehicleIsListed = 1 WHERE LenderID = \'{}\' AND VehicleVIN = \'{}\''.format(lender_id, trip_list[lender_option - 1][3]))
            print('Updated successfully!')
        else:
            print('Returning to the menu screen.')
    else:
        print('You currently have no active trips.')

# Option 7
# -------------------------------------------------------------------------------------------------

def lender_view_history(lender_id, cursor):
    cursor.execute('SELECT * FROM TRIP WHERE LenderID = \'{}\' AND TripIsCompleted = 1 ORDER BY TripDate ASC'.format(lender_id))
    trip_list = cursor.fetchall()
    max = len(trip_list)

    if (max > 0):
        print('\nHere are your completed trips:')
        for x in range(0, max):
            print('(' + str(x + 1) + ')', trip_list[x][4])

        lender_option = ask_for_int('\nWhich trip would you like to check the information of? (enter 0 to go back)', 1, max)
        if (lender_option > 0):
            cursor.execute('SELECT * FROM TRIP WHERE LenderID = \'{}\' AND TripID = \'{}\''.format(lender_id, trip_list[lender_option - 1][0]))
            trip_info = cursor.fetchall()
            for x in trip_info:
                for y in range(0, len(x)):
                    if (x[y] != 1 and x[y] != lender_id):
                        print(trip_values[y] + ':', x[y])
        else:
            print('Returning to the menu screen.')
    else:
        print('You currently have no vehicles in the database.')
