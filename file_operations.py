import tkinter as tk
from tkinter import filedialog
import threading
from code_analysis import analyze_file

def clear_all(app):
    app.source_code_text.delete(1.0, tk.END)
    app.question_code_text.delete(1.0, tk.END)
    app.question_number_var.set("")

def open_file(app):
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
        app.source_code_text.delete(1.0, tk.END)
        app.source_code_text.insert(tk.END, content)
        threading.Thread(target=analyze_file, args=(app, content)).start()

def save_file(app):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(app.source_code_text.get(1.0, tk.END))

def save_as_file(app):
    save_file(app)

def close_file(app):
    clear_all(app)