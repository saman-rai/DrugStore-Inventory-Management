import tkinter as tk
from tkinter import ttk
from tkinter import Entry, Button, PhotoImage, Label
import sqlite3
import navigation

def add_supplier_to_database(supplier_name, supplier_phone):
    """Function to add supplier data to the database."""
    connection = sqlite3.connect("DB/DrugsInventory.db")
    cursor = connection.cursor()

    query = """
    INSERT INTO Supplier (SupplierName, SupplierPhoneNumber)
    VALUES (?, ?);
    """
    try:
        cursor.execute(query, (supplier_name, supplier_phone))
        connection.commit()
        print(f"Supplier '{supplier_name}' added successfully.")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()

def submitForm(entries, message_label, canvas):
    """Handles form submission."""
    # Retrieve data from entries
    supplier_name = entries["supplier_name"].get().strip()
    supplier_phone = entries["supplier_phone"].get().strip()

    # Validate data
    if not supplier_name:
        canvas.itemconfig(message_label, text="Error: Supplier name is required.", fill="#f00")
        return

    if not supplier_phone.isdigit() or len(supplier_phone) != 10:
        canvas.itemconfig(message_label, text="Error: Supplier phone must be a 10-digit number.", fill="#f00")
        return

    # Call the database function
    add_supplier_to_database(supplier_name, supplier_phone)

    # Clear all entries
    for entry in entries.values():
        entry.delete(0, tk.END)

    # Show success message
    canvas.itemconfig(message_label, text="Supplier added successfully!", fill="#0f0")
    print("Supplier added successfully!")

def drawAddSupplierForm(window, canvas):
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

    # Supplier name
    canvas.create_text(
        367.0, 230.0, anchor="nw", text="Supplier Name", fill="#000000", font=("Ubuntu Regular", 18 * -1)
    )
    window.entry_image_1 = entry_image_1 = PhotoImage(file="assets/entry.png")
    entry_bg_1 = canvas.create_image(558.0, 290.0, image=entry_image_1)
    entry_1 = Entry(bd=0, bg="#DBF8FF", fg="#000716", highlightthickness=0)
    entry_1.place(x=367.0, y=265.0, width=382.0, height=48.0)
    entries["supplier_name"] = entry_1

    # Supplier phone number
    canvas.create_text(
        805.0, 230.0, anchor="nw", text="Phone Number", fill="#000000", font=("Ubuntu Regular", 18 * -1)
    )
    entry_bg_2 = canvas.create_image(996.0, 290.0, image=entry_image_1)
    entry_2 = Entry(bd=0, bg="#DBF8FF", fg="#000716", highlightthickness=0)
    entry_2.place(x=805.0, y=265.0, width=382.0, height=48.0)
    entries["supplier_phone"] = entry_2

    return entries

def addsupplier(window, canvas):
    navigation.drawUI("addsupplier", window, canvas)
    drawAddSupplierForm(window, canvas)
