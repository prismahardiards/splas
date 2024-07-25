import tkinter as tk
import random
import re
import sqlite3
import hashlib
import logging
from tkinter import filedialog, messagebox

logging.basicConfig(level=logging.INFO)

def generate_html(app):
    source_code = app.question_code_text.get(1.0, tk.END)
    if not source_code.strip():
        messagebox.showerror("Error", "Source code is empty.")
        return

    source_code = remove_answers_section(source_code)
    logging.info("Source code after removing Answers EFP, Answer GUP, Answer VTP:\n" + source_code)

    qNo = int(app.question_number_var.get())
    logging.info(f"Generating HTML for question number: {qNo}")

    encrypted_efp = [encrypt_str_with_params(elem, qNo, i + 1) for i, elem in enumerate(app.answers_efp)]
    logging.info(f"Encrypted EFP: {encrypted_efp}")

    start_index_gup = len(encrypted_efp) + 1
    logging.info(f"Start index GUP: {start_index_gup}")
    encrypted_gup = [encrypt_str_with_params(elem, qNo, start_index_gup + i) for i, elem in enumerate(app.answer_gup)]
    logging.info(f"Encrypted GUP: {encrypted_gup}")

    start_index_vtp = start_index_gup + len(encrypted_gup)
    logging.info(f"Start index VTP: {start_index_vtp}")
    encrypted_vtp = []
    for i, elem in enumerate(app.answer_vtp):
        if " : " in elem:
            key, value = elem.split(" : ", 1)
            if re.match(r'^-?\d+(\.\d+)?$', value):
                logging.info(f'Encrypting value: {value}')
                encrypted_value = encrypt_str_with_params(value, qNo, start_index_vtp + i)
                logging.info(f'Encrypted value: {encrypted_value}')
                encrypted_vtp.append(f"{key} : {encrypted_value}")
            else:
                encrypted_vtp.append(elem)
        else:
            encrypted_vtp.append(elem)

    logging.info(f"Encrypted VTP: {encrypted_vtp}")

    db_path = r'C:\Users\PRISMA\Documents\statistics-generator\statistics-generator\db\questions.db'
    fill_in_blank_problem = create_html(app, source_code, encrypted_efp, encrypted_gup, encrypted_vtp, qNo, db_path)

    file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(fill_in_blank_problem)
        messagebox.showinfo("Success", "HTML file has been saved.")

def create_html(app, source_code, encrypted_efp, encrypted_gup, encrypted_vtp, qNo, db_path):
    srcs = source_code.strip().split("\n")
    src = "\n".join(srcs[:-1])
    bf = []
    bf.append(f"<h2 id=\"statement\">{qNo}</h2>\nFill in Blanks<br>\n")
    bf.append("<DIV class=\"fl\" style=\"width: 670px; height: 620px\">")
    bf.append("<h4 id=\"code\">Source Code</h4>\n<pre class=\"prettyprint\" id=\"scoring-res\">\n")

    for i in range(len(encrypted_efp)):
        flg = f"_{i + 1}_"
        encryptedAnswer = encrypted_efp[i]
        src = re.sub(re.escape(flg), f"<input size=2 ans=\"{encryptedAnswer}\" placeholder=\"{i + 1}\"></input>", src, count=1)

    lines = src.split("\n")

    while lines and not lines[-1].strip():
        lines.pop()
    numbered_lines = []
    for idx, line in enumerate(lines):
        numbered_lines.append(f"{str(idx + 1).zfill(2)}: {line}")
    numbered_src = "\n".join(numbered_lines)

    bf.append(numbered_src.split("//@JPLAS")[0])

    bf.append("<br>\n")

    # update 16 July 2024
    question_index = 1
    start_index_gup = len(encrypted_efp) + 1

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for i, (gup, encryptedAnswer) in enumerate(zip(app.answer_gup, encrypted_gup)):
        placeholder_number = start_index_gup + i
        question_number = f"Q{question_index}"

        cursor.execute('SELECT question FROM elements WHERE element = ?', (gup,))
        result = cursor.fetchone()
        question = result[0] if result else gup

        bf.append(f"{question_number}. {question}? <input size=2 ans=\"{encryptedAnswer}\" placeholder=\"{placeholder_number}\"></input>\n")
        question_index += 1

    conn.close()

    start_index_vtp = start_index_gup + len(encrypted_gup)
    for i, vtp in enumerate(encrypted_vtp):
        key, value = vtp.split(" : ", 1)
        placeholder_number = start_index_vtp + i
        question_number = f"Q{question_index}"

        bf.append(f"{question_number}. What is the value of {key}? <input size=2 ans=\"{value}\" placeholder=\"{placeholder_number}\"></input>\n")
        question_index += 1

    bf.append("</DIV>\n")
    bf.append("</pre>\n")
    bf.append("<DIV class=\"fl\" style=\"width: 430px; height: 620px\">")
    bf.append("<h4 id=\"code\">Description</h4>\n<pre class=\"prettyprint\" id=\"scoring-res\">")
    bf.append("<img src=\"./img/1-mean.png\" alt=\"Mean\">\n</pre>\n</DIV>")

    bf.append("<DIV class=\"fr\" style=\"width: 1100px; height: 130px\">")
    bf.append("<h4 id=\"code1\">References</h4>\n<pre class=\"prettyprint\" id=\"scoring-res\">\n<h2 id=\"code1\"></h2>")
    bf.append("<a href=\"./references/references.pdf\" target=\"_blank\">Download</a>\n</pre>\n</DIV>")

    bf.append("<a class=\"btn\" href=\"javascript:newScoring()\">Answer</a>")
    bf.append("\n<script type=\"text/javascript\">\n$(function(){\n prettyPrint();\n});\n</script>")
    return ''.join(bf)

def encrypt_str_with_params(text, qNo, index):
    logging.info(f"Encrypting text: {text}, qNo: {qNo}, index: {index}")
    nText = f"{text}{qNo}{index}"
    md = hashlib.sha256()
    md.update(nText.encode())
    valueArray = md.digest()

    buffer = []
    for byte in valueArray:
        tmpStr = format(byte & 0xff, '02x')
        buffer.append(tmpStr)
    
    encrypted_text = ''.join(buffer)
    logging.info(f"Encrypted text: {encrypted_text}")
    return encrypted_text

def remove_answers_section(source_code):
    source_code = re.sub(r'Answers EFP.*?Answer VTP.*?\n', '', source_code, flags=re.DOTALL)
    return source_code