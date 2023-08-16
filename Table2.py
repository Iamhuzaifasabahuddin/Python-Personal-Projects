import sqlite3

connection = sqlite3.connect('Passwords.db')

cursor = connection.cursor()
print("Connection established")

# f = connection.execute("SELECT * FROM manager")

f = cursor.execute("DELETE FROM manager")

connection.commit()

print(f.fetchall())


