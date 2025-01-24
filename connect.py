import os
import sys
from tkinter import messagebox
from PIL import Image
import customtkinter as ctk
import subprocess

import backend

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("light")
root = ctk.CTk()
root.geometry("800x500")
root.title("Connect - Employee Management System")

theme_mode = ctk.get_appearance_mode()
if theme_mode == "Dark":
    text_color = "white"
else:
    text_color = "black"

image_frame = ctk.CTkFrame(root)
image_frame.grid(row=0, column=0, sticky="nsew")

connect_frame = ctk.CTkFrame(root)
connect_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
root.resizable(False, False)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_rowconfigure(0, weight=1)

image_path = "images/management.jpg"
if os.path.exists(image_path):
    image = ctk.CTkImage(light_image=Image.open(image_path), size=(350, 500))
    image_label = ctk.CTkLabel(root, image=image, text="")
    image_label.grid(row=0, column=0, sticky="nsew")
else:
    image_label = ctk.CTkLabel(root, text="Image Not Found", font=("Arial", 16, "bold"))
    image_label.grid(row=0, column=0, sticky="nsew")

title_label = ctk.CTkLabel(connect_frame, text="Connect To Your Account", font=("Arial", 20, "bold"))
title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)


def connect():
    email = email_entry.get()
    password = password_entry.get()
    role = backend.user_role_byemail(email)
    user = backend.search_user_email(email)

    if user:  # Ensure user exists
        stored_password = backend.user_password(email)

        if stored_password and password == stored_password and role == "admin":
            subprocess.Popen([sys.executable, "gui.py"])
            root.destroy()
        else:
            messagebox.showerror("ERROR", "Wrong password")
    else:
        messagebox.showerror("ERROR", "No user with such email!")


def register():
    subprocess.Popen([sys.executable, "register.py"])


#Fields

email_label = ctk.CTkLabel(connect_frame, text="Email:", font=("Arial", 16))
email_label.grid(row=1, column=0, sticky="w", padx=20, pady=10)
email_entry = ctk.CTkEntry(connect_frame, width=250, placeholder_text="example@gmail.com", corner_radius=10)
email_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

password_label = ctk.CTkLabel(connect_frame, text="Password:", font=("Arial", 16))
password_label.grid(row=2, column=0, sticky="w", padx=20, pady=10)
password_entry = ctk.CTkEntry(connect_frame, show="*", width=250, placeholder_text="*******", corner_radius=10)
password_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

connect_button = ctk.CTkButton(connect_frame, text="Connect", font=("Arial", 16, "bold"), command=connect)
connect_button.grid(row=3, column=1, padx=20, pady=20)

register_button = ctk.CTkButton(connect_frame, text="Create Account", font=("Arial", 12), command=register,
                                fg_color="transparent", text_color=text_color)
register_button.grid(row=4, column=1, padx=20)

root.mainloop()
