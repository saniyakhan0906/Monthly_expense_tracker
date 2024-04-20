import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

from flask import Flask, render_template, request, redirect, url_for
from expense import Expense
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

expenses = []
budget = 10000
expense_file_path = "./expenses.csv"
static = os.path.join(app.root_path, 'static')  # Static folder path

@app.route('/')
def index():
    total_spent, remaining_budget, daily_budget_remaining, amount_by_category = summarize_expense(expense_file_path, budget)
    return render_template('index.html', expenses=expenses, total_spent=total_spent, remaining_budget=remaining_budget, daily_budget_remaining=daily_budget_remaining)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    name = request.form['name']
    amount = float(request.form['amount'])
    category = request.form['category']
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_expense = Expense(name=name, amount=amount, category=category)
    expenses.append(new_expense)
    save_expense_to_file(new_expense, expense_file_path)
    return redirect(url_for('index'))

@app.route('/summary')
def summary():
    total_spent, remaining_budget, daily_budget_remaining, amount_by_category = summarize_expense(expense_file_path, budget)
    return render_template('summary.html', total_spent=total_spent, remaining_budget=remaining_budget, daily_budget_remaining=daily_budget_remaining, amount_by_category=amount_by_category)

def save_expense_to_file(expense, expense_file_path):
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")

def summarize_expense(expense_file_path, budget):
    expenses = []
    total_expenses = 0
    amount_by_category = {}

    with open(expense_file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            values = line.split(",")
            if len(values) != 3:
                print(f"Skipping line with unexpected format: {line}")
                continue
            
            name, amount, category = values
            amount = float(amount)
            
            expense = Expense(name=name, amount=amount, category=category)
            expenses.append(expense)
            
            total_expenses += amount
            
            if category in amount_by_category:
                amount_by_category[category] += amount
            else:
                amount_by_category[category] = amount

    total_spent = sum(expense.amount for expense in expenses)
    remaining_budget = budget - total_spent

    today = datetime.now()
    current_month_days = (datetime(today.year, today.month + 1, 1) - timedelta(days=1)).day
    days_left_in_month = current_month_days - today.day

    if days_left_in_month > 0:
        daily_budget_remaining = remaining_budget / days_left_in_month
    else:
        daily_budget_remaining = 0

    categories = list(amount_by_category.keys())
    amounts = list(amount_by_category.values())

    plt.figure(figsize=(8, 8))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Budget Distribution by Category")
    img_path = os.path.join(static, 'budget_distribution.png')
    plt.savefig(img_path)  # Save the plot as a static file
    plt.close()

    return total_spent, remaining_budget, daily_budget_remaining, amount_by_category

if __name__ == '__main__':
    app.run(debug=True)
