import tkinter as tk
import random
import re
from tkinter import messagebox
from utilizes import extract_elements
import networkx as nx
import matplotlib.pyplot as plt # type: ignore

def generate_question(app):
    source_code = app.source_code_text.get(1.0, tk.END)
    if not source_code.strip():
        messagebox.showerror("Error", "Source code is empty.")
        return

    lines = source_code.split('\n')
    placeholders = set()
    answers_efp = []
    answer_gup = set()
    answer_vtp = set()
    placeholder_count = 1
    modified_lines = []

    keywords, functions, libraries, variables, constants, operators, outputs, output_values = extract_elements(source_code)

    # Create graph
    G = nx.Graph()

    for line in lines:
        if "=" in line:
            lhs, rhs = line.split('=', 1)
            rhs_cleaned = re.sub(r'\[\s*\d+(?:\s*,\s*\d+)*\s*\]', '', rhs)
            rhs_variables = [
                var for var in re.findall(r'\b([a-zA-Z_]\w*)\b', rhs_cleaned)
                if var not in {"for", "in", "if"} and (re.match(r'^[a-zA-Z_]+\d*$', var) or re.match(r'^[a-zA-Z_]+$', var))
            ]
            rhs_operators = re.findall(r'(\*\*|//|[-+*/%&|^~<>])', rhs_cleaned)
            rhs_constants = re.findall(r'\b(\d+)\b', rhs_cleaned)

            # Add nodes and edges to the graph with attributes
            all_elements = rhs_variables + rhs_operators + rhs_constants
            for elem in all_elements:
                if elem in rhs_variables:
                    G.add_node(elem, type='variable')
                elif elem in rhs_operators:
                    G.add_node(elem, type='operator')
                elif elem in rhs_constants:
                    G.add_node(elem, type='constant')
            for i in range(len(all_elements)):
                for j in range(i + 1, len(all_elements)):
                    if G.has_edge(all_elements[i], all_elements[j]):
                        G[all_elements[i]][all_elements[j]]['weight'] += 1
                    else:
                        G.add_edge(all_elements[i], all_elements[j], weight=1)

            elements_with_positions = [(match.start(), match.group()) for match in re.finditer(r'\b\w+\b|[-+*/%()]', rhs)]

            if len(rhs_variables) > 3:
                selected_vars = random.sample(rhs_variables, 2)
            elif len(rhs_variables) > 0:
                selected_vars = random.sample(rhs_variables, 1)
            else:
                selected_vars = []

            if len(rhs_operators) > 1:
                selected_ops = random.sample(rhs_operators, 1)
            else:
                selected_ops = rhs_operators

            if len(rhs_constants) > 1:
                selected_consts = random.sample(rhs_constants, 1)
            else:
                selected_consts = rhs_constants

            elements = selected_vars + selected_ops + selected_consts

            elements_positions = [(match.start(), match.group()) for match in re.finditer(r'\b\w+\b|[-+*/%()]', rhs)]
            elements_positions = [pos_elem for pos_elem in elements_positions if pos_elem[1] in elements]
            elements_positions.sort() 

            complex_expression = len(selected_vars) > 0 or len(selected_ops) > 0

            for pos, elem in elements_positions:
                if elem in elements and complex_expression:  
                    rhs_before = rhs  
                    if elem in selected_vars or elem in rhs_variables:
                        rhs = re.sub(r'\b' + re.escape(elem) + r'\b', f'_{placeholder_count}_', rhs, count=1)
                    elif elem in selected_consts or elem in rhs_constants:
                        rhs = re.sub(r'\b' + re.escape(elem) + r'\b', f'_{placeholder_count}_', rhs, count=1)
                    else:
                        rhs = re.sub(re.escape(elem), f'_{placeholder_count}_', rhs, count=1)
                    if rhs != rhs_before:  
                        answers_efp.append(elem)
                        placeholder_count += 1

            modified_line = f"{lhs}={rhs}"
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line)

    for keyword in keywords:
        keyword_used_in_efp = False

        for line in lines:
            if re.search(r'\b' + re.escape(keyword) + r'\b', line):
                elements_in_line = re.findall(r'\b\w+\b', line)
                if any(elem in elements_in_line for elem in answers_efp):
                    keyword_used_in_efp = True
                    break

        if not keyword_used_in_efp and not re.search(r'\[\s*\w+\s*\]', keyword):
            answer_gup.add(keyword)

    for line in lines:
        if "=" in line:
            lhs, rhs = line.split('=', 1)
            lhs = lhs.strip()
            elements_in_rhs = re.findall(r'\b\w+\b', rhs)
            if not any(elem in elements_in_rhs for elem in answers_efp) and not re.search(r'\[\s*\w+\s*\]', lhs):
                answer_gup.add(lhs)

    for line in lines:
        if "=" in line:
            lhs, rhs = line.split('=', 1)
            lhs = lhs.strip()
            elements_in_line = re.findall(r'\b\w+\b', line)
            if not any(elem in elements_in_line for elem in answers_efp) and not re.search(r'\[\s*\w+\s*\]', lhs):
                answer_gup.add(lhs)

    for function in functions:
        if function not in answers_efp:
            answer_gup.add(function)
    for library in libraries:
        if library not in answers_efp:
            answer_gup.add(library)

    filtered_outputs = [output for output in outputs if output.strip()]
    filtered_output_values = [value for value in output_values if value.strip()]

    min_length = min(len(filtered_outputs), len(filtered_output_values))
    filtered_outputs = filtered_outputs[:min_length]
    filtered_output_values = filtered_output_values[:min_length]

    output_values_dict = dict(zip(filtered_outputs, filtered_output_values))

    answer_vtp = set()
    for output in filtered_outputs:
        if output in output_values_dict:
            value = output_values_dict[output]
            if value:
                answer_vtp.add(f"{output} : {value}")

    answer_vtp_list = list(answer_vtp)

    # Apply the rule for even and odd lengths
    if len(answer_vtp_list) > 1:
        if len(answer_vtp_list) % 2 == 0:
            answer_vtp_list = random.sample(answer_vtp_list, len(answer_vtp_list) // 2)
        else:
            answer_vtp_list = random.sample(answer_vtp_list, len(answer_vtp_list) // 2 + 1)

    answer_vtp = set(answer_vtp_list)

    # Calculate and detail the total weight of selected elements
    total_weight = 0
    edge_weights = []
    counted_edges = set()
    for elem in answers_efp:
        if elem in G:
            neighbors = list(G.neighbors(elem))
            for neighbor in neighbors:
                if neighbor in answers_efp:
                    edge = tuple(sorted([elem, neighbor]))
                    if edge not in counted_edges:
                        weight = G[elem][neighbor]['weight']
                        total_weight += weight
                        edge_weights.append(f"({elem}, {neighbor}): {weight}")
                        counted_edges.add(edge)

    print("Outputs List:", outputs)
    print("Output Values List:", output_values)
    print("Output Values Dictionary:", output_values_dict)

    print(
        "\nAnswers EFP:\n" + ", ".join(answers_efp) +
        "\nAnswer GUP:\n" + ", ".join(answer_gup) +
        "\nAnswer VTP:\n" + ", ".join(answer_vtp) +
        "\nTotal Weight of Selected Elements:\n" + str(total_weight) +
        "\nEdge Weights:\n" + "\n".join(edge_weights)
    )

    modified_source_code = '\n'.join(modified_lines)
    answer_text = "\nAnswers EFP:\n" + ", ".join(answers_efp)
    gup_text = "\nAnswer GUP:\n" + ", ".join(answer_gup)
    vtp_text = "\nAnswer VTP:\n" + ", ".join(answer_vtp)
    #weight_text = "\nTotal Weight of Selected Elements:\n" + str(total_weight)
    #edge_weights_text = "\nEdge Weights:\n" + "\n".join(edge_weights)

    app.question_code_text.delete(1.0, tk.END)
    app.question_code_text.insert(tk.END, modified_source_code + "\n" + answer_text + "\n" + gup_text + "\n" + vtp_text)
    #app.question_code_text.insert(tk.END, modified_source_code + "\n" + answer_text + "\n" + gup_text + "\n" + vtp_text + "\n" + weight_text + "\n" + edge_weights_text)

    app.answers_efp = answers_efp
    app.answer_gup = answer_gup
    app.answer_vtp = answer_vtp

    '''
    # Plotting the advanced graph
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, k=0.3)
    node_colors = []
    for node in G.nodes(data=True):
        if node[1]['type'] == 'variable':
            node_colors.append('red')
        elif node[1]['type'] == 'operator':
            node_colors.append('blue')
        elif node[1]['type'] == 'constant':
            node_colors.append('green')
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray', node_size=3000, font_size=10, font_weight='bold')
    plt.title("Advanced Graph of Variables, Constants, and Operators")
    plt.show()
    '''