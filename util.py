import tkinter as tk
from tkinter import messagebox

def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
                        window,
                        text=text,
                        activebackground="black",
                        activeforeground="white",
                        fg=fg,
                        bg=color,
                        command=command,
                        height=2,
                        width=20,
                        font=('Helvetica bold', 15)
                    )

    return button
def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label
def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 15), justify="left")
    return label


def get_entry_text(window):
    inputtxt = tk.Text(window,
                       height=1,
                       width=10, font=("Arial", 31))
    return inputtxt


def msg_box(title, description):
    messagebox.showinfo(title, description)








