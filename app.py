from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect("expenses.db") as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT DEFAULT (datetime('now'))
            )
        ''')
        conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()

    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        description = request.form['description']
        c.execute("INSERT INTO expenses (amount, category, description) VALUES (?, ?, ?)",
                  (amount, category, description))
        conn.commit()
        return redirect('/')

    c.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = c.fetchall()

    c.execute("SELECT SUM(amount) FROM expenses")
    total = c.fetchone()[0] or 0

    conn.close()
    return render_template('index.html', expenses=expenses, total=total)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
