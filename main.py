import tkinter as tk
from tkinter import Menu, filedialog, messagebox, simpledialog
from gui_components import create_menu, create_source_code_frame, create_question_code_frame, create_bottom_frame
from database import setup_database
from file_operations import clear_all, open_file, save_file, save_as_file, close_file
from question_generation import generate_question
from html_generation import generate_html

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Desktop Version Statistics PLAS")
        self.geometry("800x600")

        create_menu(self)
        create_source_code_frame(self)
        create_question_code_frame(self)
        create_bottom_frame(self)

        self.setup_database()
        
        self.create_question_number_frame()

    def setup_database(self):
        setup_database()

    def create_question_number_frame(self):
        question_number_frame = tk.Frame(self)
        question_number_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(question_number_frame, text="Question Number:").pack(side=tk.LEFT)
        self.question_number_var = tk.IntVar(value="")
        tk.Entry(question_number_frame, textvariable=self.question_number_var, width=5).pack(side=tk.LEFT)

if __name__ == "__main__":
    app = Application()
    app.mainloop()