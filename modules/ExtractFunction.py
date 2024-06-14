from sympy import symbols, sympify, latex
from sympy.parsing.sympy_parser import parse_expr
from sympy.utilities.lambdify import lambdify


def make_pretty_expr(expression):
    return rf"${latex(parse_expr(expression))}$"


def read_expression(expression):
    out_list = []
    try:
        if "x" in expression:
            function = parse_expr(expression)
            for symbol in function.free_symbols:
                if str(symbol) != 'x':
                    out_list.append(str(symbol))
            out_list.sort()
            out_list = ["x"] + out_list
            return lambdify(out_list, function), out_list[1:]
        else:
            return "", out_list
    except Exception:
        return "", out_list
