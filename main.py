import sqlite3
import curses
from datetime import datetime
import csv

# Database setup
def init_db():
    conn = sqlite3.connect('expenses.db')
    with open('schema.sql') as f:
        conn.executescript(f.read())
    conn.close()

# Add an expense
def add_expense(description, amount, category):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (description, amount, category)
        VALUES (?, ?, ?)
    ''', (description, amount, category))
    conn.commit()
    conn.close()

# View all expenses
def get_expenses():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
    expenses = cursor.fetchall()
    conn.close()
    return expenses

# Get spending summary
def get_summary():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    summary = cursor.fetchall()
    conn.close()
    return summary

# Export expenses to CSV
def export_to_csv(filename='expenses.csv'):
    expenses = get_expenses()
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Description', 'Amount', 'Category', 'Date'])
        writer.writerows(expenses)

# Terminal UI
def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Expense Tracker", curses.A_BOLD)
        stdscr.addstr(2, 0, "1. Add Expense")
        stdscr.addstr(3, 0, "2. View Expenses")
        stdscr.addstr(4, 0, "3. View Spending Summary")
        stdscr.addstr(5, 0, "4. Export to CSV")
        stdscr.addstr(6, 0, "5. Exit")
        stdscr.refresh()

        key = stdscr.getch()

        if key == ord('1'):
            stdscr.clear()
            stdscr.addstr(0, 0, "Enter description: ")
            curses.echo()
            description = stdscr.getstr(1, 0).decode('utf-8')
            stdscr.addstr(2, 0, "Enter amount: ")
            amount = float(stdscr.getstr(3, 0).decode('utf-8'))
            stdscr.addstr(4, 0, "Enter category: ")
            category = stdscr.getstr(5, 0).decode('utf-8')
            curses.noecho()
            add_expense(description, amount, category)
            stdscr.addstr(7, 0, "Expense added successfully! Press any key to continue.")
            stdscr.getch()

        elif key == ord('2'):
            stdscr.clear()
            expenses = get_expenses()
            stdscr.addstr(0, 0, "ID | Description          | Amount | Category      | Date")
            for idx, expense in enumerate(expenses):
                stdscr.addstr(idx + 2, 0, f"{expense[0]} | {expense[1]:<20} | {expense[2]:<6} | {expense[3]:<12} | {expense[4]}")
            stdscr.addstr(len(expenses) + 3, 0, "Press any key to continue.")
            stdscr.getch()

        elif key == ord('3'):
            stdscr.clear()
            summary = get_summary()
            stdscr.addstr(0, 0, "Category      | Total Amount")
            for idx, (category, total) in enumerate(summary):
                stdscr.addstr(idx + 2, 0, f"{category:<12} | {total}")
            stdscr.addstr(len(summary) + 3, 0, "Press any key to continue.")
            stdscr.getch()

        elif key == ord('4'):
            export_to_csv()
            stdscr.addstr(8, 0, "Expenses exported to expenses.csv! Press any key to continue.")
            stdscr.getch()

        elif key == ord('5'):
            break

if __name__ == "__main__":
    init_db()
    curses.wrapper(main)