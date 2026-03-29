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
texts = ["pizza", "burger", "bus", "uber", "movie", "snacks", "train", "coffee"]
labels = ["Food", "Food", "Travel", "Travel", "Entertainment", "Food", "Travel", "Food"]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

nb_model = MultinomialNB()
nb_model.fit(X, labels)

def predict_category(text):
    X_input = vectorizer.transform([text])
     
    prediction = nb_model.predict(X_input)[0]
    probabilities = nb_model.predict_proba(X_input)[0]
    
    confidence = max(probabilities)

    print(f"Predicted Category: {prediction} (Confidence: {confidence:.2f})")

    # If confidence is low, ask user to confirm
    if confidence < 0.6:
        print("⚠️ Low confidence in prediction.")
        user_choice = input("Enter correct category (Food/Travel/Entertainment): ")
        return user_choice
    
    return prediction

# ---------------- ADD EXPENSE ----------------
def add_expense():
    desc = input("Enter description: ")
    amount = float(input("Enter amount: "))
    category = predict_category(desc)
    date = datetime.now().strftime("%Y-%m-%d")

    with open(FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, desc, category, amount])

    print(f"✅ Added under category: {category}")

# ---------------- SUMMARY & VISUALIZATION ----------------
def show_summary():
    try:
        df = pd.read_csv(FILE, names=["Date", "Desc", "Category", "Amount"])

        total = df["Amount"].sum()
        print("\n💰 Total Spending:", total)

        category_sum = df.groupby("Category")["Amount"].sum()
        print("\n📊 Category-wise Spending:\n", category_sum)

        print("\n🔍 You spend most on:", category_sum.idxmax())

        category_sum.plot(kind="bar")
        plt.title("Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount")
        plt.show()

    except:
        print("⚠️ No data found.")

# ---------------- BUDGET STATUS ----------------
def budget_status(budget):
    try:
        df = pd.read_csv(FILE, names=["Date", "Desc", "Category", "Amount"])
        total = df["Amount"].sum()

        print(f"\n💰 Total Spending: {total}")
        print(f"🎯 Budget: {budget}")

        remaining = budget - total
        print(f"💵 Remaining Budget: {remaining}")

        if total > budget:
            print("⚠️ Budget exceeded!")
        else:
            print("✅ You are within budget.")

    except:
        print("⚠️ No data found.")

# ---------------- PREDICTION ----------------
def predict_spending():
    try:
        df = pd.read_csv(FILE, names=["Date", "Desc", "Category", "Amount"])

        df["Day"] = np.arange(len(df))

        X = df[["Day"]]
        y = df["Amount"]

        lr_model = LinearRegression()
        lr_model.fit(X, y)

        future_day = pd.DataFrame([[len(df) + 1]], columns=["Day"])
        prediction = lr_model.predict(future_day)

        print(f"📈 Predicted next expense: {prediction[0]:.2f}")

    except:
        print("⚠️ Not enough data for prediction.")

# ---------------- MAIN MENU ----------------
def main():
    print("==== AI Expense Tracker ====")
    
    try:
        budget = float(input("Enter your monthly budget: "))
    except:
        print("Invalid input. Setting default budget = 0")
        budget = 0

    while True:
        print("\n--- MENU ---")
        print("1. Add Expense")
        print("2. Show Summary")
        print("3. Budget Status")
        print("4. Predict Spending")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            show_summary()
        elif choice == "3":
            budget_status(budget)
        elif choice == "4":
            predict_spending()
        elif choice == "5":
            print("Exiting... 👋")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
