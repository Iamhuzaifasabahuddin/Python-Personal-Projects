import sqlite3


def delete_all_records():
    connection = sqlite3.connect("Passwords.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM manager")
    connection.commit()

    connection.close()


# Call the function to delete all records
delete_all_records()
