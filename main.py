import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from parsers.html_parser import HtmlParser
from client.smart_test_client import SmartTestsClient
from constants.constants import SUPPORTED_GROUPS
from models.data_manager import DataManager

# Global
data_manager = DataManager()
smart_test_client = SmartTestsClient()


def load_build_report():
    global data_manager
    file_name = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
    if not file_name:
        messagebox.showerror("Error", "Failed to load build report.")
    else:
        try:
            with open(file_name, "r") as f:
                html = f.read()
            html_parser = HtmlParser(html)
            html_parser.load_html(data_manager.get_services_map())
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to load build report. error: {ex}")
        else:
            messagebox.showinfo("Success", "Build Report Loaded Successfully")
            button_load_tests.config(state="normal")
            progress_bar['value'] = 0
            progress_label.config(text=f"Tests: {progress_bar['value']}/{progress_bar['maximum']}")
            button_create_testng.config(state="disabled")


def pick_group(group):
    global data_manager, smart_test_client
    try:
        if data_manager.curr_group != group:
            data_manager.test_names_by_group.clear()

        filter_list = data_manager.filter_by_group[group]
        res = smart_test_client.get_all_flows_by_filter(filter_list)
        data_manager.set_curr_group(group_name=group)
        progress_bar['value'] = 0
        progress_bar['maximum'] = res['total_count']
        total_label.config(text=f"Total Flows: {res['total_count']}")
        progress_label.config(text=f"Tests: 0/{res['total_count']} (0%)")
        button_create_testng.config(state="disabled")
    except Exception as ex:
        messagebox.showerror("Error", f"Failed with error: {ex}")
        value_inside_picker.set("Select Group")
        total_label.config(text="Total Flows: 0")
        progress_label.config(text=f"Tests: 0/0")
        progress_bar['value'] = 0
        progress_bar['maximum'] = 0
        button_load_tests.config(state="disabled")
        button_create_testng.config(state="disabled")


def analyze_tests_by_group():
    global data_manager
    try:
        smart_test_client.analyze_flows(data_manager.get_services_map(),
                                        data_manager.get_filter_for_curr_group(),
                                        data_manager.test_names_by_group)
    except Exception as ex:
        messagebox.showerror("Error", f"Failed to create xml. Error: {ex}")
    else:
        button_create_testng.config(state="normal")
        progress_bar['value'] = data_manager.get_tests_total_count()
        percentage = '{:.2%}'.format(float(progress_bar['value'])/float(progress_bar['maximum']))
        progress_label.config(text=f"Tests: {progress_bar['value']}/{progress_bar['maximum']} ({percentage})")
        messagebox.showinfo("Success", "Analyzed Data Successfully")


def create_testng_xml():
    global data_manager
    flows_by_group = data_manager.test_names_by_group
    curr_group_filter = value_inside_picker.get()
    if flows_by_group is not None and len(flows_by_group) > 0:
        for group_name in flows_by_group:
            try:
                smart_test_client.create_testng_xml(flows_by_group[group_name], group_name, curr_group_filter)
            except Exception as ex:
                print(f"Failed to create xml for: {group_name}. Error: {ex}")

        messagebox.showinfo("Success", "TestNG Created successfully")
    else:
        messagebox.showerror("Error", "Failed to create xml")


window = tk.Tk()
window.title("Smart Tests Client")
window.minsize(width=400, height=300)
window.config(width=400, height=300)

button_load_html = tk.Button(window, text="Load Build Report", command=load_build_report, width=30)
button_load_html.pack(padx=10, pady=10)

row = tk.Frame(window)
row.pack()

pick_label = tk.Label(row, text="Pick a Group: ")
pick_label.pack(side=tk.LEFT)

value_inside_picker = tk.StringVar(window)
value_inside_picker.set("Select Group")
pick_picker = tk.OptionMenu(row, value_inside_picker, *SUPPORTED_GROUPS, command=pick_group)
pick_picker.pack(side=tk.LEFT)

total_label = tk.Label(row, text="Total Flows: 0")
total_label.pack(side=tk.LEFT)

button_load_tests = tk.Button(window, text="Analyze Tests To Run", command=analyze_tests_by_group, width=30)
button_load_tests.config(state="disabled")
button_load_tests.pack(padx=10, pady=10)

s = ttk.Style()
s.theme_use('clam')
s.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
progress_bar = ttk.Progressbar(window,
                               orient='horizontal',
                               mode='determinate',
                               length=280,
                               style="green.Horizontal.TProgressbar")
progress_bar['maximum'] = 0
progress_bar.pack(padx=10, pady=10)

progress_label = tk.Label(window, text="Tests: 0/0")
progress_label.pack(padx=10, pady=10)

button_create_testng = tk.Button(window, text="Create TestNG", command=create_testng_xml, width=30)
button_create_testng.config(state="disabled")
button_create_testng.pack(padx=10, pady=10)

window.mainloop()
