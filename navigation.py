from tkinter import Entry, Text, Button, PhotoImage
from login import login
from inventory import inventory
from purchasedrug import purchasedrug
from adddrug import adddrug
from addsupplier import addsupplier
from purchaserecord import purchaserecord
from selldrug import selldrug
from salesrecord import salesrecord
tree = None
def destoryTree():
    global tree
    print('a')
    # Destroy the Treeview if it exists
    if tree:
        tree.destroy()
        tree = None  # Reset the reference
def gotoLogin(window, canvas):
    login(window, canvas)
def gotoInventory(window, canvas):
    inventory(window, canvas)
def logOut(window,canvas):
    destoryTree()
    login(window, canvas)
def menu(select,window, canvas):
    destoryTree()
    drawUI(select,window, canvas)
    if(select=="inventory"):
        inventory(window, canvas)
    elif(select=="purchasedrug"):
        purchasedrug(window, canvas)
    elif(select=="adddrug"):
        adddrug(window,canvas)
    elif(select=="addsupplier"):
        addsupplier(window,canvas)
    elif(select=="purchaserecord"):
        purchaserecord(window,canvas)
    elif(select=="selldrug"):
        selldrug(window,canvas)
    elif(select=="salesrecord"):
        salesrecord(window,canvas)
    pass

def drawUI(select,window, canvas):
    canvas.delete("all")
    for widget in window.winfo_children():
        if isinstance(widget,Button) or isinstance(widget,Entry):
            widget.destroy()
    canvas.create_rectangle(
        318.0,
        87.0,
        1235.0,
        746.0,
        fill="#fff",
        outline="")
    
    if(select=="inventory"):
        window.button_image_1 = button_image_1 = PhotoImage(
        file="assets/inventory_selected.png")
    else:
        window.button_image_1 = button_image_1 = PhotoImage(
        file="assets/inventory.png")
    inventory = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: menu('inventory',window, canvas),
        relief="flat"
    )
    inventory.place(
        x=0.0,
        y=87.0,
        width=318.0,
        height=74.0
    )
    if(select=="purchasedrug"):
        window.button_image_2 = button_image_2 = PhotoImage(
        file="assets/purchasedrug_selected.png")
    else:
        window.button_image_2 = button_image_2 = PhotoImage(
        file="assets/purchasedrug.png")
    purchasedrug = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: menu('purchasedrug',window,canvas),
        relief="flat"
    )
    purchasedrug.place(
        x=0.0,
        y=161.0,
        width=318.0,
        height=74.0
    )
    if(select=="selldrug"):
        window.button_image_3 = button_image_3 = PhotoImage(
        file="assets/selldrug_selected.png")
    else:
        window.button_image_3 = button_image_3 = PhotoImage(
        file="assets/selldrug.png")
    selldrug = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: menu('selldrug',window,canvas),
        relief="flat"
    )
    selldrug.place(
        x=0.0,
        y=235.0,
        width=318.0,
        height=74.0
    )

    if(select == "purchaserecord"):
        window.button_image_4 = button_image_4 = PhotoImage(
        file="assets/purchaserecord_selected.png")
    else:
        window.button_image_4 = button_image_4 = PhotoImage(
        file="assets/purchaserecord.png")
    purchaserecord = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: menu('purchaserecord', window, canvas),
        relief="flat"
    )
    purchaserecord.place(
        x=0.0,
        y=309.0,
        width=318.0,
        height=74.0
    )

    if(select == "salesrecord"):
        window.button_image_5 = button_image_5 = PhotoImage(
        file="assets/salesrecord_selected.png")
    else:
        window.button_image_5 = button_image_5 = PhotoImage(
        file="assets/salesrecord.png")
    salesrecord = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: menu('salesrecord',window,canvas),
        relief="flat"
    )
    salesrecord.place(
        x=0.0,
        y=383.0,
        width=318.0,
        height=74.0
    )

    if(select=="addsupplier"):
        window.button_image_6 = button_image_6 = PhotoImage(
        file="assets/addsupplier_selected.png")
    else:
        window.button_image_6 = button_image_6 = PhotoImage(
        file="assets/addsupplier.png")
    addsupplier = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: menu('addsupplier',window,canvas),
        relief="flat"
    )
    addsupplier.place(
        x=0.0,
        y=457.0,
        width=318.0,
        height=74.0
    )

    if(select=="adddrug"):
        window.button_image_7 = button_image_7 = PhotoImage(
        file="assets/adddrug_selected.png")
    else:
        window.button_image_7 = button_image_7 = PhotoImage(
        file="assets/adddrug.png")
    adddrug = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: menu('adddrug',window,canvas),
        relief="flat"
    )
    adddrug.place(
        x=0.0,
        y=531.0,
        width=318.0,
        height=74.0
    )
    window.image_image_1 = image_image_1 = PhotoImage(
        file="assets/inventory_image_1.png")
    image_1 = canvas.create_image(
        640.0,
        43.0,
        image=image_image_1
    )

    canvas.create_text(
        43.0,
        25.0,
        anchor="nw",
        text="Drug Inventory Management System",
        fill="#000000",
        font=("Ubuntu Regular", 34 * -1)
    )

    # canvas.create_text(
    #     336.0,
    #     769.0,
    #     anchor="nw",
    #     text="Total Fund Available",
    #     fill="#000000",
    #     font=("Ubuntu Regular", 26 * -1)
    # )

    # canvas.create_text(
    #     1091.0,
    #     769.0,
    #     anchor="nw",
    #     text="$5000",
    #     fill="#000000",
    #     font=("Ubuntu Regular", 26 * -1)
    # )

    window.button_image_8 = button_image_8 = PhotoImage(
        file="assets/logout.png")
    logout = Button(
        image=button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: logOut(window,canvas),
        relief="flat"
    )
    logout.place(
        x=969.0,
        y=6.0,
        width=266.0,
        height=74.0
    )