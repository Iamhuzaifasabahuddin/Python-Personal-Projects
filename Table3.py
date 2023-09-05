import sqlite3

connection = sqlite3.connect("Expenses.db")
cursor = connection.cursor()

print("Connection Established")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Transactions (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Date DATE NOT NULL,
        Category TEXT NOT NULL,
        Description TEXT,
        Amount FLOAT NOT NULL,
        Total FLOAT  NOT NULL
    )
''')
cursor.execute("SELECT * FROM Transactions")
print(cursor.fetchall())
print("Table Created Successfully!")
