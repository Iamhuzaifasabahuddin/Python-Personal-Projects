import os


def remove(account):
    found = False
    with open("Passwords.txt", 'r') as f, open("temp.txt", 'w') as temp:
        for line in f:
            if not line.startswith(f"Account: {account},"):
                temp.write(line)
            else:
                found = True
        if not found:
            print(f"Account '{account}' doesn't exist")
        else:
            print(f"Removing account '{account}'...")
            os.replace('temp.txt', 'Passwords.txt')
            print(f"Account '{account}' successfully removed")

remove('res'.capitalize())