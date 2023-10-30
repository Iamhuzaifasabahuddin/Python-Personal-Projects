import mysql.connector

db = mysql.connector.connect(
    user='root',
    password='Hexz7799*',
    host='localhost',
    port=3306,
    database='pharmaceutical_company',
    auth_plugin='mysql_native_password'
)

cursor = db.cursor()
cursor.execute("SELECT * FROM Employees")

print(cursor.fetchall())

# ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Hexz7799*';
