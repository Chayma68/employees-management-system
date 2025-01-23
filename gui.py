import customtkinter as ctk
from tkinter import messagebox, ttk
import backend

#main window
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Employee Management System")
root.geometry("900x600")

#Frame Layouts

top_frame = ctk.CTkFrame(root, fg_color="#3262a8", height=80)  #for the header
top_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

middle_frame = ctk.CTkFrame(root, fg_color="white")
middle_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

bottom_frame = ctk.CTkFrame(root, fg_color="white")
bottom_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=2)
root.grid_columnconfigure(0, weight=1)

#Header
title_label = ctk.CTkLabel(top_frame, text="Employee Management System", font=("Arial", 18, "bold"), text_color="White",
                           )
title_label.pack(pady=20)

#Search Bar
search_label = ctk.CTkLabel(middle_frame, text="Search Employee By Name:", font=("Arial", 12))
search_label.grid(row=0, column=0, padx=5, pady=5)
search_Entry = ctk.CTkEntry(middle_frame, font=("Arial", 12), width=200)
search_Entry.grid(row=0, column=1, padx=5, pady=5)

#TreeView
columns = ("ID", "Name", "Department", "Salary", "Hire Date")
tree = ttk.Treeview(bottom_frame, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.grid(row=0, column=0, sticky="nsew")
bottom_frame.grid_rowconfigure(0, weight=1)
bottom_frame.grid_columnconfigure(0, weight=1)


def update_table(data=None):
    for row in tree.get_children():
        tree.delete(row)
    employees = data if data else backend.get_employees()
    for emp in employees:
        tree.insert("", "end", values=(emp[0], emp[1], emp[2], emp[3], emp[4]))


def search_employee():
    query = search_Entry.get()
    result = backend.search_employee(query)
    update_table(result)


search_button = ctk.CTkButton(middle_frame, text="Search", command=search_employee, corner_radius=32)
search_button.grid(row=0, column=2, padx=5, pady=5)

fields = [("Name:", "name"), ("Department:", "department"), ("Salary:", "salary"), ("Hire Date:", "hire_date")]
entries = {}

for i, (label_text, var_name) in enumerate(fields):
    ctk.CTkLabel(middle_frame, text=label_text).grid(row=i + 1, column=0, sticky="w", padx=10, pady=5)
    entry = ctk.CTkEntry(middle_frame)
    entry.grid(row=i + 1, column=1, padx=10, pady=5, sticky="ew")
    entries[var_name] = entry


def add_employee():
    name = entries["name"].get()
    department = entries["department"].get()
    salary = entries["salary"].get()
    hire_date = entries["hire_date"].get()

    if not name or not department or not salary or not hire_date:
        messagebox.showerror("Error", "All fields are required!")
        return
    try:
        salary = float(salary)
        backend.add_employee(name, department, salary, hire_date)
        update_table()
        messagebox.showinfo("Success", "Employee added successfully!")
    except ValueError:
        messagebox.showerror("Error", "Invalid salary format")


def edit_employee():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("ERROR", "Please Select an employee to edit!")
        return
    emp_id = tree.item(selected_item, "values")[0]
    name = entries["name"].get()
    department = entries["department"].get()
    salary = entries["salary"].get()
    hire_date = entries["hire_date"].get()
    try:
        salary = float(salary)
        backend.edit_employee(emp_id, name, department, salary, hire_date)
        update_table()
        messagebox.showinfo("Success", "Employee updated successfully!")
    except ValueError:
        messagebox.showerror("ERROR", "Invalid salary format")


def delete_employee():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please selected an employee to delete")
        return

    emp_id = tree.item(selected_item, "values")[0]
    backend.delete_employee(emp_id)
    update_table()
    messagebox.showinfo("Success", "Employee deleted successfully!")


button_frame = ctk.CTkFrame(bottom_frame, fg_color="white")
button_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=10)

button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)

ctk.CTkButton(button_frame, text="Add Employee", command=add_employee, width=150).grid(row=0, column=0, padx=10, pady=5, sticky="ew")
ctk.CTkButton(button_frame, text="Edit Employee", command=edit_employee, width=150).grid(row=0, column=1, padx=10,
                                                                                        pady=5, sticky="ew")
ctk.CTkButton(button_frame, text="Delete Employee", command=delete_employee, width=150).grid(row=0, column=2, padx=10,
                                                                                            pady=5, sticky="ew")

update_table()
root.mainloop()
