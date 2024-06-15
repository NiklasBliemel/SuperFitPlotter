import types
import matplotlib.pyplot as plt
import numpy as np
import warnings
from scipy.optimize import curve_fit, OptimizeWarning
from modules.ExtractFunction import read_expression, make_pretty_expr
from mplcursors import cursor


def plot_file(file_path, title=None, split_sign=";", x_name="", y_name="", x_column=0, y_column=1, x_scale=1,
              y_scale=1, model_function="", p0=None, fit_start=None, fit_end=None, y_log=False, x_log=False):
    fig, ax = plt.subplots()
    ax.set_title(title, fontsize=16, pad=15)
    ax.set_xlabel(x_name, fontsize=10, labelpad=8)
    ax.set_ylabel(y_name, fontsize=10, labelpad=8)
    if y_log:
        ax.set_yscale('log')
    if x_log:
        ax.set_xscale('log')
    ax.grid(True)
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
        ax.plot(x_data, y_data, color='black', linestyle="", marker='o', markersize=1)
        ax.plot(x_model, y_model, color='r', label=legend_text)
        opt_para_text = "parameter: "
        for i in range(len(opt_paras)):
            opt_para_text += f"{para_list[i]} = {opt_paras[i]:.3}; "
        opt_para_text = opt_para_text[:-2] + "\n" + error_text[:-2]
        ax.text(
            1.02, 0.5,
            opt_para_text,
            transform=ax.transAxes,
            fontsize=10,
            color='black',
            horizontalalignment='left',
            verticalalignment='center',
            rotation=90
        )

        ax.legend(loc='best', draggable=True)
    else:
        ax.plot(x_data, y_data, color='black', marker='o', markersize=1)

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
