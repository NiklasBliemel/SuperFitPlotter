from modules.PlotTxtFile import plot_file, np


# Tip: plot_file(saved_file_name, model_function=None, p0=None, fit_start=None, fit_end=None) -> popt, error
# p = parameter (of fit function)

# ---------------------------
def model_function(x, A, B):
    return A*x + B


p_str = "A, B"

# StartValues
A_0 = -5e6
B_0 = 0
p0 = [A_0, B_0]
# ---------------------------

popt, error = plot_file("Spectroscopy", model_function, p0, fit_start=6.78e-7)
print(f"Optimal parameters {p_str}: {popt}, error: {error}")
