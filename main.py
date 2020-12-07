from menu import main_menu
from connect import open
from disconnect import close

import mysql.connector
from mysql.connector import ClientFlag

# Obtain connection string information from the portal
config = {
    'host': 'steve-larisa-edrees.mysql.database.azure.com',
    'user': 'capstone@steve-larisa-edrees',
    'password': 'JI6xF10Gfrdj',
    'database': 'autoshare'
    # 'client_flags': [ClientFlag.SSL],
    # 'ssl_key': '',
    # 'ssl_cert': '~/dev/keys/DigiCertGlobalRootG2.crt.pem'
}

# Define the main which will print the first line, call main_menu, and print the last line.
def main():
    conn = mysql.connector.connect(**config)
    cursor = open(conn)
    main_menu(cursor)
    close(conn, cursor)


# Run the main
main()
