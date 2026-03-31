#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, simpledialog

# ML imports
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LinearRegression
import numpy as np

FILE = "expenses.csv"

# ---------------- ML MODEL ----------------
texts = [
    "pizza", "burger", "biryani", "sandwich", "coffee", "snacks",
    "bus", "train", "uber", "auto", "metro", "rapido",
    "movie", "netflix", "concert", "game", "event",
    "pen", "notebook", "book", "marker", "highlighter",
    "shirt", "jeans", "shoes", "jacket", "tshirt", "pants", "blazer",
    "soap", "toothpaste", "shampoo", "detergent", "hair oil"
]

labels = [
    "Food","Food","Food","Food","Food","Food",
    "Travel","Travel","Travel","Travel","Travel","Travel",
    "Entertainment","Entertainment","Entertainment","Entertainment","Entertainment",
    "Stationary","Stationary","Stationary","Stationary","Stationary",
    "Fashion","Fashion","Fashion","Fashion","Fashion","Fashion","Fashion",
    "Essentials","Essentials","Essentials","Essentials","Essentials"
]

vectorizer = CountVectorizer(lowercase=True, ngram_range=(1,2))
X = vectorizer.fit_transform(texts)

nb_model = MultinomialNB()
nb_model.fit(X, labels)

# ---------------- RETRAIN ----------------
def retrain_model():
    global vectorizer, nb_model
    vectorizer = CountVectorizer(lowercase=True, ngram_range=(1,2))
    X = vectorizer.fit_transform(texts)
    nb_model = MultinomialNB()
    nb_model.fit(X, labels)

# ---------------- PREDICT ----------------
def predict_category(text):
    global texts, labels

    text = text.lower().strip()
    X_input = vectorizer.transform([text])

    prediction = nb_model.predict(X_input)[0]
    probabilities = nb_model.predict_proba(X_input)[0]

    if text in texts:
        return prediction

    confidence = max(probabilities)

    if confidence < 0.3:
        correct = simpledialog.askstring(
            "Low Confidence",
            "Enter correct category:\n(Food/Travel/Entertainment/Stationary/Fashion/Essentials)"
        )

        if correct:
            texts.append(text)
            labels.append(correct)
            retrain_model()
            return correct

    return prediction

# ---------------- GUI FUNCTIONS ----------------
def gui_add_expense():
    global budget

    if budget == 0:
        messagebox.showerror("Error", "Please set budget first")
        return

    desc = desc_entry.get()

    try:
        amount = float(amount_entry.get())
    except:
        messagebox.showerror("Error", "Invalid amount")
        return

    category = predict_category(desc)
    date = datetime.now().strftime("%Y-%m-%d")

    with open(FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, desc, category, amount])

    messagebox.showinfo("Success", f"Added under: {category}")

    # CLEAR INPUTS 
    desc_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

    # BUDGET CHECK 
    try:
        df = pd.read_csv(FILE, names=["Date", "Desc", "Category", "Amount"])
        total = df["Amount"].sum()

        if total > budget:
            messagebox.showwarning("Alert", "🚨 Budget exceeded!")
        elif abs(total - budget) < 1:
            messagebox.showinfo("Notice", "🎯 Budget limit reached!")
        elif total >= 0.8 * budget:
            messagebox.showwarning("Warning", "⚠️ 80% budget used!")
    except Exception as e:
        print("Error:", e)

def gui_show_summary():
    try:
        df = pd.read_csv(FILE, names=["Date", "Desc", "Category", "Amount"])
        total = df["Amount"].sum()
        category_sum = df.groupby("Category")["Amount"].sum()

        messagebox.showinfo("Summary", f"Total: {total}\n\n{category_sum}")

        category_sum.plot(kind="bar")
        plt.title("Expenses by Category")
        plt.show()

    except:
        messagebox.showerror("Error", "No data found")

def gui_budget_status():
    try:
        df = pd.read_csv(FILE, names=["Date", "Desc", "Category", "Amount"])
        total = df["Amount"].sum()
        remaining = budget - total

        messagebox.showinfo("Budget",
                            f"Total: {total}\nBudget: {budget}\nRemaining: {remaining}")
    except:
        messagebox.showerror("Error", "No data found")

def gui_predict_spending():
    try:
        df = pd.read_csv(FILE, names=["Date", "Desc", "Category", "Amount"])
        df["Day"] = np.arange(len(df))

        X = df[["Day"]]
        y = df["Amount"]

        model = LinearRegression()
        model.fit(X, y)

        future = pd.DataFrame([[len(df)+1]], columns=["Day"])
        pred = model.predict(future)

        messagebox.showinfo("Prediction", f"Next expense: {pred[0]:.2f}")
    except:
        messagebox.showerror("Error", "Not enough data")

# ---------------- GUI SETUP ----------------
root = tk.Tk()
root.title("AI Expense Tracker")
root.geometry("300x400")

budget = 0

def set_budget():
    global budget
    try:
        budget = float(budget_entry.get())
        messagebox.showinfo("Success", f"Budget set: {budget}")
    except:
        messagebox.showerror("Error", "Invalid budget")

# Layout
tk.Label(root, text="Enter Budget").pack()
budget_entry = tk.Entry(root)
budget_entry.pack()
tk.Button(root, text="Set Budget", command=set_budget).pack(pady=5)

tk.Label(root, text="Description").pack()
desc_entry = tk.Entry(root)
desc_entry.pack()

tk.Label(root, text="Amount").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Button(root, text="Add Expense", command=gui_add_expense).pack(pady=5)
tk.Button(root, text="Show Summary", command=gui_show_summary).pack(pady=5)
tk.Button(root, text="Budget Status", command=gui_budget_status).pack(pady=5)
tk.Button(root, text="Predict Spending", command=gui_predict_spending).pack(pady=5)
tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

root.mainloop()

