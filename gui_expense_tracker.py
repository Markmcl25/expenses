import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

FILENAME = 'expenses.json'

# Load and Save Functions
def load_expenses():
    try:
        with open(FILENAME, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_expenses(expenses):
    with open(FILENAME, 'w') as f:
        json.dump(expenses, f, indent=4)

# Add Expense Function
def add_expense():
    try:
        amount = float(entry_amount.get())
        category = entry_category.get()
        description = entry_description.get()
        date = datetime.now().strftime("%Y-%m-%d")

        if not category:
            messagebox.showwarning("Missing Info", "Category is required.")
            return

        expense = {
            "amount": amount,
            "category": category,
            "description": description,
            "date": date
        }

        expenses = load_expenses()
        expenses.append(expense)
        save_expenses(expenses)

        update_expense_list()
        update_total()
        clear_entries()

        messagebox.showinfo("Success", "Expense added!")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for amount.")

# View Expenses
def update_expense_list():
    expenses = load_expenses()
    listbox.delete(0, tk.END)
    for e in expenses:
        line = f"€{e['amount']} - {e['category']} ({e['date']}) - {e.get('description', '')}"
        listbox.insert(tk.END, line)

# Total Spent
def update_total():
    expenses = load_expenses()
    total = sum(e['amount'] for e in expenses)
    label_total.config(text=f"💸 Total Spent: €{total:.2f}")

# Clear Input Fields
def clear_entries():
    entry_amount.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_description.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Expense Tracker")

# Labels and Entries
tk.Label(root, text="Amount (€):").grid(row=0, column=0)
entry_amount = tk.Entry(root)
entry_amount.grid(row=0, column=1)

tk.Label(root, text="Category:").grid(row=1, column=0)
entry_category = tk.Entry(root)
entry_category.grid(row=1, column=1)

tk.Label(root, text="Description:").grid(row=2, column=0)
entry_description = tk.Entry(root)
entry_description.grid(row=2, column=1)

tk.Button(root, text="Add Expense", command=add_expense).grid(row=3, column=0, columnspan=2, pady=5)

# Expense List
listbox = tk.Listbox(root, width=50)
listbox.grid(row=4, column=0, columnspan=2, pady=10)

# Total Label
label_total = tk.Label(root, text="💸 Total Spent: €0.00", font=("Arial", 12, "bold"))
label_total.grid(row=5, column=0, columnspan=2, pady=5)

# Load existing expenses
update_expense_list()
update_total()

root.mainloop()
