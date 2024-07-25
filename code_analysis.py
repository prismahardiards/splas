import tkinter as tk
from utilizes import extract_elements

def analyze_file(app, content):
    keywords, functions, libraries, variables, constants, operators, outputs, output_values = extract_elements(content)

    analysis_result = (
        f"Keywords:\n{', '.join(keywords)}\n\n"
        f"Functions:\n{', '.join(func + '()' for func in functions)}\n\n"
        f"Libraries:\n{', '.join(libraries)}\n\n"
        f"Variables:\n{', '.join(variables)}\n\n"
        f"Constants:\n{', '.join(constants)}\n\n"
        f"Operators:\n{', '.join(operators)}\n\n"
        f"Outputs:\n{', '.join(outputs)}\n\n"
        f"Output Values:\n{', '.join(output_values)}"
    )

    print("Source Code:")
    lines = content.split('\n')
    for i, line in enumerate(lines, start=1):
        print(f"{i:>4}: {line}")

    print("\nAnalysis Result:")
    print(analysis_result)

    app.question_code_text.delete(1.0, tk.END)
