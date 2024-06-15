from sympy import symbols, sympify, latex
from sympy.parsing.sympy_parser import parse_expr
from sympy.utilities.lambdify import lambdify


def make_pretty_expr(expression):
    return rf"${latex(parse_expr(expression))}$"


def extract_x_function(expression):
    out_list = []
    try:
        function = parse_expr(expression)
        has_x = False
        for symbol in function.free_symbols:
            if str(symbol) != 'x':
                out_list.append(str(symbol))
            else:
                has_x = True
        if not has_x:
            raise ValueError("no x in expression")
        out_list.sort()
        out_list = ["x"] + out_list
        function = lambdify(out_list, function)
        return function, out_list[1:]
    except Exception as e:
        raise e


def extract_any_function(expression):
    out_list = []
    try:
        function = parse_expr(expression)
        for symbol in function.free_symbols:
            out_list.append(str(symbol))
        out_list.sort()
        function = lambdify(out_list, function)
        return function, out_list
    except Exception as e:
        raise e
