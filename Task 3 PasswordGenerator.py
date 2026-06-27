import tkinter as tk
import random
import string

window = tk.Tk()
window.title("Passify")
window.resizable(False, False)
window.configure(bg="white")

big_title  = ("Segoe UI", 22, "bold")
normal     = ("Segoe UI", 10)
small      = ("Segoe UI", 9)
password_font = ("Consolas", 13)   # monospace so letters are easy to read
button_font   = ("Segoe UI", 10)

white       = "white"
light_gray  = "#efefef"
dark        = "#111111"
gray_text   = "#888888"
divider_color = "#e8e8e8"

container = tk.Frame(window, bg=white, padx=30, pady=24)
container.pack()

tk.Label(container, text="Passify", font=big_title, bg=white, fg=dark).pack(anchor="w")
tk.Label(container, text="Generate a secure password instantly.",
         font=normal, bg=white, fg=gray_text).pack(anchor="w", pady=(2, 18))

length_row = tk.Frame(container, bg=white)
length_row.pack(fill="x", pady=(0, 4))

tk.Label(length_row, text="Length", font=normal, bg=white, fg=gray_text).pack(side="left")

length_input = tk.IntVar(value=16)   # default password length is 16

length_number = tk.Label(length_row, text="16", font=normal, bg=white, fg=dark, width=3)
length_number.pack(side="right")

def on_slider_move(value):
    length_number.config(text=str(int(float(value))))

tk.Scale(length_row, variable=length_input, from_=4, to=64,
         orient="horizontal", command=on_slider_move,
         bg=white, fg=dark, troughcolor=light_gray,
         highlightthickness=0, bd=0, showvalue=False,
         length=260, sliderlength=18).pack(side="right", padx=(0, 8))

tk.Frame(container, bg=divider_color, height=1).pack(fill="x", pady=8)

tk.Label(container, text="Include", font=normal, bg=white, fg=gray_text).pack(anchor="w", pady=(0, 6))

include_uppercase = tk.BooleanVar(value=True)
include_lowercase = tk.BooleanVar(value=True)
include_numbers   = tk.BooleanVar(value=True)
include_symbols   = tk.BooleanVar(value=False)

checkbox_options = [
    ("Uppercase  A – Z", include_uppercase),
    ("Lowercase  a – z", include_lowercase),
    ("Numbers    0 – 9", include_numbers),
    ("Symbols  ! @ # $", include_symbols),
]

for label_text, checkbox_var in checkbox_options:
    tk.Checkbutton(container, text=label_text, variable=checkbox_var,
                   font=normal, bg=white, fg=dark,
                   activebackground=white, selectcolor=white,
                   relief="flat", bd=0,
                   highlightthickness=0).pack(anchor="w", pady=1)

tk.Frame(container, bg=divider_color, height=1).pack(fill="x", pady=12)

tk.Label(container, text="Password", font=normal, bg=white, fg=gray_text).pack(anchor="w", pady=(0, 4))

result_box = tk.Frame(container, bg=light_gray, padx=12, pady=10)
result_box.pack(fill="x")

generated_password = tk.StringVar(value="")
tk.Label(result_box, textvariable=generated_password,
         font=password_font, bg=light_gray, fg=dark,
         anchor="w", width=28, wraplength=280, justify="left").pack(side="left")

status_message = tk.StringVar(value="")
tk.Label(container, textvariable=status_message,
         font=small, bg=white, fg=gray_text).pack(anchor="w", pady=(6, 0))

buttons_row = tk.Frame(container, bg=white)
buttons_row.pack(fill="x", pady=(14, 0))

def generate_password():
    character_pool = ""
    if include_uppercase.get(): character_pool += string.ascii_uppercase  # A-Z
    if include_lowercase.get(): character_pool += string.ascii_lowercase  # a-z
    if include_numbers.get():   character_pool += string.digits           # 0-9
    if include_symbols.get():   character_pool += string.punctuation      # !@#$ etc.

    if not character_pool:
        status_message.set("Select at least one option.")
        return

    length = length_input.get()

    new_password = "".join(random.choice(character_pool) for _ in range(length))
    generated_password.set(new_password)
    status_message.set("")

def copy_password():
    pwd = generated_password.get()
    if not pwd:
        status_message.set("Nothing to copy yet.")
        return
    window.clipboard_clear()
    window.clipboard_append(pwd)   # puts the password on your clipboard
    status_message.set("Copied to clipboard.")

tk.Button(buttons_row, text="Generate", font=button_font,
          bg=dark, fg=white,
          activebackground="#333333", activeforeground=white,
          relief="flat", bd=0, padx=18, pady=8,
          cursor="hand2", command=generate_password).pack(side="left", padx=(0, 8))

tk.Button(buttons_row, text="Copy", font=button_font,
          bg=light_gray, fg=dark,
          activebackground="#dddddd", activeforeground=dark,
          relief="flat", bd=0, padx=18, pady=8,
          cursor="hand2", command=copy_password).pack(side="left")

window.mainloop()