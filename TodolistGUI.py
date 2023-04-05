import tkinter as tk

Tasks = []

def add_items(item: str, listbox: tk.Listbox):
    if item not in Tasks:
        Tasks.append(item)
        listbox.insert(tk.END, f"{len(Tasks)}. {item}")
        print("Task has been added")
    else:
        print("Task already exists")

    with open("tasks.txt", "w") as f:
        for index, items in enumerate(Tasks):
            f.write(f"{index+1} {items}\n")

def view_list(listbox: tk.Listbox):
    for index, items in enumerate(Tasks, start=1):
        listbox.insert(tk.END, f"{index}. {items}")

def complete_list(item: str, listbox: tk.Listbox):
    if item not in Tasks:
        print("Task does not exist")
    else:
        Tasks.remove(item)
        listbox.delete(0, tk.END)
        view_list(listbox)
        print("Task has been removed")

    with open("tasks.txt", "w") as f:
        for index, items in enumerate(Tasks, start=1):
            f.write(f"{index} {items}\n")



def on_add_click(entry: tk.Entry, listbox: tk.Listbox,  message_label: tk.Label):
    task = entry.get()
    if task:
        if task in Tasks:
            message_label.config(text="Task already exist")
        else:
            add_items(task, listbox)
            entry.delete(0, tk.END)
            message_label.config(text="Task added successfully")


def on_complete_click(entry: tk.Entry, listbox: tk.Listbox, message_label: tk.Label):
    task = entry.get()
    if task:
        if task not in Tasks:
            message_label.config(text="Task does not exist")
        else:
            complete_list(task, listbox)
            entry.delete(0, tk.END)
            message_label.config(text="Task has been completed")



def main():
    window = tk.Tk()
    window.title("Task Manager")


    add_label = tk.Label(window, text="Add task:", font=("oswald", 20, "italic"))
    add_entry = tk.Entry(window, font=("oswald", 20))
    add_button = tk.Button(window, text="Add",
                           command=lambda: on_add_click(add_entry, task_listbox, message_label),  font=("oswald", 20))

    message_label = tk.Label(window, text="", font=("oswald", 16))
    message_label.pack()

    complete_label = tk.Label(window, text="Mark task as complete:", font=("oswald", 20, "italic"))
    complete_entry = tk.Entry(window,  font=("oswald", 20))
    complete_button = tk.Button(window, text="Complete",
                                command=lambda: on_complete_click(complete_entry, task_listbox, message_label),  font=("oswald", 20))

    task_listbox = tk.Listbox(window,  font=("oswald", 20), width=20)

    add_label.pack(pady=5)
    add_entry.pack(pady=5)
    add_button.pack(pady=5)
    add_entry.bind('<Return>', lambda event: on_add_click(add_entry, task_listbox, message_label))

    complete_label.pack(pady=5)
    complete_entry.pack(pady=5)
    complete_button.pack(pady=5)
    complete_entry.bind('<Return>', lambda event: on_complete_click(complete_entry, task_listbox, message_label))

    task_listbox.pack(pady=5, )

    with open("tasks.txt", "r") as f:
        for line in f:
            index, task = line.strip().split(" ", maxsplit=1)
            Tasks.append(task)
            task_listbox.insert(tk.END, f"{index}. {task}")

    window.mainloop()


if __name__ == "__main__":
    main()
