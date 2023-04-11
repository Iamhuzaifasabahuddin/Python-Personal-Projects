import os
import pwinput  # type: ignore


def add(account, username, password):
    with open("Passwords.txt", 'a') as f:
        f.write(f"Account: {account}, Username: {username}, Password: {password}\n")


def remove(account):
    found = False
    print(f"Removing account '{account}'...")
    with open("Passwords.txt", 'r') as f, open("temp.txt", 'w') as temp:
        for line in f:
            if not line.startswith(f"Account: {account},"):
                temp.write(line)
            else:
                found = True
        if not found:
            print(f"Account '{account}' doesn't exist")
        else:
            os.replace("temp.txt", "Passwords.txt")
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


def main():
    while True:
        try:
            print("Enter what operation you want to perform")
            op = str(input("Operation add/view/remove/exit: ")).lower()
            if op not in ["add", "view", "remove", "exit"]:
                print("Invalid operation")
            else:
                if op == "add":
                    ac = str(input("Enter account: "))
                    if exists(ac) is False:
                        un = str(input("Enter username: "))
                        pw = pwinput.pwinput(prompt="Enter password: ", mask="X")
                        add(ac, un, pw)
                    print("Account already exists")
                if op == "view":
                    view()
                if op == "remove":
                    ac = str(input("Enter account to remove: "))
                    remove(ac)
                if op == "exit":
                    print("Exiting...")
                    break
        except TypeError:
            print("Invalid Type entered")
        except ValueError:
            print("Invalid Value entered")
        except Exception as e:
            print("Error: " + str(e))


if __name__ == '__main__':
    main()
