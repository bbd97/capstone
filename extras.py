def ask_for_int(message, low, high):
    while True:
        try:
            x = int(input(message + ': '))

            if (x == 0):
                return x
            elif x in range(low, high + 1):
                return x
            elif (low == high):
                print('Your only option is the number', str(low) + '.')
            else:
                print('You need to enter a number between', low, 'and', str(high) + '.')

        except ValueError:
            print('Error! Please enter a valid integer. Try again.')

# -------------------------------------------------------------------------------------------------

def ask_for_float(message, low, high):
    while True:
        try:
            x = float(input(message + ': '))

            if (x % 0.5 != 0):
                print('The number must be a multiple of 0.5! Please try again.')
            elif (x == 0):
                return x
            elif (x >= low and x <= high):
                return x
            elif (low == high):
                print('Your only option is the number', str(low) + '.')
            else:
                print('You need to enter a number between',
                      low, 'and', str(high) + '.')

        except ValueError:
            print('Error! Please enter a valid integer. Try again.')

# -------------------------------------------------------------------------------------------------

def ask_for_input(message, input_type, low, high):
    while True:
        if (input_type == 'int'):
            type_output = 'n integer'
            while True:
                try:
                    string = int(input(message + ': '))
                    break
                except ValueError:
                    print('Error! Please enter a valid integer. Try again.')

        else:
            type_output = ' string'
            string = input(message + ': ')

        string = str(string)

        if (string == '0'):
            break
        elif (len(string) >= low and len(string) <= high):
            return string
        elif (low == high):
            print('You need to enter a' + type_output, 'exactly', low, 'character(s) long.')
        else:
            print('You need to enter a' + type_output, 'between', low, 'and', high, 'characters.')
    
# -------------------------------------------------------------------------------------------------

def ask_for_search(message, value_tuple, key):
    while True:
        query_match = False
        admin_search = input(message + ': ')

        if (key != 0 and admin_search == ''):
            return '*'
        else:
            for x in range (0, len(value_tuple)):
                if (admin_search.lower() == value_tuple[x].lower() or admin_search.lower() == '*'):
                    query_match = True

            if (query_match):
                return admin_search
            else:
                while True:
                    admin_option = input('Invalid option. Would you like to see your options? (Y/N): ').upper()
                    if (admin_option == 'Y'):
                        for x in range(0, len(value_tuple)):
                            separator = ''
                            if (x != len(value_tuple) - 1):
                                separator = ', '
                            print(value_tuple[x] + separator, end='')
                        print()
                        break
                    elif (admin_option == 'N'):
                        break
                    else:
                        print('Invalid input! Please try again.')
