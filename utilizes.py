import re

def extract_elements(content):
    keywords = []
    functions = []
    libraries = []
    variables = []
    constants = []
    operators = []
    outputs = []
    output_values = []

    lines = content.split('\n')

    import_pattern = re.compile(r'^import\s+(\w+)')
    assignment_pattern = re.compile(r'(\w+)\s*=\s*(.*)')
    function_pattern = re.compile(r'(\w+)\s*\(.*\)')
    variable_pattern = re.compile(r'\b([a-zA-Z_]\w*)\b')
    constant_pattern = re.compile(r'\b(\d+(\.\d+)?)\b')
    operator_pattern = re.compile(r'(\*\*|[-+*/%])')
    print_pattern = re.compile(r'print\s*\((.*?)\)')
    output_value_pattern = re.compile(r':\s*(.*)')

    next_line_output_value = False

    for line_number, line in enumerate(lines, start=1):
        if next_line_output_value:
            next_line_match = constant_pattern.search(line.strip())
            if next_line_match:
                constants.append(next_line_match.group(0))
            next_line_output_value = False

        import_match = import_pattern.match(line.strip())
        if import_match:
            libraries.append(import_match.group(1))

        assignment_match = assignment_pattern.match(line.strip())
        if assignment_match:
            keyword = assignment_match.group(1)
            expression = assignment_match.group(2)

            keywords.append(keyword)

            function_matches = function_pattern.findall(expression)
            for func in function_matches:
                functions.append(func)

            expression_without_brackets = re.sub(r'\[.*?\]', '', expression)

            variable_matches = variable_pattern.findall(expression_without_brackets)
            for var in variable_matches:
                if var not in {"in", "for"} and not re.match(constant_pattern, var):
                    variables.append(var)

            constant_matches = constant_pattern.findall(expression_without_brackets)
            for const in constant_matches:
                constants.append(const[0])

            operator_matches = operator_pattern.findall(expression_without_brackets)
            for op in operator_matches:
                operators.append(op)

        print_match = print_pattern.search(line.strip())
        if print_match:
            print_expression = print_match.group(1)
            print_elements = re.findall(r'"(.*?)"|(\w+)', print_expression)
            for elem in print_elements:
                if elem[0]:
                    outputs.append(elem[0])

        output_value_match = output_value_pattern.search(line.strip())
        if output_value_match:
            value = output_value_match.group(1).strip()
            if value: 
                output_values.append(value)

    return keywords, functions, libraries, variables, constants, operators, outputs, output_values