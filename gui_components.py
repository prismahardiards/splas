import tkinter as tk
from tkinter import Menu
from file_operations import clear_all, open_file, save_file, save_as_file, close_file
from question_generation import generate_question
from html_generation import generate_html

def create_menu(app):
    menubar = Menu(app)

    file_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label="Open", command=lambda: open_file(app))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=app.quit)
    menubar.add_cascade(label="File", menu=file_menu)

    app.config(menu=menubar)

def create_source_code_frame(app):
    source_code_frame = tk.Frame(app)
    source_code_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

    tk.Label(source_code_frame, text="Source Code:").pack(anchor=tk.W)
    app.source_code_text = tk.Text(source_code_frame, height=10)
    app.source_code_text.pack(fill=tk.BOTH, expand=True)

def create_question_code_frame(app):
    question_code_frame = tk.Frame(app)
    question_code_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

    tk.Label(question_code_frame, text="Question Code:").pack(anchor=tk.W)
    app.question_code_text = tk.Text(question_code_frame, height=10)
    app.question_code_text.pack(fill=tk.BOTH, expand=True)

def create_bottom_frame(app):
    bottom_frame = tk.Frame(app)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

    tk.Button(bottom_frame, text="Clear All", command=lambda: clear_all(app)).pack(side=tk.LEFT, padx=5)
    tk.Button(bottom_frame, text="Generate HTML", bg="yellow", command=lambda: generate_html(app)).pack(side=tk.RIGHT, padx=5)
    tk.Button(bottom_frame, text="Generate Problems", command=lambda: generate_question(app)).pack(side=tk.RIGHT, padx=5)