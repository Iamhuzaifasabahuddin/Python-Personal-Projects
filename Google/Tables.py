import sqlite3

connection = sqlite3.connect('Timetable.db')

cursor = connection.cursor()
print("Connection established")

connection.execute('''CREATE TABLE hours
        (DATE       DATE    NOT NULL,
        CATEGORY           TEXT    NOT NULL,
        HOURS            INT     NOT NULL);''')

print("Table created")
