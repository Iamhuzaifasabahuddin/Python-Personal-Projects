import sqlite3


def update_data(username, new_username, new_account, new_password):
    connection = sqlite3.connect('Passwords.db')
    cursor = connection.cursor()

    # query = "UPDATE manager SET USERNAME=?, ACCOUNT=?, PASSWORD=? WHERE USERNAME=?"
    # cursor.execute(query, (new_username, new_account, new_password, username))

    connection.commit()

    f = cursor.execute("SELECT * FROM manager")
    print(f.fetchall())

# Usage example:
update_data("", "NewUsername", "NewAccount", "NewPassword")
