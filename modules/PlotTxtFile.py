import types

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from modules.ExtractFunction import read_expression, make_pretty_expr

"""""
Welcome to PlotTxtFile, here is a short manual description:
* fist get any experiment data as txt file and save it in TxtFiles (make sure to set right split sign)
* use plot_file to get basic plot of function
* set y_log/x_log=True to make y/x-axi logarithmic

fitting (see example in main.py):
* define model_function and give starting values in as List (must not be very accurate)
* you may define start and end value for the fit (this only effects plot of the fit function)
* the function returns the fit parameters and their errors (extract by print)
"""""


def plot_file(file_path, title=None, split_sign=";", x_name="", y_name="", x_column=0, y_column=1, x_scale=1,
              y_scale=1, model_function="", p0=None, fit_start=None, fit_end=None, y_log=False, x_log=False):

    plt.ion()
    fig, ax = plt.subplots()

    errors = None
    x_list, y_list = extract_data(file_path, split_sign, x_column, y_column)
    x_data = np.array(x_list)
    y_data = np.array(y_list)

    try:
        x_data = x_data * float(x_scale)
    except Exception:
        x_f, _ = read_expression(x_scale)
        if isinstance(x_f, types.FunctionType):
            x_data = x_f(x_data)
        else:
            raise ValueError("no valid function")

    try:
        y_data = y_data * float(y_scale)
    except Exception:
        y_f, _ = read_expression(y_scale)
        if isinstance(y_scale, types.FunctionType):
            y_data = y_f(y_data)
        else:
            raise ValueError("no valid function")

    if model_function != "":
        x_fit, y_fit = get_fit_arrays(fit_end, fit_start, x_data, y_data)
        f, para_list = read_expression(model_function)
        opt_paras, error_matrix = curve_fit(f, x_fit, y_fit, p0=p0)[:2]
        errors = np.sqrt(np.diag(error_matrix))
        x_model = np.linspace(np.min(x_fit), np.max(x_fit), 100)
        y_model = f(x_model, *opt_paras)
        text = "f(x) = " + make_pretty_expr(model_function) + "\n"
        for i in range(len(opt_paras)):
            text += f"{para_list[i]} = {opt_paras[i]:.3}; "
        ax.plot(x_data, y_data, color='black', linestyle="", marker='o', markersize=1)
        ax.plot(x_model, y_model, color='r', label=text)
    else:
        ax.plot(x_data, y_data, color='black', marker='o', markersize=1)

    ax.set_title(title)
    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)

    if y_log:
        ax.set_yscale('log')
    if x_log:
        ax.set_xscale('log')
    if model_function != "":
        ax.legend(loc='best')
    ax.grid(True)
    plt.show(block=False)
    if errors is not None:
        return errors


def get_fit_arrays(fit_end, fit_start, x_data, y_data):
    mask = np.ones_like(x_data, dtype=bool)
    if fit_start is not None:
        mask = (x_data >= fit_start)
    if fit_end is not None:
        mask = (x_data <= fit_end) & mask
    x_fit = x_data[mask]
    y_fit = y_data[mask]
    return x_fit, y_fit


def extract_data(file_path, split_sign, x_column, y_column):
    x_list = []
    y_list = []
    with open(file_path, 'r') as file:
        for line in file:
            data_line = line.strip().split(split_sign)
            x_value = float(data_line[x_column])
            y_value = float(data_line[y_column])
            x_list.append(x_value)
            y_list.append(y_value)
    return x_list, y_list
