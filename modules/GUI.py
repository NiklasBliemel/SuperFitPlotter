from tkinter import filedialog
import customtkinter as ctk

from modules.PlotTxtFile import plot_file
from modules.ExtractFunction import read_expression

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("fit plot")
root.geometry("730x630")


def select_file():
    filename = filedialog.askopenfilename()
    if filename.endswith(".txt"):
        file_label.configure(text=filename, bg_color=default_label_bg)
        x_column_entry.configure(placeholder_text="x column (0 default)", state="normal")
        y_column_entry.configure(placeholder_text="y column (1 default)", state="normal")
        x_scale_entry.configure(placeholder_text="x scale / function", state="normal")
        y_scale_entry.configure(placeholder_text="y scale / function", state="normal")
        x_log_switch.configure(state="normal")
        y_log_switch.configure(state="normal")
        if fit_switch_var.get() == "off" or fit_function_var.get() != "":
            plot_button.configure(state="normal")
    else:
        file_label.configure(text="no .txt file", bg_color="red")
        x_column_entry.configure(state="disabled")
        y_column_entry.configure(state="disabled")
        x_scale_entry.configure(state="disabled")
        y_scale_entry.configure(state="disabled")
        x_log_switch.configure(state="disabled")
        y_log_switch.configure(state="disabled")
        plot_button.configure(state="disabled")


def plot():
    x_column = int(x_column_entry.get()) if x_column_entry.get() != "" else 0
    y_column = int(y_column_entry.get()) if y_column_entry.get() != "" else 1
    x_scale = x_scale_entry.get() if x_scale_entry.get() != "" else 1
    y_scale = y_scale_entry.get() if y_scale_entry.get() != "" else 1
    x_log = True if x_log_switch_var.get() == "on" else False
    y_log = True if y_log_switch_var.get() == "on" else False

    if fit_switch.get() == "off":
        try:
            plot_file(file_path=file_label.cget("text"), x_column=x_column, y_column=y_column,
                      title=plot_title.get(), x_name=x_axis.get(), y_name=y_axis.get(),
                      x_scale=x_scale, y_scale=y_scale, x_log=x_log, y_log=y_log)
            error_field.configure(text="")
        except Exception as e:
            error_field.configure(text=e)

    if fit_switch.get() == "on":
        fit_start = float(fit_start_entry.get()) if fit_start_entry.get() != "" else None
        fit_end = float(fit_end_entry.get()) if fit_end_entry.get() != "" else None
        try:
            errors = plot_file(file_path=file_label.cget("text"), x_column=x_column, y_column=y_column,
                                title=plot_title.get(), x_name=x_axis.get(), y_name=y_axis.get(),
                                model_function=fit_entry.get(), fit_start=fit_start,
                                fit_end=fit_end, p0=start_values_var.get(),
                                x_scale=x_scale, y_scale=y_scale, x_log=x_log, y_log=y_log)
            text = "errors: "
            for i in range(len(errors)):
                text += f"{para_list_var.get()[i]}_err = {errors[i]:.3}; "

            error_field.configure(text=text[:-2])
        except Exception as e:
            error_field.configure(text=e)


def toggle_switch():
    if fit_switch_var.get() == "on":
        plot_button.configure(state="disabled")
        fit_entry.configure(state="normal", placeholder_text="(a*x**2 + b*x + c)/sqrt(2*w*x))")
        confirm_fit_button.configure(state="normal")
        if fit_function_var.get() != "":
            plot_button.configure(state="normal")
            fit_start_entry.configure(state="normal")
            fit_end_entry.configure(state="normal")
            start_values_button.configure(state="normal")
    else:
        plot_button.configure(state="normal")
        fit_entry.configure(state="disabled")
        confirm_fit_button.configure(state="disabled")
        fit_start_entry.configure(state="disabled")
        fit_end_entry.configure(state="disabled")
        start_values_button.configure(state="disabled")
        start_values_label_2.configure(text="")


def confirm_fit():
    f, para_list = read_expression(fit_entry.get())
    fit_function_var.set(f)
    para_list_var.set(para_list)
    start_values_var.set([0.0 for _ in range(len(para_list))])
    if fit_function_var.get() != "":
        plot_button.configure(state="normal")
        fit_entry.configure(fg_color=default_entry_fg)
        fit_start_entry.configure(state="normal", placeholder_text="fit start")
        fit_end_entry.configure(state="normal", placeholder_text="fit end")
        start_values_button.configure(state="normal")
        text = ""
        for i in range(len(para_list_var.get())):
            text += para_list[i] + "_0=" + str(start_values_var.get()[i]) + "; "
        start_values_label_2.configure(text=text[:-2])
    else:
        fit_entry.configure(fg_color="yellow")


def set_start_values():
    text = ""
    for para in para_list_var.get():
        text += para + "_0/"

    try:
        start_values_input = ctk.CTkInputDialog(text=text[:-1]).get_input().split("/")
        new_start_values = [float(value) for value in start_values_input]
        start_values_var.set(new_start_values)
        text = ""
        for i in range(len(para_list_var.get())):
            text += f"{para_list_var.get()[i]}_0={start_values_var.get()[i]:.3}; "
        start_values_label_2.configure(text=text[:-2])
        start_values_button.configure(fg_color=default_button_color)
    except Exception:
        start_values_button.configure(fg_color="red")


def start_values_string():
    return None


master_frame = ctk.CTkFrame(master=root)
master_frame.grid(padx=20, pady=20)

# frame
data_config = ctk.CTkFrame(master=master_frame)
data_config.grid(row=0, column=0, padx=20, pady=20)
# button
select_file_button = ctk.CTkButton(master=data_config, text="select file", command=select_file)
select_file_button.grid(row=0, columnspan=3, padx=10, pady=12)
# file
file_label = ctk.CTkLabel(master=data_config, text="none", wraplength=500)
file_label.grid(row=1, columnspan=3, padx=10, pady=12)
# choose x and y columns
x_column_entry = ctk.CTkEntry(master=data_config, state="disabled")
x_column_entry.grid(row=2, column=0, padx=10, pady=12)
default_entry_fg = x_column_entry.cget("fg_color")
y_column_entry = ctk.CTkEntry(master=data_config, state="disabled")
y_column_entry.grid(row=2, column=1, padx=10, pady=12)
# x and y scales
x_scale_entry = ctk.CTkEntry(master=data_config, state="disabled")
x_scale_entry.grid(row=3, column=0, padx=10, pady=12)
y_scale_entry = ctk.CTkEntry(master=data_config, state="disabled")
y_scale_entry.grid(row=3, column=1, padx=10, pady=12)
# log switches
x_log_switch_var = ctk.StringVar(value="off")
x_log_switch = ctk.CTkSwitch(master=data_config, state="disabled", variable=x_log_switch_var, onvalue="on",
                             offvalue="off", text="log x axis")
x_log_switch.grid(row=2, column=2, padx=10, pady=12)
y_log_switch_var = ctk.StringVar(value="off")
y_log_switch = ctk.CTkSwitch(master=data_config, state="disabled", variable=y_log_switch_var, onvalue="on",
                             offvalue="off", text="log y axis")
y_log_switch.grid(row=3, column=2, padx=10, pady=12)

# frame
name_frame = ctk.CTkFrame(master=master_frame)
name_frame.grid(row=0, column=1, padx=20, pady=20)
# description
name_config_label = ctk.CTkLabel(master=name_frame, text="configure names:")
name_config_label.grid(row=0, padx=10, pady=12)
# entries
plot_title = ctk.CTkEntry(master=name_frame, placeholder_text="plot title")
plot_title.grid(row=1, padx=10, pady=12)
x_axis = ctk.CTkEntry(master=name_frame, placeholder_text="x - axis")
x_axis.grid(row=2, padx=10, pady=12)
y_axis = ctk.CTkEntry(master=name_frame, placeholder_text="y - axis")
y_axis.grid(row=3, padx=10, pady=12)

# frame
fit_frame = ctk.CTkFrame(master=master_frame)
fit_frame.grid(row=2, columnspan=2, padx=20, pady=20)
# switch
fit_switch_var = ctk.StringVar(value="off")
fit_switch = ctk.CTkSwitch(master=fit_frame, text="fit function: ", variable=fit_switch_var, onvalue="on",
                           offvalue="off",
                           command=toggle_switch)
fit_switch.grid(row=0, column=0, padx=10, pady=12)
# fit function definition
fit_entry = ctk.CTkEntry(master=fit_frame, state="disabled")
fit_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=12, sticky="ew")
# fit confirmation button
confirm_fit_button = ctk.CTkButton(master=fit_frame, text="confirm", command=confirm_fit, state="disabled")
confirm_fit_button.grid(row=0, column=3, padx=10, pady=12)
# fit config
fit_start_entry = ctk.CTkEntry(master=fit_frame, state="disabled")
fit_start_entry.grid(row=1, column=0, padx=10, pady=12)
fit_end_entry = ctk.CTkEntry(master=fit_frame, state="disabled")
fit_end_entry.grid(row=1, column=1, padx=10, pady=12)
start_values_label_1 = ctk.CTkLabel(master=fit_frame, text="start values:")
start_values_label_1.grid(row=1, column=2, padx=10, pady=12)
start_values_label_2 = ctk.CTkLabel(master=fit_frame, text="", text_color="grey")
start_values_label_2.grid(row=2, column=2, columnspan=2, padx=10, pady=12)
default_label_bg = start_values_label_2.cget("bg_color")
start_values_button = ctk.CTkButton(master=fit_frame, text="set start values", command=set_start_values,
                                    state="disabled")
start_values_button.grid(row=1, column=3, padx=10, pady=12)
default_button_color = start_values_button.cget("fg_color")
# variables
fit_function_var = ctk.Variable()
fit_function_var.set("")
start_values_var = ctk.Variable()
start_values_var.set([])
para_list_var = ctk.Variable()
para_list_var.set([])

start_frame = ctk.CTkFrame(master=master_frame)
start_frame.grid(row=3, columnspan=2, padx=20, pady=20)
plot_button = ctk.CTkButton(master=start_frame, text="generate Plot", command=plot, state="disabled")
plot_button.grid(row=0, padx=10, pady=12)
error_field = ctk.CTkLabel(master=start_frame, text="", text_color="red", wraplength=600)
error_field.grid(row=1, columnspan=3, padx=10, pady=12)


def run():
    root.mainloop()


run()
