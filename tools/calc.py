import sympy as sp


def calculate(expression):
    parts = expression.split()

    if parts[1] == "*":
        return float(parts[0]) * float(parts[2])
    elif parts[1] == "+":
        return float(parts[0]) + float(parts[2])
    elif parts[1] == "-":
        return float(parts[0]) - float(parts[2])
    elif parts[1] == "/":
        return float(parts[0]) / float(parts[2])