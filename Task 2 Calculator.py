import tkinter as tk

root = tk.Tk()
root.title("Calculator")
root.resizable(False, False)

expression = ""
display_text = tk.StringVar()
display_text.set("0")

def button_click(char):
    global expression
    if expression == "0" or expression == "Error":
        expression = str(char)
    else:
        expression += str(char)
    display_text.set(expression)

def clear():
    global expression
    expression = "0"
    display_text.set("0")

def backspace():
    global expression
    expression = expression[:-1]
    if expression == "":
        expression = "0"
    display_text.set(expression)

def calculate():
    global expression
    try:
        result = eval(expression)
        if result == int(result):
            result = int(result)
        expression = str(result)
        display_text.set(expression)
    except ZeroDivisionError:
        display_text.set("Can't divide by 0")
        expression = "0"
    except:
        display_text.set("Error")
        expression = "0"

# display
tk.Label(root, textvariable=display_text, font=("Arial", 24), anchor="e",
         width=15, relief="sunken", bd=2).grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# buttons
buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"],
]

for r, row in enumerate(buttons):
    for c, label in enumerate(row):
        if label == "=":
            cmd = calculate
        else:
            cmd = lambda l=label: button_click(l)

        tk.Button(root, text=label, font=("Arial", 18), width=4, height=2,
                  command=cmd).grid(row=r+1, column=c, padx=5, pady=5)

# clear and backspace buttons
tk.Button(root, text="C", font=("Arial", 18), width=4, height=2,
          command=clear).grid(row=5, column=0, padx=5, pady=5)

tk.Button(root, text="<-", font=("Arial", 18), width=4, height=2,
          command=backspace).grid(row=5, column=1, padx=5, pady=5)

def key_press(event):
    key = event.char
    if key in "0123456789.+-*/":
        button_click(key)
    elif key == "\r":
        calculate()
    elif key == "\x08":
        backspace()

root.bind("<Key>", key_press)
root.mainloop()