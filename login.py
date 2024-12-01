import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Treeview
from tkinter import Entry, Text, Button, PhotoImage
import navigation
def validate_user(username, password):
    """Validate the username and password against the Staff table."""
    connection = sqlite3.connect("DB/DrugsInventory.db")
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM Staff WHERE Username = ? AND Password = ?;"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        return user is not None  # Returns True if a match is found
    except sqlite3.Error as e:
        print(f"Error validating user: {e}")
        return False
    finally:
        connection.close()

def loginBtn(username_entry, password_entry, canvas, window, error_message):
    """Handle the login button click."""
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    # Validate input
    if not username or not password:
        canvas.itemconfig(error_message, text="Username and password are required!", fill="red")
        return

    # Validate user credentials
    if validate_user(username, password):
        navigation.gotoInventory(window, canvas)
    else:
        canvas.itemconfig(error_message, text="Invalid username or password.", fill="red")

def login(window, canvas):
    canvas.delete("all")
    for widget in window.winfo_children():
        if isinstance(widget,Button) or isinstance(widget,Entry) or isinstance(widget,Treeview):
            widget.destroy()
       
    
    window.image_image_1 = image_image_1 = PhotoImage(
        file="assets/image_1.png")
    image_1 = canvas.create_image(
        636.0,
        421.0,
        image=image_image_1
    )
    window.image_image_2 = image_image_2 = PhotoImage(
        file="assets/image_2.png")
    image_2 = canvas.create_image(
        359.0,
        283.0,
        image=image_image_2
    )
    
    window.image_image_3 = image_image_3 = PhotoImage(
        file="assets/image_3.png")
    image_3 = canvas.create_image(
        359.0,
        435.0,
        image=image_image_3
    )

    # Error Message
    error_message = canvas.create_text(
        173.0,
        480.0,
        anchor="nw",
        text="",
        fill="",
        font=("Ubuntu Regular", 14 * -1)
    )
    window.image_image_4 = image_image_4 = PhotoImage(
            file="assets/image_4.png")
    login_button = canvas.create_image(
            359.0,
            579.0,
            image=image_image_4
        )
    canvas.tag_bind(login_button, '<Button-1>', lambda e: loginBtn(username_entry, password_entry, canvas, window, error_message))
    
    window.image_image_5 = image_image_5 = PhotoImage(
        file="assets/image_5.png")
    image_5 = canvas.create_image(
        879.0,
        421.0,
        image=image_image_5
    )
    
    username_entry = Entry(
        bd=0,
        bg="#DBF8FF",
        fg="#000716",
        highlightthickness=0,
        font=20
    )
    username_entry.place(
        x=173.0,
        y=276.0,
        width=373.0,
        height=45.0
    )
    password_entry = Entry(
        bd=0,
        bg="#DBF8FF",
        fg="#000716",
        highlightthickness=0,
        font=20,
        show="*"
    )
    password_entry.place(
        x=173.0,
        y=427.0,
        width=373.0,
        height=45.0
    )
    