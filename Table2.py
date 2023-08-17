import sqlite3

connection = sqlite3.connect('Passwords.db')

cursor = connection.cursor()
print("Connection established")

# f = connection.execute("SELECT * FROM manager")
#
# f = cursor.execute("DELETE FROM manager")
f1 = cursor.execute("SELECT USERNAME, ACCOUNT, PASSWORD FROM manager WHERE USERNAME=?", ("Facebook",))

res = f1.fetchall()
for r in res:
    print(r[1])

