import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Treeview
from tkinter import Entry, Text, Button, PhotoImage

import navigation

import sqlite3
from tkinter import ttk
def add_to_database(drug_id, supplier_id, qty):
    """Function to add the purchase data to the database, update drug stock quantity, and deduct funds."""
    connection = sqlite3.connect("DB/DrugsInventory.db")
    cursor = connection.cursor()

    try:
        # Fetch the purchase price of the drug
        cursor.execute("SELECT PurchasePrice FROM Drug WHERE DrugID = ?;", (drug_id,))
        purchase_price = cursor.fetchone()[0]

        # Calculate the total cost
        total_cost = purchase_price * qty

        # Check if sufficient funds are available
        cursor.execute("SELECT CurrentAmount FROM Fund;")
        current_fund = cursor.fetchone()[0]
        if current_fund < total_cost:
            print("Error: Insufficient funds to complete the purchase.")
            return

        # Insert purchase record into the Purchase table
        insert_query = """
        INSERT INTO Purchase (DrugID, SupplierID, Quantity, PurchaseDate)
        VALUES (?, ?, ?, DATE('now'));
        """
        cursor.execute(insert_query, (drug_id, supplier_id, qty))

        # Update the stock quantity in the Drug table
        update_query = """
        UPDATE Drug
        SET StockQuantity = StockQuantity + ?
        WHERE DrugID = ?;
        """
        cursor.execute(update_query, (qty, drug_id))

        # Deduct the total cost from the fund
        deduct_fund_query = """
        UPDATE Fund
        SET CurrentAmount = CurrentAmount - ?;
        """
        cursor.execute(deduct_fund_query, (total_cost,))

        # Commit the transaction
        connection.commit()
        print(f"Purchase data added, stock quantity updated, and ${total_cost:.2f} deducted from fund.")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()

def submitForm(entries, message_label, canvas):
    """Handles form submission with validation."""
    selected_drug = entries["drug_name"].get().strip()
    selected_supplier = entries["supplier"].get().strip()
    qty = entries["qty"].get().strip()

    # Validation checks
    if not selected_drug:
        canvas.itemconfig(message_label, text="Error: Please select a drug.", fill="#f00")
        return
    if not selected_supplier:
        canvas.itemconfig(message_label, text="Error: Please select a supplier.", fill="#f00")
        return
    if not qty.isdigit() or int(qty) <= 0:
        canvas.itemconfig(message_label, text="Error: Quantity must be a positive number.", fill="#f00")
        return

    # Extract IDs from selected options
    drug_id, drug_name = selected_drug.split(":")
    supplier_id, supplier_name = selected_supplier.split(":")
    qty = int(qty)

    # Call database function
    add_to_database(drug_id, supplier_id, qty)

    # Success message and clear entries
    canvas.itemconfig(message_label, text="Purchase added successfully!", fill="#0a0")
    entries["drug_name"].set("")  # Clear dropdown
    entries["supplier"].set("")  # Clear dropdown
    entries["qty"].delete(0, tk.END)  # Clear quantity entry

def fetch_drug_names():
    """Fetch drug IDs and names from the database."""
    connection = sqlite3.connect("DB/DrugsInventory.db")
    cursor = connection.cursor()

    query = "SELECT DrugID, DrugName FROM Drug;"
    cursor.execute(query)
    drug_options = [f"{row[0]}:{row[1]}" for row in cursor.fetchall()]  # Format as ID:DrugName

    connection.close()
    return drug_options
def fetch_supplier_names():
    """Fetch supplier IDs and names from the database."""
    connection = sqlite3.connect("DB/DrugsInventory.db")
    cursor = connection.cursor()

    query = "SELECT SupplierID, SupplierName FROM Supplier;"
    cursor.execute(query)
    supplier_options = [f"{row[0]}:{row[1]}" for row in cursor.fetchall()]  # Format as ID:SupplierName

    connection.close()
    return supplier_options

def drawPurchaseForm(window, canvas):
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

    # Drug dropdown with ID:DrugName format
    canvas.create_text(
        367.0, 230.0, anchor="nw", text="Drug name", fill="#000000", font=("Ubuntu Regular", 18 * -1)
    )
    drug_options = fetch_drug_names()  # Get options as ID:DrugName
    drug_dropdown = ttk.Combobox(
        window,
        values=drug_options,
        state="readonly",  # Dropdown is read-only
        font=("Ubuntu Regular", 14)
    )
    drug_dropdown.place(x=367.0, y=265.0, width=382.0, height=48.0)
    drug_dropdown.set("")  # Default empty selection
    entries["drug_name"] = drug_dropdown

    # Supplier dropdown with ID:SupplierName format
    canvas.create_text(
        805.0, 230.0, anchor="nw", text="Supplier", fill="#000000", font=("Ubuntu Regular", 18 * -1)
    )
    supplier_options = fetch_supplier_names()  # Get options as ID:SupplierName
    supplier_dropdown = ttk.Combobox(
        window,
        values=supplier_options,
        state="readonly",  # Dropdown is read-only
        font=("Ubuntu Regular", 14)
    )
    supplier_dropdown.place(x=805.0, y=265.0, width=382.0, height=48.0)
    supplier_dropdown.set("")  # Default empty selection
    entries["supplier"] = supplier_dropdown

    # Quantity entry
    canvas.create_text(
        367.0, 372.0, anchor="nw", text="Quantity", fill="#000000", font=("Ubuntu Regular", 18 * -1)
    )
    window.entry_image_1 = entry_image_1 = PhotoImage(file="assets/entry.png")
    entry_bg_3 = canvas.create_image(558.0, 432.0, image=entry_image_1)
    entry_3 = Entry(bd=0, bg="#DBF8FF", fg="#000716", highlightthickness=0)
    entry_3.place(x=367.0, y=407.0, width=382.0, height=48.0)
    entries["qty"] = entry_3

    return entries

def purchasedrug(window, canvas):
    navigation.drawUI("purchasedrug",window, canvas)

    drawPurchaseForm(window, canvas)

