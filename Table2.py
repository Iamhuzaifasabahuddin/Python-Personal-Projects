import sqlite3

connection = sqlite3.connect('Your_file_name.db')

cursor = connection.cursor()
print("Connection established")

connection.execute('''CREATE TABLE Table_name
        (USERNAME      TEXT    NOT NULL,
        ACCOUNT           TEXT    NOT NULL,
        PASSWORD           TEXT     NOT NULL);''')

print("Table created")
