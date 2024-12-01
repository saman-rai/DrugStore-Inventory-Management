import tkinter as tk
from tkinter import ttk
from tkinter import Entry, Button, PhotoImage, Label
import sqlite3
import navigation

def add_to_database(drug_name, purchase_price, selling_price, stock_quantity):
    connection = sqlite3.connect("DB/DrugsInventory.db")
    cursor = connection.cursor()

    query = """
    INSERT INTO Drug (DrugName, PurchasePrice, SellingPrice, StockQuantity)
    VALUES (?, ?, ?, ?);
    """
    cursor.execute(query, (drug_name, purchase_price, selling_price, stock_quantity))

    connection.commit()
    print(f"Drug '{drug_name}' added successfully.")
    connection.close()

def submitForm(entries, message_label, canvas):
    """Handles form submission."""
    # Retrieve data from entries
    drug_name = entries["drug_name"].get().strip()
    stock_qty = entries["stock_qty"].get().strip()
    purchase_price = entries["purchase_price"].get().strip()
    selling_price = entries["selling_price"].get().strip()

    # Validate data
    if not drug_name:
        canvas.itemconfig(message_label, text="Error: Drug name is required.", fill="#f00")
        # message_label.config(text="Error: Drug name is required.", fg="red")
        return

    if not stock_qty.isdigit():
        canvas.itemconfig(message_label, text="Error: Stock quantity must be a number.", fill="#f00")
        # message_label.config(text="Error: Stock quantity must be a number.", fg="red")
        return

    try:
        purchase_price = float(purchase_price)
    except ValueError:
        canvas.itemconfig(message_label, text="Error: Purchase price must be a valid number.", fill="#f00")
        # message_label.config(text="Error: Purchase price must be a valid number.", fg="red")
        return

    try:
        selling_price = float(selling_price)
    except ValueError:
        canvas.itemconfig(message_label, text="Error: Selling price must be a valid number.", fill="#f00")
        # message_label.config(text="Error: Selling price must be a valid number.", fg="red")
        return

    # Call the database function
    add_to_database(drug_name, purchase_price, selling_price,int(stock_qty))
    # Clear all entries
    for entry in entries.values():
        entry.delete(0, tk.END)

    # Show success message
    # message_label.config(text="Form submitted successfully!", fg="green")
    canvas.itemconfig(message_label, text="Form submitted successfully!", fill="#0f0")
    print("Form submitted successfully!")

def drawAddDrugForm(window, canvas):
    entries = {}

    # Add submission/done button
    window.button_image_9 = button_image_9 = PhotoImage(file="assets/done.png")
    button_9 = Button(
        image=button_image_9,
        borderwidth=0,
        highlightthickness=0,
        relief="flat"
    )
    button_9.place(x=644.0, y=514.0, width=266.0, height=74.0)

    # Add a label for validation messages
    message_label = canvas.create_text(644.0, 600.0,text="", font=("Ubuntu Regular", 14), fill="#000000")

    # Configure the button command
    button_9.config(command=lambda: submitForm(entries, message_label, canvas))

    # Drug name
    canvas.create_text(
        367.0, 230.0, anchor="nw", text="Drug name", fill="#000000", font=("Ubuntu Regular", 18 * -1)
    )
    window.entry_image_1 = entry_image_1 = PhotoImage(file="assets/entry.png")
    entry_bg_1 = canvas.create_image(558.0, 290.0, image=entry_image_1)
    entry_1 = Entry(bd=0, bg="#DBF8FF", fg="#000716", highlightthickness=0)
    entry_1.place(x=367.0, y=265.0, width=382.0, height=48.0)
    entries["drug_name"] = entry_1

    # Stock quantity
    canvas.create_text(
        805.0, 230.0, anchor="nw", text="Stock Qty", fill="#000000", font=("Ubuntu Regular", 18 * -1)
    )
    entry_bg_2 = canvas.create_image(996.0, 290.0, image=entry_image_1)
    entry_2 = Entry(bd=0, bg="#DBF8FF", fg="#000716", highlightthickness=0)
    entry_2.place(x=805.0, y=265.0, width=382.0, height=48.0)
    entries["stock_qty"] = entry_2

    # Purchase price
    canvas.create_text(
        367.0, 372.0, anchor="nw", text="Purchase Price", fill="#000000", font=("Ubuntu Regular", 18 * -1)
    )
    entry_bg_3 = canvas.create_image(558.0, 432.0, image=entry_image_1)
    entry_3 = Entry(bd=0, bg="#DBF8FF", fg="#000716", highlightthickness=0)
    entry_3.place(x=367.0, y=407.0, width=382.0, height=48.0)
    entries["purchase_price"] = entry_3

    # Selling price
    canvas.create_text(
        805.0, 372.0, anchor="nw", text="Selling Price", fill="#000000", font=("Ubuntu Regular", 18 * -1)
    )
    entry_bg_4 = canvas.create_image(996.0, 432.0, image=entry_image_1)
    entry_4 = Entry(bd=0, bg="#DBF8FF", fg="#000716", highlightthickness=0)
    entry_4.place(x=805.0, y=407.0, width=382.0, height=48.0)
    entries["selling_price"] = entry_4

    return entries

def adddrug(window, canvas):
    navigation.drawUI("adddrug", window, canvas)
    drawAddDrugForm(window, canvas)
