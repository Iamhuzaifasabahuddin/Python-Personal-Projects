Task = []


def add(item: str):
    Task.append(item)
    return f"{item} has been added to the list:{Task}"


def view():
    for index, items in enumerate(Task, start=1):
        print(f"{index}:{items}")


def complete(item: str):
    Task.remove(item)
    return f"{item} has been removed from the list:{Task}"


if __name__ == "__main__":
    while True:
        operation = str(input("Enter operation you wish to entertain add/view/complete: "))
        if operation.lower() not in ["add", "view", "complete"]:
            print("Invalid operation")

        if operation.lower() == "add":
            task = input("Enter task you would like to add: ")
            if task in Task:
                print("Task already exists")
            else:
                add(task)
                print("Task added")
        elif operation.lower() == "view":
            print("List of tasks is:")
            view()
        elif operation.lower() == "complete":
            task = input("Enter task you would like to complete: ")
            if task in Task:
                complete(task)
                print("Task completed")
            else:
                print("Task does not exist")






