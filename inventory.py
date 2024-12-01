import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Treeview
from tkinter import Entry, Text, Button, PhotoImage
import sqlite3
import navigation
def edit_cell(tree, event, canvas):
    """Allows editing of Treeview cell values."""
    # Identify row and column clicked
    row_id = tree.identify_row(event.y)
    col_id = tree.identify_column(event.x)

    if not row_id or not col_id:
        return

    # Get current value of the cell
    col_index = int(col_id[1:]) - 1
    current_value = tree.item(row_id)["values"][col_index]

    # Get the cell's bounding box
    bbox = tree.bbox(row_id, col_id)

    if not bbox:
        return

    # Create an Entry widget to overlay the cell
    entry = tk.Entry(canvas)
    entry.insert(0, current_value)
    entry.focus()

    # Place the Entry widget over the cell
    entry.place(x=bbox[0] + 318.0, y=bbox[1] + 87.0, width=bbox[2], height=bbox[3])

    def send_updated_data(row_id, column, new_value):
        """Send the updated data along with ID to another function."""
        item_values = tree.item(row_id)["values"]
        record_id = item_values[0]  # Assuming the first column (ID) is hidden and stores the ID
        updated_data = {  # Example payload
            "id": record_id,
            "column": column,
            "new_value": new_value
        }
        # Call your function here (replace `process_update` with your function name)
        print(updated_data)

    def save_edit(event=None):
        """Save the edited value back to the Treeview and send the updated data."""
        new_value = entry.get()
        values = list(tree.item(row_id)["values"])
        values[col_index] = new_value
        tree.item(row_id, values=values)  # Update Treeview with new value
        entry.destroy()

        # Send the updated data along with the ID
        column_name = tree["columns"][col_index]  # Get the column name
        send_updated_data(row_id, column_name, new_value)

    def cancel_edit(event=None):
        """Cancel editing without saving changes."""
        entry.destroy()

    # Bind events to save or cancel editing
    entry.bind("<Return>", save_edit)
    entry.bind("<Escape>", cancel_edit)

def fetch_drug_data():
    """Fetch drug data from the SQLite database."""
    connection = sqlite3.connect("DB/DrugsInventory.db")
    cursor = connection.cursor()

    query = "SELECT DrugID, DrugName, PurchasePrice, SellingPrice, StockQuantity FROM Drug;"
    cursor.execute(query)
    data = cursor.fetchall()

    connection.close()
    return data

def fetch_fund_amount():
    """Fetch the current fund amount from the database."""
    connection = sqlite3.connect("DB/DrugsInventory.db")
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT CurrentAmount FROM Fund;")
        current_fund = cursor.fetchone()[0]
        return current_fund
    except sqlite3.Error as e:
        print(f"Error fetching fund amount: {e}")
        return 0.0
    finally:
        connection.close()

def create_table(canvas):
    """Create a Treeview and populate it with data from the database."""
    tree = Treeview(canvas, columns=("DrugID", "DrugName", "PurchasePrice", "SellingPrice", "StockQuantity"), show="headings", height=150, padding=(0, 15))

    # Configure Treeview columns and headings
    tree.heading("DrugID", text="ID")
    tree.heading("DrugName", text="Drug Name")
    tree.heading("PurchasePrice", text="Purchase Price")
    tree.heading("SellingPrice", text="Selling Price")
    tree.heading("StockQuantity", text="Stock Quantity")

    tree.column("DrugID", width=0, stretch=False)  # Hidden column for ID
    tree.column("DrugName", anchor="center")
    tree.column("PurchasePrice", anchor="center")
    tree.column("SellingPrice", anchor="center")
    tree.column("StockQuantity", anchor="center")

    style = ttk.Style()
    style.configure("Treeview", font=("Ubuntu Regular", 14), padding=(0, 24))
    style.configure("Treeview.Heading", font=("Ubuntu Regular", 18), background="red", padding=(0, 16))

    # Fetch data from the database
    data = fetch_drug_data()

    # Populate the Treeview with database data
    for row in data:
        tree.insert("", tk.END, values=row)

    # Place the Treeview on the canvas
    tree.place(x=318.0, y=87.0, width=1235.0 - 318.0, height=746.0 - 87.0)

    # Adjust column widths
    tree_width = tree.winfo_width()
    num_columns = len(tree["columns"]) - 1  # Exclude hidden ID column
    column_width = tree_width // num_columns

    for col in tree["columns"]:
        if col != "DrugID":  # Skip resizing the hidden ID column
            tree.column(col, width=column_width, stretch=True)

    # Bind double-click event for editing
    tree.bind("<Double-1>", lambda event: edit_cell(tree, event, canvas))
    return tree

def inventory(window, canvas):
    navigation.drawUI("inventory",window, canvas)

    navigation.tree = create_table(canvas)

    # Fetch the current total fund
    current_fund = fetch_fund_amount()

    # Display the total fund at the bottom
    canvas.create_text(
        800.0, 800.0,  # Adjust the position to fit your layout
        text=f"Current Total Fund: ${current_fund:.2f}",
        font=("Ubuntu Regular", 18),
        fill="green"
    )
