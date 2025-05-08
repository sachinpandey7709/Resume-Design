import tkinter as tk
from tkinter import messagebox
import pyperclip
import json
import os

DATA_FILE = "data.json"

# ------------------------- Load Existing Data -------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# ------------------------- Functions -------------------------
def add_password():
    website = website_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if website and username and password:
        data.append({"website": website, "username": username, "password": password})
        save_data()
        website_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        refresh_tree()
    else:
        messagebox.showwarning("Missing Info", "All fields are required.")

def delete_password(index):
    del data[index]
    save_data()
    refresh_tree()

def copy_to_clipboard(value):
    pyperclip.copy(value)
    messagebox.showinfo("Copied", f"'{value}' copied to clipboard.")

def refresh_tree():
    for widget in tree_frame.winfo_children():
        widget.destroy()

    if not data:
        tk.Label(tree_frame, text="No Data To Show", font=("Arial", 12)).pack()
        return

    headers = ["Website", "Username", "Password", "Delete"]
    for col, text in enumerate(headers):
        tk.Label(tree_frame, text=text, font=("Arial", 12, "bold"), borderwidth=1, relief="solid", width=20, pady=5).grid(row=0, column=col)

    for i, entry in enumerate(data):
        tk.Label(tree_frame, text=entry["website"], borderwidth=1, relief="solid", width=20).grid(row=i+1, column=0, sticky="w")
        tk.Button(tree_frame, text="Copy", command=lambda t=entry["website"]: copy_to_clipboard(t)).grid(row=i+1, column=0, sticky="e")

        tk.Label(tree_frame, text=entry["username"], borderwidth=1, relief="solid", width=20).grid(row=i+1, column=1, sticky="w")
        tk.Button(tree_frame, text="Copy", command=lambda t=entry["username"]: copy_to_clipboard(t)).grid(row=i+1, column=1, sticky="e")

        tk.Label(tree_frame, text="*" * len(entry["password"]), borderwidth=1, relief="solid", width=20).grid(row=i+1, column=2, sticky="w")
        tk.Button(tree_frame, text="Copy", command=lambda t=entry["password"]: copy_to_clipboard(t)).grid(row=i+1, column=2, sticky="e")

        def make_delete_func(index):
            return lambda: delete_password(index)

        tk.Button(tree_frame, text="Delete", command=make_delete_func(i), bg="black", fg="white", padx=10, pady=2).grid(row=i+1, column=3)

# ------------------------- GUI Layout -------------------------
data = load_data()

root = tk.Tk()
root.title("PassX - Password Manager")
root.geometry("800x600")
root.configure(bg="white")

# -------------------- Header --------------------
header_frame = tk.Frame(root, bg="black", height=60)
header_frame.pack(fill=tk.X)

tk.Label(header_frame, text="PassX", bg="black", fg="white", font=("Arial", 20, "bold")).pack(side=tk.LEFT, padx=20)

menu_frame = tk.Frame(header_frame, bg="black")
menu_frame.pack(side=tk.RIGHT, padx=20)

for item in ["Home", "About", "Contact"]:
    tk.Label(menu_frame, text=item, bg="black", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=15)

# -------------------- Title & Info --------------------
tk.Label(root, text="Password Manager", font=("Arial", 20, "bold"), bg="white").pack(pady=20)
tk.Label(root, text="We're thrilled to have you here. Your digital life contains a myriad of passwords,\nand we know how challenging it can be to manage them all.\nThat's why we're here to make it easy for you.",
         font=("Arial", 12), bg="white", justify="center").pack(pady=10)

# -------------------- Tree / Table --------------------
tree_frame = tk.Frame(root, bg="white")
tree_frame.pack(pady=20)
refresh_tree()

# -------------------- Form --------------------
form_frame = tk.Frame(root, bg="white")
form_frame.pack(pady=20)

tk.Label(form_frame, text="Add a Password", font=("Arial", 16, "bold"), bg="white").grid(row=0, columnspan=2, pady=10)

tk.Label(form_frame, text="Website:", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="e", pady=5)
website_entry = tk.Entry(form_frame, width=30)
website_entry.grid(row=1, column=1, pady=5)

tk.Label(form_frame, text="Username:", font=("Arial", 12), bg="white").grid(row=2, column=0, sticky="e", pady=5)
username_entry = tk.Entry(form_frame, width=30)
username_entry.grid(row=2, column=1, pady=5)

tk.Label(form_frame, text="Password:", font=("Arial", 12), bg="white").grid(row=3, column=0, sticky="e", pady=5)
password_entry = tk.Entry(form_frame, show="*", width=30)
password_entry.grid(row=3, column=1, pady=5)

submit_btn = tk.Button(form_frame, text="Submit", command=add_password, bg="black", fg="white", padx=15, pady=5)
submit_btn.grid(row=4, columnspan=2, pady=10)

root.mainloop()
