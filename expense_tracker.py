import json
from datetime import datetime

FILENAME = 'expenses.json'

def load_expenses():
    try:
        with open(FILENAME, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_expenses(expenses):
    with open(FILENAME, 'w') as f:
        json.dump(expenses, f, indent=4)

def add_expense():
    amount = float(input("Enter amount: €"))
    category = input("Enter category (e.g., Food, Rent): ")
    description = input("Optional description: ")
    date = datetime.now().strftime("%Y-%m-%d")
    expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }
    expenses = load_expenses()
    expenses.append(expense)
    save_expenses(expenses)
    print("✅ Expense added!")

def view_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return
    for i, e in enumerate(expenses, start=1):
        print(f"{i}. €{e['amount']} - {e['category']} ({e['date']}) - {e.get('description', '')}")

def show_total():
    expenses = load_expenses()
    total = sum(e["amount"] for e in expenses)
    print(f"💸 Total spent: €{total:.2f}")

def menu():
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Total Spent")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            show_total()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()
