import os
import pwinput  # type: ignore
import time


def master_password(password: str):
    with open("master.txt", 'w') as f:
        f.write(f"Master password: {password}")


def master_check(password: str):
    with open("master.txt", 'r') as f:
        for line in f:
            if line.startswith("Master password"):
                if password in line.split():
                    return True
                return False


def add(account, username, password):
    with open("Passwords.txt", 'a') as f:
        f.write(f"Account: {account}, Username: {username}, Password: {password}\n")


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



def view():
    with open("Passwords.txt", 'r') as f:
        for line in f:
            print(line.strip())


def exists(account):
    found = False
    with open("Passwords.txt", 'r') as f:
        for line in f:
            if line.startswith(f"Account: {account},"):
                found = True
        return found

def search(account):
    with open("Passwords.txt", 'r') as f:
        for line in f:
            if line.startswith(f"Account: {account},"):
                print(line)
            else:
                print(f"Account: {account} not found")


def main():
    attempts = 3
    for count in range(3):
        pwd = pwinput.pwinput(prompt="Enter password: ", mask="X")
        if master_check(pwd):
            while True:
                try:
                    print("Enter what operation you want to perform")
                    op = str(input("Operation add/view/remove/search/exit: ")).lower()
                    if op not in ["add", "view", "remove", "search", "exit"]:
                        print("Invalid operation")
                    else:
                        if op == "add":
                            ac = str(input("Enter account: ")).capitalize()
                            if exists(ac) is False:
                                un = str(input("Enter username: "))
                                pw = pwinput.pwinput(prompt="Enter password: ", mask="X")
                                add(ac, un, pw)
                            print("Account already exists")
                        if op == "view":
                            view()
                        if op == "remove":
                            ac = str(input("Enter account to remove: ")).capitalize()
                            remove(ac)
                        if op == "search":
                            ac = str(input("Enter account to search: ")).capitalize()
                            search(ac)
                        if op == "exit":
                            print("Exiting...")
                            break
                except TypeError:
                    print("Invalid Type entered")
                except ValueError:
                    print("Invalid Value entered")
                except Exception as e:
                    print("Error: " + str(e))
        else:
            print("Invalid master password")
        if count < attempts - 1:
            print("Please try again...")
            time.sleep(2)
        else:
            print("Try again later...")
            break


if __name__ == '__main__':
    main()
