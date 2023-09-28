import tkinter as tk
from ttkthemes import ThemedStyle
from tkinter import ttk, scrolledtext, messagebox


def dishes():
    raise NotImplementedError


def centered(window: tk.Tk, width: int, height: int) -> None:
    """
    Center a Tkinter window on the screen.

    Parameters:
        window (tk.Tk): The Tkinter window to be centered.
        width (int): The desired width of the window.
        height (int): The desired height of the window.
    """
    try:
        screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
        centered_width, centered_height = (screen_width - width) // 2, (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{centered_width}+{centered_height}")
    except TypeError as error:
        print(f"An Error occurred: {error}")


def gui():
    window = tk.Tk()
    window.title("Dishes App")
    centered(window, 500, 700)
    main_frame = tk.Frame()
    main_frame.pack(fill='both', expand=1)

    canvas = tk.Canvas(main_frame)

    vsb = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
    hsb = tk.Scrollbar(main_frame, orient='horizontal', command=canvas.xview)
    canvas.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)

    vsb.pack(fill='y', side='right')
    hsb.pack(fill='x', side='bottom')
    canvas.pack(side='left', fill='both', expand=1)

    canvas.update_idletasks()
    canvas_width = canvas.winfo_width()
    x = canvas_width // 2

    content_frame = tk.Frame(canvas)
    window_id = canvas.create_window((x, 0), window=content_frame, anchor="n")

    def update(event):
        updated_width = event.width
        new_width = updated_width // 2
        canvas.coords(window_id, new_width, 0)

    content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.bind("<Configure>", update)

    main_title = tk.Label(content_frame, text="Welcome To Recipe Generator!", font=("Quicksand", 25, "italic"))
    main_title.pack(pady=10)

    window.mainloop()


if __name__ == '__main__':
    gui()
