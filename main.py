from modules.PlotTxtFile import plot_file, np


# Tip: plot_file(saved_file_name, y_name="", x_name="", model_function=None,
#                           p0=None, fit_start=None, fit_end=None, split_str=";")
# -> popt, error (parameters of fit function, and their error)
# p = parameter (of fit function)


# ---------------------------
def model_function(x, A, B):
    return A * x + B


p_str = "A, B"

# StartValues
A_0 = -5e6
B_0 = 0
p0 = [A_0, B_0]

# Configuration
file_name = "FrequencySweep"
y_name = "Amplitude in mV"
x_name = "height difference in m"

split_sign = ";"
x_column = 0
y_column = 1

fit_start = 6.78e-7
fit_end = None
x_log = False
y_log = False
# ---------------------------


popt, error = plot_file(file_name, split_sign=split_sign, y_name=y_name, x_name=x_name, x_log=x_log, y_log=y_log,
                        x_column=x_column, y_column=y_column,
                        model_function=model_function, p0=p0, fit_start=fit_start, fit_end=fit_end)
print(f"Optimal parameters {p_str}: {popt}, error: {error}")
