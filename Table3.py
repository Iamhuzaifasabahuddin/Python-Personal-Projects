import sqlite3

connection = sqlite3.connect("Expenses.db")
cursor = connection.cursor()

print("Connection Established")
cursor.execute('''CREATE TABLE expenses
        (DATE      DATE    NOT NULL,
        CATEGORY   TEXT    NOT NULL,
        AMOUNT     FLOAT     NOT NULL);''')

print("Table Created Successfully!")
