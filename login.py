import sys
import getpass

def user_login(user_type, cursor):
    if (user_type == 1):
        table = 'borrower'
    elif (user_type == 2):
        table = 'lender'
    else:
        print('Something bad happened. Abort mission!')
        exit(1)

    user_id = input('Please enter your account ID: ').upper()
    cursor.execute('SELECT EXISTS(SELECT * FROM {} WHERE {}ID = \'{}\')'.format(table.upper(), table.title(), user_id))
    user_exists = cursor.fetchall()[0][0]
    if (user_exists == 1):
        count = 5
        while True:
            count -= 1
            user_password = getpass.getpass(prompt='Please enter your password: ')
            cursor.execute('SELECT {}Password FROM {} WHERE {}ID = \'{}\''.format(table.title(), table.upper(), table.title(), user_id))
            check_password = cursor.fetchall()[0][0]
            if (user_password == check_password):
                print('Correct password.')
                break
            else:
                if (count == 0):
                    print('You have been locked out of your account.')
                    exit(1)
                else:
                    plural = ''
                    if (count != 1):
                        plural = 's'
                    print('Incorrect password. You have', count, 'login attempt' + plural, 'left.')
        return user_id
    else:
        print('User does not exist.')
        return -1

# -------------------------------------------------------------------------------------------------

def admin_login():
    username = 'admin'
    password = 'admin123'

    check_un = input('Please enter your admin username: ').lower()
    if (username == check_un):
        count = 5
        while True:
            count -= 1
            check_pw = getpass.getpass(prompt='Please enter your password: ')
            if (password == check_pw):
                print('Correct password.')
                break
            else:
                if (count == 0):
                    print('You have been locked out of your account.')
                    exit(1)
                else:
                    plural = ''
                    if (count != 1):
                        plural = 's'
                    print('Incorrect password. You have', count, 'login attempt' + plural, 'left.')
        return True
    else:
        print('User does not exist.')
        return False
