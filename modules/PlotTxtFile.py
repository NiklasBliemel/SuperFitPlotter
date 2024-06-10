import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

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


def plot_file(saved_file_name, title=None, split_sign=";", y_name="y", x_name="x", x_column=0, y_column=1,
              x_scale=1.0, y_scale=1.0,
              model_function=None, p0=None, fit_start=None, fit_end=None, y_log=False, x_log=False):
    error = None
    popt = None
    plot_data = "modules/TxtFiles/" + saved_file_name + ".txt"
    x_list = []
    y_list = []
    with open(plot_data, 'r') as file:
        for line in file:
            data_line = line.strip().split(split_sign)
            x_value = float(data_line[x_column]) * x_scale
            y_value = float(data_line[y_column]) * y_scale
            x_list.append(x_value)
            y_list.append(y_value)

    x_data = np.array(x_list)
    y_data = np.array(y_list)

    mask = np.ones_like(x_data, dtype=bool)

    if fit_start is not None:
        mask = (x_data >= fit_start)
    if fit_end is not None:
        mask = (x_data <= fit_end) & mask

    x_fit = x_data[mask]
    y_fit = y_data[mask]

    if model_function is not None:
        popt, pcov = curve_fit(model_function, x_fit, y_fit, p0=p0)[:2]
        error = np.sqrt(np.diag(pcov))

        x_model = np.linspace(np.min(x_fit), np.max(x_fit), 100)
        y_model = model_function(x_model, *popt)

        plt.plot(x_data, y_data, color='black', label=saved_file_name + " data", linestyle="", marker='o', markersize=1)
        plt.plot(x_model, y_model, color='r', label="fit plot")

    else:
        plt.plot(x_data, y_data, color='black', label=saved_file_name + " data", marker='o', markersize=1)

    if title is not None:
        plt.title(title)
    else:
        plt.title(saved_file_name)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    if y_log:
        plt.yscale('log')
    if x_log:
        plt.xscale('log')
    plt.grid(True)
    plt.legend(loc='best')
    plt.show()

    if model_function is not None:
        return popt, error
