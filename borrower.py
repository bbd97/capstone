from extras import ask_for_int, ask_for_float
from datetime import date

vehicle_values = ('VIN', 'Make', 'Model', 'Year', 'Color', 'License Plate Number', 'Capacity', 'Mileage', 'Miles Per Gallon', 'Type', 'Transmission', 'Smoking', 'Condition', 'Times Borrowed', 'Rental Price', 'Listed', 'Approved', 'Lender ID')
trip_values = ('Trip ID', 'User ID', 'Lender Username', 'Vehicle', 'Date Of Trip', 'Completed', 'Your Rating For Borrower', 'Lender\'s Rating For You')

# Option 1
# -------------------------------------------------------------------------------------------------

def borrower_rent_vehicle(borrower_id, cursor):
    cursor.execute('SELECT TripIsCompleted FROM TRIP WHERE BorrowerID = \'{}\''.format(borrower_id))
    borrower_status = cursor.fetchall()
    vehicle_is_being_rented = 0
    for x in range(0, len(borrower_status)):
        for y in range(0, len(borrower_status[x])):
            if (borrower_status[x][y] == 0):
                vehicle_is_being_rented += 1

    if (vehicle_is_being_rented == 0):
        cursor.execute('SELECT * FROM VEHICLE WHERE VehicleIsListed = 1')
        vehicle_list = cursor.fetchall()
        max = len(vehicle_list)

        if (max > 0):
            print('\nHere are the listed vehicles:')
            for x in range(0, max):
                print('(' + str(x + 1) + ')', vehicle_list[x][0])
            
            borrower_option = ask_for_int('\nWhich vehicle would you like to rent? (enter 0 to go back)', 1, max)
            if (borrower_option > 0):
                vehicle_selection = vehicle_list[borrower_option - 1][0]

                cursor.execute('SELECT TripID FROM TRIP ORDER BY TripID DESC LIMIT 1')

                previous_trip_id = cursor.fetchall()[0][0]
                trip_id = int(previous_trip_id.replace('T', ''))
                trip_id = str(trip_id + 1)
                trip_id = 'T' + trip_id.zfill(4)
                
                cursor.execute('SELECT LenderID FROM VEHICLE WHERE VehicleVIN = \'{}\''.format(vehicle_selection))
                lender_id = cursor.fetchall()[0][0]

                current_date = date.today().strftime('%m/%d/%Y')

                cursor.execute('UPDATE VEHICLE SET VehicleIsListed = 0 WHERE VehicleVIN = \'{}\''.format(vehicle_selection))
                cursor.execute('INSERT INTO TRIP VALUES\n(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', 0, NULL, NULL)'.format(trip_id, borrower_id, lender_id, vehicle_selection, current_date))
                print('You are now renting this vehicle! Enjoy your trip.')
        else:
            print('There are currently no listed vehicles.')
    else:
        print('You are currently renting a vehicle!')

# Option 2
# -------------------------------------------------------------------------------------------------

def borrower_rate_trip(borrower_id, cursor):
    cursor.execute('SELECT * FROM TRIP WHERE BorrowerID = \'{}\' AND TripIsCompleted = 1 AND BorrowerRating IS NULL'.format(borrower_id))
    trip_list = cursor.fetchall()

    max = len(trip_list)

    if (max > 0):
        print('\nHere are your recently completed trips:')
        for x in range(0, max):
            print('(' + str(x + 1) + ') Trip', trip_list[x][0], 'with lender', trip_list[x][2], 'and vehicle', trip_list[x][3])

        borrower_option = ask_for_int('\nWhich trip would you like to rate? (enter 0 to go back)', 1, max)
        if (borrower_option > 0):
            borrower_rating = ask_for_float('\nWhat is your preferred rating for the lender? (enter 0 to go back)', 1, 5)
            cursor.execute('UPDATE TRIP SET BorrowerRating = {} WHERE BorrowerID = \'{}\' AND TripID = \'{}\''.format(borrower_rating, borrower_id, trip_list[borrower_option - 1][0]))
            print('Updated successfully!')
        else:
            print('Returning to the menu screen.')
    else:
        print('You currently have no unrated trips.')

# Option 3
# -------------------------------------------------------------------------------------------------

def borrower_view_history(borrower_id, cursor):
    cursor.execute('SELECT * FROM TRIP WHERE BorrowerID = \'{}\' AND TripIsCompleted = 1 ORDER BY TripDate ASC'.format(borrower_id))
    trip_list = cursor.fetchall()
    max = len(trip_list)

    if (max > 0):
        print('\nHere are your completed trips:')
        for x in range(0, max):
            print('(' + str(x + 1) + ')', trip_list[x][4])

        borrower_option = ask_for_int('\nWhich trip would you like to check the information of? (enter 0 to go back)', 1, max)
        if (borrower_option > 0):
            cursor.execute('SELECT * FROM TRIP WHERE BorrowerID = \'{}\' AND TripID = \'{}\''.format(borrower_id, trip_list[borrower_option - 1][0]))
            trip_info = cursor.fetchall()
            for x in trip_info:
                for y in range(0, len(x)):
                    if (x[y] != 1 and x[y] != borrower_id):
                        print(trip_values[y] + ':', x[y])
        else:
            print('Returning to the menu screen.')
    else:
        print('You currently have no trip history.')



