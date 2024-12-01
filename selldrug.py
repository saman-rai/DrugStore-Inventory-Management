import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Treeview
from tkinter import Entry, Text, Button, PhotoImage

import navigation

import sqlite3
from tkinter import ttk
def fetch_customer_by_phone(phone):
    """Fetch customer ID by phone number."""
    connection = sqlite3.connect("DB/DrugsInventory.db")
    cursor = connection.cursor()

    query = "SELECT CustomerID FROM Customer WHERE CustomerPhoneNumber = ?;"
    cursor.execute(query, (phone,))
    result = cursor.fetchone()

    connection.close()
    return result[0] if result else None

def add_customer(name, phone):
    """Add a new customer and return the new customer ID."""
    connection = sqlite3.connect("DB/DrugsInventory.db")
    cursor = connection.cursor()

    query = "INSERT INTO Customer (CustomerName, CustomerPhoneNumber) VALUES (?, ?);"
    cursor.execute(query, (name, phone))
    customer_id = cursor.lastrowid

    connection.commit()
    connection.close()
    return customer_id

def fetch_drug_names():
    """Fetch drug IDs and names from the database."""
    connection = sqlite3.connect("DB/DrugsInventory.db")
    cursor = connection.cursor()

    query = "SELECT DrugID, DrugName FROM Drug;"
    cursor.execute(query)
    drug_options = [f"{row[0]}:{row[1]}" for row in cursor.fetchall()]  # Format as ID:DrugName

    connection.close()
    return drug_options
def process_sale(customer_id, drug_id, qty):
    """Process a drug sale."""
    connection = sqlite3.connect("DB/DrugsInventory.db")
    cursor = connection.cursor()

    try:
        # Fetch selling price and stock
        cursor.execute("SELECT SellingPrice, StockQuantity FROM Drug WHERE DrugID = ?;", (drug_id,))
        result = cursor.fetchone()
        selling_price, stock_qty = result

        # Validate stock availability
        if stock_qty < qty:
            raise ValueError("Insufficient stock to complete the sale.")

        # Calculate total price
        total_price = selling_price * qty

        # Insert sale record
        insert_query = """
        INSERT INTO Sale (CustomerID, DrugID, Quantity, SaleDate, TotalPrice)
        VALUES (?, ?, ?, DATE('now'), ?);
        """
        cursor.execute(insert_query, (customer_id, drug_id, qty, total_price))

        # Update drug stock
        update_stock_query = """
        UPDATE Drug
        SET StockQuantity = StockQuantity - ?
        WHERE DrugID = ?;
        """
        cursor.execute(update_stock_query, (qty, drug_id))

        # Update fund
        update_fund_query = """
        UPDATE Fund
        SET CurrentAmount = CurrentAmount + ?;
        """
        cursor.execute(update_fund_query, (total_price,))

        connection.commit()
        print(f"Sale completed successfully. Total price: ${total_price:.2f}")
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
def submitForm(entries, message_label, canvas):
    """Handles form submission with validation."""
    selected_drug = entries["drug_name"].get().strip()
    customer_name = entries["customer_name"].get().strip()
    customer_phone = entries["customer_phone"].get().strip()
    qty = entries["qty"].get().strip()

    # Validation checks
    if not selected_drug:
        canvas.itemconfig(message_label, text="Error: Please select a drug.", fill="#f00")
        return
    if not customer_name:
        canvas.itemconfig(message_label, text="Error: Customer name is required.", fill="#f00")
        return
    if not customer_phone.isdigit() or len(customer_phone) != 10:
        canvas.itemconfig(message_label, text="Error: Phone number must be a 10-digit number.", fill="#f00")
        return
    if not qty.isdigit() or int(qty) <= 0:
        canvas.itemconfig(message_label, text="Error: Quantity must be a positive number.", fill="#f00")
        return

    # Extract IDs from selected options
    drug_id, drug_name = selected_drug.split(":")
    qty = int(qty)

    # Fetch or create customer
    customer_id = fetch_customer_by_phone(customer_phone)
    if not customer_id:
        customer_id = add_customer(customer_name, customer_phone)

    try:
        # Process sale
        process_sale(customer_id, drug_id, qty)
        canvas.itemconfig(message_label, text="Sale completed successfully!", fill="#0a0")

        # Clear entries
        entries["drug_name"].set("")
        entries["customer_name"].delete(0, tk.END)
        entries["customer_phone"].delete(0, tk.END)
        entries["qty"].delete(0, tk.END)
    except ValueError as e:
        canvas.itemconfig(message_label, text=f"Error: {str(e)}", fill="#f00")
    except Exception as e:
        canvas.itemconfig(message_label, text="Error: An unexpected error occurred.", fill="#f00")


def drawSellDrugForm(window, canvas):
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
    message_label = canvas.create_text(644.0, 600.0, text="", font=("Ubuntu Regular", 14), fill="#000000")

    # Configure the button command
    button_9.config(command=lambda: submitForm(entries, message_label, canvas))

    # Drug dropdown
    canvas.create_text(
        367.0, 230.0, anchor="nw", text="Drug name", fill="#000000", font=("Ubuntu Regular", 18 * -1)
    )
    drug_options = fetch_drug_names()
    drug_dropdown = ttk.Combobox(
        window,
        values=drug_options,
        state="readonly",
        font=("Ubuntu Regular", 14)
    )
    drug_dropdown.place(x=367.0, y=265.0, width=382.0, height=48.0)
    drug_dropdown.set("")
    entries["drug_name"] = drug_dropdown

    # Customer name
    canvas.create_text(
        805.0, 230.0, anchor="nw", text="Customer Name", fill="#000000", font=("Ubuntu Regular", 18 * -1)
    )
    entry_name = Entry(bd=0, bg="#DBF8FF", fg="#000716", highlightthickness=0)
    entry_name.place(x=805.0, y=265.0, width=382.0, height=48.0)
    entries["customer_name"] = entry_name

    # Customer phone number
    canvas.create_text(
        367.0, 372.0, anchor="nw", text="Phone Number", fill="#000000", font=("Ubuntu Regular", 18 * -1)
    )
    entry_phone = Entry(bd=0, bg="#DBF8FF", fg="#000716", highlightthickness=0)
    entry_phone.place(x=367.0, y=407.0, width=382.0, height=48.0)
    entries["customer_phone"] = entry_phone

    # Quantity
    canvas.create_text(
        805.0, 372.0, anchor="nw", text="Quantity", fill="#000000", font=("Ubuntu Regular", 18 * -1)
    )
    entry_qty = Entry(bd=0, bg="#DBF8FF", fg="#000716", highlightthickness=0)
    entry_qty.place(x=805.0, y=407.0, width=382.0, height=48.0)
    entries["qty"] = entry_qty

    return entries

def selldrug(window, canvas):
    navigation.drawUI("selldrug",window, canvas)

    drawSellDrugForm(window, canvas)

