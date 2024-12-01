import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Treeview
from tkinter import Entry, Text, Button, PhotoImage
import sqlite3
import navigation

def fetch_purchase_records():
    """Fetch purchase records from the SQLite database."""
    connection = sqlite3.connect("DB/DrugsInventory.db")
    cursor = connection.cursor()

    try:
        query = """
        SELECT 
            p.PurchaseID,
            d.DrugName,
            s.SupplierName,
            p.Quantity,
            d.PurchasePrice,
            (p.Quantity * d.PurchasePrice) AS TotalCost,
            p.PurchaseDate
        FROM 
            Purchase p
        JOIN 
            Drug d ON p.DrugID = d.DrugID
        JOIN 
            Supplier s ON p.SupplierID = s.SupplierID;
        """
        cursor.execute(query)
        records = cursor.fetchall()
        return records
    except sqlite3.Error as e:
        print(f"Error fetching purchase records: {e}")
        return []
    finally:
        connection.close()

def create_table(canvas):
    """Create a Treeview and populate it with purchase records."""
    tree = Treeview(canvas, columns=("PurchaseID", "DrugName", "SupplierName", "Quantity", "PurchasePrice", "TotalCost", "PurchaseDate"), show="headings", height=150, padding=(0, 15))

    # Configure Treeview columns and headings
    tree.heading("PurchaseID", text="ID")
    tree.heading("DrugName", text="Drug Name")
    tree.heading("SupplierName", text="Supplier Name")
    tree.heading("Quantity", text="Quantity")
    tree.heading("PurchasePrice", text="Purchase Price")
    tree.heading("TotalCost", text="Total Cost")
    tree.heading("PurchaseDate", text="Purchase Date")

    tree.column("PurchaseID", width=0, stretch=False)  # Hidden column for ID
    tree.column("DrugName", anchor="center", width=150)
    tree.column("SupplierName", anchor="center", width=150)
    tree.column("Quantity", anchor="center", width=100)
    tree.column("PurchasePrice", anchor="center", width=120)
    tree.column("TotalCost", anchor="center", width=120)
    tree.column("PurchaseDate", anchor="center", width=150)

    style = ttk.Style()
    style.configure("Treeview", font=("Ubuntu Regular", 14), padding=(0, 24))
    style.configure("Treeview.Heading", font=("Ubuntu Regular", 18), background="red", padding=(0, 16))

    # Fetch data from the database
    data = fetch_purchase_records()

    # Populate the Treeview with database data
    for row in data:
        tree.insert("", tk.END, values=row)

    # Place the Treeview on the canvas
    tree.place(x=318.0, y=87.0, width=1235.0 - 318.0, height=746.0 - 87.0)

    return tree

def purchaserecord(window, canvas):
    navigation.drawUI("purchaserecord",window, canvas)

    navigation.tree = create_table(canvas)


