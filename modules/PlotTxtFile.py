import types
import matplotlib.pyplot as plt
import numpy as np
import warnings
from scipy.optimize import curve_fit, OptimizeWarning
from modules.ExtractFunction import extract_x_function, extract_any_function, make_pretty_expr
from mplcursors import cursor


def plot_file(file_path, title=None, split_sign=";", x_name="", y_name="", x_expr="C1", y_expr="C2", skip_line=0,
              model_function="", p0=None, fit_start=None, fit_end=None, y_log=False, x_log=False):
    if split_sign == "\\t":
        split_sign = "\t"
    fig, ax = plt.subplots()
    ax.set_title(title, fontsize=16, pad=15)
    ax.set_xlabel(x_name, fontsize=10, labelpad=8)
    ax.set_ylabel(y_name, fontsize=10, labelpad=8)
    if y_log:
        ax.set_yscale('log')
    if x_log:
        ax.set_xscale('log')
    ax.grid(True)

    data = extract_data(file_path, split_sign, skip_line)
    x_data, y_data = modify_data(x_expr, y_expr, data)
    ax.plot(x_data, y_data, color='black', linestyle="", marker='o', markersize=1)
    if model_function != "":
        x_fit, y_fit = get_fit_arrays(fit_end, fit_start, x_data, y_data)
        f, para_list = extract_x_function(model_function)
        error_text = "errors: "
        try:
            # Filter to catch OptimizeWarning
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always", OptimizeWarning)  # Always trigger OptimizeWarning
                opt_paras, error_matrix = curve_fit(f, x_fit, y_fit, p0=p0)[:2]
                if any(issubclass(warn.category, OptimizeWarning) for warn in w):
                    raise OptimizeWarning("OptimizeWarning triggered")
                errors = np.sqrt(np.diag(error_matrix))
                for i in range(len(errors)):
                    error_text += r"$\Delta$" + f"{para_list[i]}={errors[i]:.3}; "
        except OptimizeWarning or RuntimeWarning:
            opt_paras = p0
            error_text = "fit failed"
        except Exception as e:
            opt_paras = p0
            error_text = e
        x_model = np.linspace(np.min(x_fit), np.max(x_fit), 100)
        y_model = f(x_model, *opt_paras)
        legend_text = "f(x) = " + make_pretty_expr(model_function)
        ax.plot(x_model, y_model, color='r', label=legend_text)
        opt_para_text = "parameter: "
        for i in range(len(opt_paras)):
            opt_para_text += f"{para_list[i]} = {opt_paras[i]:.3}; "
        opt_para_text = opt_para_text[:-2] + " / " + error_text[:-2]
        ax.text(
            1, 1.01,
            opt_para_text,
            transform=ax.transAxes,
            fontsize=8,
            color='black',
            horizontalalignment='right',
        )
        ax.legend(loc='best', draggable=True)

    cr = cursor(multiple=True)

    @cr.connect("add")
    def on_add(sel):
        sel.annotation.get_bbox_patch().set(fc="lightgrey", alpha=0.5)
        sel.annotation.set_text(f'[{sel.target[0]:.3}, {sel.target[1]:.3}]')

    plt.show()


def get_fit_arrays(fit_end, fit_start, x_data, y_data):
    mask = np.ones_like(x_data, dtype=bool)
    if fit_start is not None:
        mask = (x_data >= fit_start)
    if fit_end is not None:
        mask = (x_data <= fit_end) & mask
    x_fit = x_data[mask]
    y_fit = y_data[mask]
    return x_fit, y_fit


def extract_data(file_path, split_sign, skip_line):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.replace(',', '.')
            data_line = line.strip().split(split_sign)
            data.append(data_line)
    float_data = [[float(item) for item in line] for line in data[skip_line:]]
    return np.array(float_data)


def modify_data(x_expr, y_expr, data):
    x_f, x_para = extract_any_function(x_expr)
    for i in range(len(x_para)):
        if x_para[i][0] == "C" and len(x_para[i]) == 2:
            column = int(x_para[i][1]) - 1
            if 0 <= column <= len(data[-1]):
                x_para[i] = data[:, column]
            else:
                raise ValueError("column indices out of range")
        else:
            raise ValueError("parameters have to be named C1, C2, ...")
    x_data = x_f(*x_para)
    y_f, y_para = extract_any_function(y_expr)
    for i in range(len(y_para)):
        if y_para[i][0] == "C" and len(y_para[i]) == 2:
            column = int(y_para[i][1]) - 1
            if 0 <= column <= len(data[-1]):
                y_para[i] = data[:, column]
            else:
                raise ValueError("column indices out of range")
        else:
            raise ValueError("parameters have to be named C1, C2, ...")
    y_data = y_f(*y_para)
    return x_data, y_data
