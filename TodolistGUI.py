import tkinter as tk

Tasks = []


def is_valid_priority(priority: str) -> bool:
    return priority in ["!!!", "!!", "!", "None"]


def add_items(item: str, priority: str, listbox: tk.Listbox):
    if (item, priority) not in Tasks:
        Tasks.append((item, priority))
        listbox.insert(tk.END, f"{item} - {priority}")
        print("Task has been added")
    else:
        print("Task already exists")

    with open("tasks.txt", "w") as f:
        for task, prio in Tasks:
            f.write(f"{task} - {prio}\n")


def view_list(listbox: tk.Listbox):
    listbox.delete(0, tk.END)
    sorted_tasks = sorted(Tasks, key=lambda x: (
    "!!!" if x[1] == "!!!" else "!!" if x[1] == "!!" else "!" if x[1] == "!" else "None", x[0]))
    for task, prio in sorted_tasks:
        listbox.insert(tk.END, f"{task} - {prio}")


def complete_list(item: str, listbox: tk.Listbox):
    for task, prio in Tasks[:]:
        if task == item:
            Tasks.remove((task, prio))
            listbox.delete(0, tk.END)
            view_list(listbox)
            print("Task has been removed")
            break

    with open("tasks.txt", "w") as f:
        for task, prio in Tasks:
            f.write(f"{task} - {prio}\n")


def rearrange_tasks(listbox: tk.Listbox):
    Tasks.sort(
        key=lambda x: ("!!!" if x[1] == "!!!" else "!!" if x[1] == "!!" else "!" if x[1] == "!" else "None", x[0]))
    listbox.delete(0, tk.END)
    for task, prio in Tasks:
        listbox.insert(tk.END, f"{task} - {prio}")


def on_add_click(entry_task: tk.Entry, entry_priority: tk.Entry, listbox: tk.Listbox, message_label: tk.Label):
    task = entry_task.get()
    priority = entry_priority.get()

    if task and is_valid_priority(priority):
        if (task, priority) in Tasks:
            message_label.config(text="Task already exists")
        else:
            add_items(task, priority, listbox)
            entry_task.delete(0, tk.END)
            entry_priority.delete(0, tk.END)
            message_label.config(text="Task added successfully")
    else:
        message_label.config(text="Invalid priority! Use '!!!', '!!', '!', or 'None'")


def on_complete_click(entry_task: tk.Entry, listbox: tk.Listbox, message_label: tk.Label):
    task = entry_task.get()
    if task:
        complete_list(task, listbox)
        entry_task.delete(0, tk.END)
        message_label.config(text="Task has been completed")


def main():
    window = tk.Tk()
    window.title("Task Manager")

    message_label = tk.Label(window, text="", font=("oswald", 16))
    message_label.pack()

    add_label = tk.Label(window, text="Add task:", font=("oswald", 20, "italic"))
    add_entry_task = tk.Entry(window, font=("oswald", 20))
    add_label_priority = tk.Label(window, text="Priority:", font=("oswald", 20, "italic"))
    add_entry_priority = tk.Entry(window, font=("oswald", 20))
    add_button = tk.Button(window, text="Add",
                           command=lambda: on_add_click(add_entry_task, add_entry_priority, task_listbox,
                                                        message_label),
                           font=("oswald", 20))

    complete_label = tk.Label(window, text="Mark task as complete:", font=("oswald", 20, "italic"))
    complete_entry = tk.Entry(window, font=("oswald", 20))
    complete_button = tk.Button(window, text="Complete",
                                command=lambda: on_complete_click(complete_entry, task_listbox, message_label),
                                font=("oswald", 20))

    rearrange_button = tk.Button(window, text="Rearrange Tasks",
                                 command=lambda: rearrange_tasks(task_listbox),
                                 font=("oswald", 20))

    task_listbox = tk.Listbox(window, font=("oswald", 20), width=30)

    add_label.pack(pady=5)
    add_entry_task.pack(pady=5)
    add_label_priority.pack(pady=5)
    add_entry_priority.pack(pady=5)
    add_button.pack(pady=5)
    add_entry_task.bind('<Return>',
                        lambda event: on_add_click(add_entry_task, add_entry_priority, task_listbox, message_label))
    add_entry_priority.bind('<Return>',
                            lambda event: on_add_click(add_entry_task, add_entry_priority, task_listbox, message_label))

    complete_label.pack(pady=5)
    complete_entry.pack(pady=5)
    complete_button.pack(pady=5)
    complete_entry.bind('<Return>', lambda event: on_complete_click(complete_entry, task_listbox, message_label))

    rearrange_button.pack(pady=5)

    task_listbox.pack(pady=5)

    with open("tasks.txt", "r") as f:
        for line in f:
            task, prio = line.strip().split(" - ")
            if is_valid_priority(prio):
                Tasks.append((task, prio))
                task_listbox.insert(tk.END, f"{task} - {prio}")

    window.mainloop()


if __name__ == "__main__":
    main()
