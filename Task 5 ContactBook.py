import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

FILE = "contacts.json"

def load():
    if os.path.exists(FILE):
        f = open(FILE, "r")
        data = json.load(f)
        f.close()
        return data
    return {}

def save():
    f = open(FILE, "w")
    json.dump(all_contacts, f)
    f.close()

all_contacts = load()

def show_contacts():
    for i in tree.get_children():
        tree.delete(i)

    text = search_box.get().lower()

    for key in all_contacts:
        c = all_contacts[key]
        if text != "":
            if text not in c["name"].lower() and text not in c["phone"]:
                continue
        tree.insert("", "end", iid=key, values=(c["name"], c["phone"], c["email"], c["address"]))

    n = len(all_contacts)
    lbl_count.config(text=str(n) + " contacts")

def get_selected():
    sel = tree.selection()
    if len(sel) > 0:
        return sel[0]
    return None

def add_contact():
    show_form("Add", None, None)

def edit_contact():
    key = get_selected()
    if key == None:
        messagebox.showinfo("Oops", "Please select a contact first!")
        return
    show_form("Edit", all_contacts[key], key)

def delete_contact():
    key = get_selected()
    if key == None:
        messagebox.showinfo("Oops", "Please select a contact first!")
        return

    name = all_contacts[key]["name"]
    ans = messagebox.askyesno("Delete?", "Delete " + name + "?")
    if ans == True:
        del all_contacts[key]
        save()
        show_contacts()

def show_form(mode, existing, old_key):
    win = tk.Toplevel(window)
    win.title(mode + " Contact")
    win.geometry("350x280")
    win.grab_set()

    tk.Label(win, text=mode + " Contact", font=("Arial", 13, "bold")).pack(pady=10)

    frm = tk.Frame(win)
    frm.pack()

    tk.Label(frm, text="Name:").grid(row=0, column=0, sticky="w", pady=4, padx=10)
    e_name = tk.Entry(frm, width=25)
    e_name.grid(row=0, column=1)

    tk.Label(frm, text="Phone:").grid(row=1, column=0, sticky="w", pady=4, padx=10)
    e_phone = tk.Entry(frm, width=25)
    e_phone.grid(row=1, column=1)

    tk.Label(frm, text="Email:").grid(row=2, column=0, sticky="w", pady=4, padx=10)
    e_email = tk.Entry(frm, width=25)
    e_email.grid(row=2, column=1)

    tk.Label(frm, text="Address:").grid(row=3, column=0, sticky="w", pady=4, padx=10)
    e_address = tk.Entry(frm, width=25)
    e_address.grid(row=3, column=1)

    if existing != None:
        e_name.insert(0, existing["name"])
        e_phone.insert(0, existing["phone"])
        e_email.insert(0, existing["email"])
        e_address.insert(0, existing["address"])

    err = tk.Label(win, text="", fg="red")
    err.pack()

    def save_contact():
        name = e_name.get().strip()
        phone = e_phone.get().strip()
        email = e_email.get().strip()
        address = e_address.get().strip()

        if name == "":
            err.config(text="Name cannot be empty!")
            return

        key = name.lower()

        if mode == "Add":
            if key in all_contacts:
                err.config(text="Contact already exists!")
                return

        if mode == "Edit":
            if key != old_key and key in all_contacts:
                err.config(text="Name already taken!")
                return
            del all_contacts[old_key]

        all_contacts[key] = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        }

        save()
        show_contacts()
        win.destroy()

    tk.Button(win, text="Save", command=save_contact, bg="green", fg="white").pack(side="left", padx=40, pady=8)
    tk.Button(win, text="Cancel", command=win.destroy).pack(side="left", pady=8)

window = tk.Tk()
window.title("My Contact Book")
window.geometry("750x450")

tk.Label(window, text="My Contact Book", font=("Arial", 16, "bold")).pack(pady=10)

search_frame = tk.Frame(window)
search_frame.pack()
tk.Label(search_frame, text="Search: ").pack(side="left")
search_box = tk.Entry(search_frame, width=30)
search_box.pack(side="left")
search_box.bind("<KeyRelease>", lambda e: show_contacts())

btn_frame = tk.Frame(window)
btn_frame.pack(pady=8)
tk.Button(btn_frame, text="Add", command=add_contact, bg="blue", fg="white", width=10).pack(side="left", padx=5)
tk.Button(btn_frame, text="Edit", command=edit_contact, bg="orange", fg="white", width=10).pack(side="left", padx=5)
tk.Button(btn_frame, text="Delete", command=delete_contact, bg="red", fg="white", width=10).pack(side="left", padx=5)

lbl_count = tk.Label(window, text="")
lbl_count.pack()

cols = ("Name", "Phone", "Email", "Address")
tree = ttk.Treeview(window, columns=cols, show="headings")
tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.heading("Email", text="Email")
tree.heading("Address", text="Address")
tree.column("Name", width=160)
tree.column("Phone", width=120)
tree.column("Email", width=190)
tree.column("Address", width=200)
tree.pack(fill="both", expand=True, padx=15, pady=10)

tree.bind("<Double-1>", lambda e: edit_contact())

show_contacts()
window.mainloop()