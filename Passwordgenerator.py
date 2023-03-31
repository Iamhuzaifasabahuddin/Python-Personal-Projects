import random
import tkinter as tk
import string


def generator(password_length: int, is_digit: bool = True, is_special: bool = True):
    Letters = string.ascii_letters
    Numbers = string.digits
    Special = string.punctuation
    character = Letters

    if is_digit:
        character += Numbers
    if is_special:
        character += Special

    password = ""
    password = "".join(random.SystemRandom().choice(character) for _ in range(password_length))
    return password


def main():
    window = tk.Tk()
    window.title("Password generator")

    heading = tk.Label(window, text="Password generator", font=("oswald", 50, "italic"),
                       fg="black", background="gold", relief="groove", pady=10)
    heading.pack()

    length_label = tk.Label(window, text="Enter password length:", font=("oswald", 20), pady=10)
    length_label.pack()

    length_entry = tk.Entry(window, font=("oswald", 20), relief="raised")
    length_entry.pack()

    numeric_label = tk.Label(window, text="Do you want numbers? (leave blank if not): ", font=("oswald", 20), pady=10)
    numeric_label.pack()

    numeric_entry = tk.Entry(window, font=("oswald", 20), relief="raised")
    numeric_entry.insert(0, 'True')
    numeric_entry.pack()

    special_label = tk.Label(window, text="Do you want special characters? (leave blank if not): ",
                             font=("oswald", 20), pady=10)
    special_label.pack()


    special_entry = tk.Entry(window, font=("oswald", 20))
    special_entry.insert(0, 'True')
    special_entry.pack()

    generated = tk.Label(window, text="Click the button to generate a password",
                         font=("oswald", 25, "italic"), relief="raised", pady=10)
    generated.pack()

    def update_password():
        password_length = length_entry.get()
        if not password_length or int(password_length) <= 0:
            generated.config(text="Error: Invalid password length")
            return
        password_length = int(password_length)
        nums_check = bool(numeric_entry.get())
        special_check = bool(special_entry.get())
        password = generator(password_length, nums_check, special_check)
        generated.config(text=password)

    update_password_button = tk.Button(window, text="Generate password", font=("oswald", 20),
                                       command=update_password, relief="solid", pady=20)
    update_password_button.pack()

    window.mainloop()


if __name__ == '__main__':
    main()
