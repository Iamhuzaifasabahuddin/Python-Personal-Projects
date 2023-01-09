Tasks = []


def add_items(item: str):
    if item not in Tasks:
        Tasks.append(item)
        print("Task has been added")
    else:
        print("Task already exist")
    with open("tasks.txt", "w") as f:
        for index, items in enumerate(Tasks):
            f.write(str(index)+" "+items)


def view_list():
    for index, items in enumerate(Tasks, start=1):
        print(str(index)+" "+items)


def complete_list(item: str):
    if item not in Tasks:
        print("Task does not exist")
    else:
        Tasks.remove(item)
        print("Task has been removed")
    with open("tasks.txt", "w") as f:
        for index, items in enumerate(Tasks):
            f.write(str(index) + " " + items)


if __name__ == "__main__":
    while True:
        operation = str(input("Enter operation you wish to entertain add/view/complete: "))
        if operation.lower() not in ["add", "view", "complete"]:
            print("Invalid operation")

        if operation.lower() == "add":
            add = input("Enter a task to be added to the list: ")
            add_items(add)

        elif operation.lower() == "view":
            view_list()

        elif operation.lower() == "complete":
            complete = input("Enter a task that has been completed: ")
            complete_list(complete)



