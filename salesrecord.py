import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Treeview
from tkinter import Entry, Text, Button, PhotoImage
import sqlite3
import navigation

def fetch_sales_records():
    """Fetch sales records from the SQLite database."""
    connection = sqlite3.connect("DB/DrugsInventory.db")
    cursor = connection.cursor()

    try:
        query = """
        SELECT 
            s.SaleID,
            c.CustomerName,
            d.DrugName,
            s.Quantity,
            s.TotalPrice,
            s.SaleDate
        FROM 
            Sale s
        JOIN 
            Customer c ON s.CustomerID = c.CustomerID
        JOIN 
            Drug d ON s.DrugID = d.DrugID;
        """
        cursor.execute(query)
        records = cursor.fetchall()
        return records
    except sqlite3.Error as e:
        print(f"Error fetching sales records: {e}")
        return []
    finally:
        connection.close()

def create_table(canvas):
    """Create a Treeview and populate it with sales records."""
    tree = Treeview(canvas, columns=("SaleID", "CustomerName", "DrugName", "Quantity", "TotalPrice", "SaleDate"), show="headings", height=150, padding=(0, 15))

    # Configure Treeview columns and headings
    tree.heading("SaleID", text="ID")
    tree.heading("CustomerName", text="Customer Name")
    tree.heading("DrugName", text="Drug Name")
    tree.heading("Quantity", text="Quantity")
    tree.heading("TotalPrice", text="Total Price")
    tree.heading("SaleDate", text="Sale Date")

    tree.column("SaleID", width=0, stretch=False)  # Hidden column for ID
    tree.column("CustomerName", anchor="center", width=150)
    tree.column("DrugName", anchor="center", width=150)
    tree.column("Quantity", anchor="center", width=100)
    tree.column("TotalPrice", anchor="center", width=120)
    tree.column("SaleDate", anchor="center", width=150)

    style = ttk.Style()
    style.configure("Treeview", font=("Ubuntu Regular", 14), padding=(0, 24))
    style.configure("Treeview.Heading", font=("Ubuntu Regular", 18), background="red", padding=(0, 16))

    # Fetch data from the database
    data = fetch_sales_records()

    # Populate the Treeview with database data
    for row in data:
        tree.insert("", tk.END, values=row)

    # Place the Treeview on the canvas
    tree.place(x=318.0, y=87.0, width=1235.0 - 318.0, height=746.0 - 87.0)

    return tree

def salesrecord(window, canvas):
    """Display the sales records."""
    navigation.drawUI("salesrecord", window, canvas)

    # Create the Treeview for sales records
    navigation.tree = create_table(canvas)
