import tkinter as tk

def left_click(event):
    event.widget.configure(bg="green")
    textoPrueba.set("Jajaja")

def right_click(event):
    event.widget.configure(bg="red")
    textoPrueba.set("Jijiji")

root = tk.Tk()
button = tk.Frame(root, width=20, height=20, background="gray")
button.pack(padx=20, pady=20)
textoPrueba = tk.StringVar()
textoPrueba.set("Lol")

button.bind("<Button-1>", left_click)
button.bind("<Button-2>", right_click)
button.bind("<Button-3>", right_click)
labol = tk.Label(root, textvariable=textoPrueba )
labol.pack()

root.mainloop()
