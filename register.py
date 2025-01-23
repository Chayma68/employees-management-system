import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import sqlite3  # Database management

# Initialize the main window
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Register - Employee Management System")
root.geometry("800x500")

# Configure grid layout to have two columns
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_rowconfigure(0, weight=1)

# Load and display image using CTkImage for better scaling
image_path = "images/management.jpg"
if os.path.exists(image_path):
    image = ctk.CTkImage(light_image=Image.open(image_path), size=(350, 500))
    image_label = ctk.CTkLabel(root, image=image, text="")
    image_label.grid(row=0, column=0, sticky="nsew")
else:
    image_label = ctk.CTkLabel(root, text="Image Not Found", font=("Arial", 16, "bold"))
    image_label.grid(row=0, column=0, sticky="nsew")

# Frame for Registration Form
register_frame = ctk.CTkFrame(root)
register_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

# Title
title_label = ctk.CTkLabel(register_frame, text="Create an Account", font=("Arial", 20, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Username Field
username_label = ctk.CTkLabel(register_frame, text="Username", font=("Arial", 14))
username_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
username_entry = ctk.CTkEntry(register_frame, font=("Arial", 14), width=300)
username_entry.grid(row=1, column=1, padx=10, pady=10)

# Email Field
email_label = ctk.CTkLabel(register_frame, text="Email", font=("Arial", 14))
email_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)

email_entry = ctk.CTkEntry(register_frame, font=("Arial", 14), width=300)
email_entry.grid(row=2, column=1, padx=10, pady=10)

# Password Field
password_label = ctk.CTkLabel(register_frame, text="Password", font=("Arial", 14))
password_label.grid(row=3, column=0, sticky="w", padx=10, pady=10)
password_entry = ctk.CTkEntry(register_frame, show="*", font=("Arial", 14), width=300)
password_entry.grid(row=3, column=1, padx=10, pady=10)

# Confirm Password Field
confirm_password_label = ctk.CTkLabel(register_frame, text="Confirm Password", font=("Arial", 14))
confirm_password_label.grid(row=4, column=0, sticky="w", padx=10, pady=10)
confirm_password_entry = ctk.CTkEntry(register_frame, show="*", font=("Arial", 14), width=300)
confirm_password_entry.grid(row=4, column=1, padx=10, pady=10)

# Role Selection
role_label = ctk.CTkLabel(register_frame, text="Select Role", font=("Arial", 14))
role_label.grid(row=5, column=0, sticky="w", padx=10, pady=10)
role_var = ctk.StringVar(value="employee")
role_dropdown = ctk.CTkComboBox(register_frame, values=["admin", "employee"], variable=role_var)
role_dropdown.grid(row=5, column=1, padx=10, pady=10)

# Terms Agreement Checkbox
terms_var = ctk.BooleanVar()
terms_check = ctk.CTkCheckBox(register_frame, text="I agree to the Terms and Privacy Policy", variable=terms_var)
terms_check.grid(row=6, column=0, columnspan=2, pady=10)


# Register Button Function
def add_user(username, password, role):
    try:
        conn = sqlite3.connect("employees.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT CHECK (role IN ('admin', 'employee')) NOT NULL
            )
        ''')
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def register_user():
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    role = role_var.get()

    if not all([username, password, confirm_password]):
        messagebox.showerror("Error", "All fields are required!")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    if not terms_var.get():
        messagebox.showerror("Error", "You must agree to the Terms and Privacy Policy!")
        return

    if add_user(username, password, role):
        messagebox.showinfo("Success", "Account Created Successfully!")
        root.destroy()
    else:
        messagebox.showerror("Error", "Username already exists!")


# Register Button
register_button = ctk.CTkButton(register_frame, text="Create Account", font=("Arial", 16, "bold"),
                                command=register_user)
register_button.grid(row=7, column=0, columnspan=2, pady=20)

# Adjust grid weights for responsiveness
register_frame.grid_columnconfigure(1, weight=1)

# Run the application
root.mainloop()
