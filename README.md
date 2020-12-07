# capstone
PSIS  4191 Capstone Project &amp; Senior Thesis

This project utilizes an Azure Database for MySQL. Individuals must have their network whitelisted in order for the code to work.

The dummy records for 'borrower' and 'lender' all have logins as follows:

Borrower: 'B0001', 'B0002', ... 'B0100'
Lender: 'L0001', 'B0002', ... 'L0025'

Password: password

The latest version of Python is required to run this program. Comments within the code have been extremely limited due to the complexity and length of the code.

A lender can add or remove a vehicle from the database, as well as list it for borrowers.

A borrower can rent any listed vehicle, and the lender determines when the trip is over through the 'check trip status' option.

The lender can then rate the trip on a star rating (1-5), and the borrower can do it after.

There are 4 tables within the database schema: borrower, lender, vehicle, trip
