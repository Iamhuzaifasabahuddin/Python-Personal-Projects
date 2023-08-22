def arithmetic_arranger(problems, show_results=False):
    if len(problems) > 5:
        return "Error: Too many problems."

    first_line = ""
    second_line = ""
    dashes_line = ""
    results_line = ""

    for problem in problems:
        parts = problem.split()
        operand1, operator, operand2 = parts[0], parts[1], parts[2]

        if operator not in ['+', '-']:
            return "Error: Operator must be '+' or '-'."

        if not operand1.isdigit() or not operand2.isdigit():
            return "Error: Numbers must only contain digits."

        if len(operand1) > 4 or len(operand2) > 4:
            return "Error: Numbers cannot be more than four digits."

        width = max(len(operand1), len(operand2)) + 2
        first_line += operand1.rjust(width) + "    "
        second_line += operator + " " + operand2.rjust(width - 2) + "    "
        dashes_line += '-' * width + "    "

        if show_results:
            result = str(eval(problem))
            results_line += result.rjust(width) + "    "

    formatted_output = first_line.rstrip() + "\n" + second_line.rstrip() + "\n" + dashes_line.rstrip()
    if show_results:
        formatted_output += "\n" + results_line.rstrip()

    return formatted_output
