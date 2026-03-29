import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# ML imports
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LinearRegression
import numpy as np

FILE = "expenses.csv"

# ---------------- ML MODEL (Categorization) ----------------
texts = ["pizza", "burger", "bus", "uber", "movie", "snacks"]
labels = ["Food", "Food", "Travel", "Travel", "Entertainment", "Food"]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)

def predict_category(text):
    return model.predict(vectorizer.transform([text]))[0]

# ---------------- ADD EXPENSE ----------------
def add_expense():
    desc = input("Enter description: ")
    amount = float(input("Enter amount: "))
    category = predict_category(desc)
    date = datetime.now().strftime("%Y-%m-%d")

    with open(FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, desc, category, amount])

    print(f"Added under category: {category}")

# ---------------- VIEW & ANALYSIS ----------------
def show_summary():
    try:
        df = pd.read_csv(FILE, names=["Date", "Desc", "Category", "Amount"])

        total = df["Amount"].sum()
        print("\nTotal Spending:", total)

        category_sum = df.groupby("Category")["Amount"].sum()
        print("\nCategory-wise:\n", category_sum)

        # Pattern detection
        print("\nYou spend most on:", category_sum.idxmax())

        category_sum.plot(kind="bar")
        plt.title("Expenses by Category")
        plt.show()

    except:
        print("No data found.")

# ---------------- BUDGET ALERT ----------------
def budget_alert():
    limit = float(input("Enter your budget: "))
    df = pd.read_csv(FILE, names=["Date", "Desc", "Category", "Amount"])

    total = df["Amount"].sum()
    if total > limit:
        print("⚠️ Budget exceeded!")
    else:
        print("Within budget.")p

# ---------------- PREDICTION ----------------
def predict_spending():
    df = pd.read_csv(FILE, names=["Date", "Desc", "Category", "Amount"])

    df["Day"] = np.arange(len(df))

    X = df[["Day"]]
    y = df["Amount"]

    model = LinearRegression()
    model.fit(X, y)
  
    future_day = np.array([[len(df) + 1]])
    prediction = model.predict(future_day)

    print("Predicted next expense:", prediction[0])

# ---------------- MENU ----------------
def main():
    while True:
        print("\n1. Add Expense")
        print("2. Show Summary")
        print("3. Budget Alert")
        print("4. Predict Spending")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            show_summary()
        elif choice == "3":
            budget_alert()
        elif choice == "4":
            predict_spending()
        elif choice == "5":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
