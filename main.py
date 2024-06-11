from modules.PlotTxtFile import plot_file, np


# Tip: plot_file(saved_file_name, y_name="", x_name="", model_function=None,
#                           p0=None, fit_start=None, fit_end=None, split_str=";")
# -> popt, error (parameters of fit function, and their error)
# p = parameter (of fit function)


# ---------------------------

# Configuration
file_name = "Spectroscopy"
title = None
y_name = "Amplitude in mV"
x_name = "height difference in nm"

split_sign = ";"
x_column = 0
y_column = 1
x_scale = 1e9
y_scale = 1e3
x_log = False
y_log = False


# Configure fit (comment if not needed)
def model_function(x, A, B):
    return A * x + B


# StartValues
A_0 = -5
B_0 = 0
p0 = [A_0, B_0]
p_str = "A, B"

fit_start = 6.78e2
fit_end = None

# ---------------------------


if "model_function" not in locals():
    model_function = None

if "p0" not in locals():
    p0 = None

opt_paras, errors = plot_file(file_name, title=title, split_sign=split_sign, x_name=x_name, y_name=y_name, x_log=x_log,
                              y_log=y_log, x_column=x_column, y_column=y_column, x_scale=x_scale, y_scale=y_scale,
                              model_function=model_function, p0=p0, fit_start=fit_start, fit_end=fit_end)

if opt_paras is not None and errors is not None:
    print(f"Optimal parameters {p_str}: {popt}, error: {error}")
