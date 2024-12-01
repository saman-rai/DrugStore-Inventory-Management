from tkinter import Tk, Canvas
import navigation


window = Tk()

window.geometry("1280x832")
window.configure(bg = "#000")
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 832,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
    )

canvas.place(x = 0, y = 0)

current_page = "login"
navigation.gotoLogin(window, canvas)
window.resizable(False, False)
window.mainloop()