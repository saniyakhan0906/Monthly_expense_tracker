from expense import Expense
from datetime import datetime, timedelta
import matplotlib.pyplot as plt



def main():
    print(f"🎯 Running Expense Tracker!")
    expense_file_path = "./expenses.csv"
    budget = 10000
    
    # Get the user's input for expense
    expense = get_user_expense()

    # Write their expense to a file
    save_expense_to_file(expense, expense_file_path)

    # Read file and summarize expense
    summarize_expense(expense_file_path, budget)

def get_user_expense():
    print(f"🎯 Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))

    # List of expense categories
    expense_categories = [
        "🍩 Food", 
        "🏠 Home", 
        "💼 Work",
        "🍻 Fun",
        "✨ Misc",
        "🛵 Transportation",
        "🩺 Health & Beauty",
        "📚 Education",
        "🛒🛍️ Shopping",
    ]

    while True:
        print("Select a category:")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        # Get category selection from user
        value_range = f"1-{len(expense_categories)}"
        selected_index = int(input(f"Enter a category number ({value_range}): ")) - 1
        
        if 0 <= selected_index < len(expense_categories):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)
            return new_expense
        else:
            print("Invalid selection. Please try again.")

def save_expense_to_file(expense, expense_file_path):
    print(f"🎯 Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")





def summarize_expense(expense_file_path, budget):
    print(f"🎯 Summarizing User Expense from {expense_file_path}")
    
    expenses = []
    total_expenses = 0
    amount_by_category = {}

    with open(expense_file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines
            if not line:
                continue
            
            # Split line and validate data
            values = line.split(",")
            if len(values) != 3:
                print(f"Skipping line with unexpected format: {line}")
                continue
            
            name, amount, category = values
            amount = float(amount)
            
            # Create an Expense object and add it to the expenses list
            expense = Expense(name=name, amount=amount, category=category)
            expenses.append(expense)
            
            # Track total expenses
            total_expenses += amount
            
            # Track expenses by category
            if category in amount_by_category:
                amount_by_category[category] += amount
            else:
                amount_by_category[category] = amount
            
            # Print the expense details
            print(f"Expense: {name}, Category: {category}, Amount: ₹{amount:.2f}")

    # Print total expenses
    print(f"Total Expenses: ₹{total_expenses:.2f}")

    # Print expenses by category
    print("Expenses by category:")
    for category, amount in amount_by_category.items():
        print(f"{category}: ₹{amount:.2f}")

    # Calculate total spent and remaining budget
    total_spent = sum(expense.amount for expense in expenses)
    remaining_budget = budget - total_spent

    # Calculate the current date and the number of days left in the month
    today = datetime.now()
    current_month_days = (datetime(today.year, today.month + 1, 1) - timedelta(days=1)).day
    days_left_in_month = current_month_days - today.day

    # Calculate the amount left to spend per day in the current month
    if days_left_in_month > 0:
        daily_budget_remaining = remaining_budget / days_left_in_month
    else:
        daily_budget_remaining = 0

    # Print total spent, remaining budget, and daily budget remaining
    print(f"💸 Total spent: ₹{total_spent:.2f}")
    print(f"✅ Budget remaining: ₹{remaining_budget:.2f}")
    print(f"📅 Remaining budget per day in month: ₹{daily_budget_remaining:.2f}")

    # Generate a pie chart for budget distribution
    categories = list(amount_by_category.keys())
    amounts = list(amount_by_category.values())
    
    plt.figure(figsize=(8, 8))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Budget Distribution by Category")
    plt.show()



    # Print total spent and remaining budget
    print(f"💸 Total spent: {total_spent:.2f}")
    print(f"✅ Budget remaining: {remaining_budget:.2f}")
if __name__ == "__main__":
    main()

