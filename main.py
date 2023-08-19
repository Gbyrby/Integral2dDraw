from tkinter import messagebox
import os, sys

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from math import *
import numpy as np

root = Tk()
root.title("Integral2dDraw")
root.geometry("650x250")

img = Image.open("dxdy.png").resize((300, 100))
pimg = ImageTk.PhotoImage(img)
size = img.size
dx = []
dy = []


def clickdydx():
    window = Toplevel()
    surface = 0
    res = Scala.get()
    zoom = Scala2.get()

    try:
        dx.clear()
        dy.clear()
        dy.append(compile(dxmax2.get(), "<string>", "exec"))
        dy.append(compile(dxmax2.get(), "<string>", "exec"))
        dx.append(eval(dymax2.get()))
        dx.append(eval(dymin2.get()))
    except Exception as error:
        messagebox.showerror(
            "Error",
            f"В пределах интегрирования ошибки.\nНапример: неизвестные переменные или ошибки в формулах\n\nОшибка которая выводит сам Python:\n{error}",
        )
        return
    error = 0
    errorFlag = False
    anti = False
    window.focus()

    frame = Frame(window, width=500, height=500)
    frame.pack(expand=True, fill=BOTH)
    h = ttk.Scrollbar(frame, orient=HORIZONTAL)
    v = ttk.Scrollbar(frame, orient=VERTICAL)
    c = Canvas(
        frame,
        scrollregion=(-500, -500, 500, 500),
        width=500,
        height=500,
        bg="black",
        yscrollcommand=v.set,
        xscrollcommand=h.set,
    )
    h.pack(side=BOTTOM, fill=X)
    v.pack(side=RIGHT, fill=Y)
    h["command"] = c.xview
    v["command"] = c.yview
    c.yview_moveto(0.25)
    c.xview_moveto(0.25)
    c.pack(side=LEFT, expand=True, fill=BOTH)

    dy[0] = eval(dymax2.get())
    dy[1] = eval(dymin2.get())
    if dx[0] < dx[1]:
        anti = True

    for y in np.arange(dy[1], dy[0], res / 50):
        if y > dy[0]:
            continue
        try:
            dx[0] = eval(dxmax2.get())
            dx[1] = eval(dxmin2.get())
        except:
            c.create_text(
                0,
                -y * 50 / zoom - error,
                text=f"ERROR in Y={y:.2f}",
                anchor=SE,
                fill="red",
            )
            errorFlag = True
            error += 10
            continue
        # for y in np.arange(dy[1],dy[0]+1,res/50):
        if dy[0] >= dy[1]:
            c.create_rectangle(
                (dx[1] * 50 / zoom),
                -y * 50 / zoom,
                (dx[0] * 50 / zoom),
                -y * 50 / zoom - 10 / zoom * res / 10,
                fill="white",
                outline="white",
            )
        else:
            anti = True
            c.create_rectangle(
                (dx[1] * 50 / zoom),
                -y * 50 / zoom,
                (dx[0] * 50 / zoom),
                -y * 50 / zoom - 10 / zoom * res / 10,
                fill="red",
                outline="white",
            )
        surface += res / 50 * ((dx[0]) - (dx[1]))

    for y in np.arange(int(dy[1]), int(dy[0]) + 1):
        c.create_text(0, -y * 50 / zoom, text=f"Y={int(y)}", anchor=SE, fill="red")

    c.create_line(-10000, 0, 10000, 0, fill="green")
    c.create_line(0, -10000, 0, 10000, fill="green")
    if errorFlag:
        messagebox.showerror(
            "Math Error",
            "В пределах интегрирования ошибки. \nНапример sqrt(-2) или деление на ноль",
            parent=window,
        )
    if anti:
        messagebox.showerror(
            "Math Error",
            "Верхний предел меньше нижнего!\nМожет, ты перепутал границы интегрирования?\n(красным выделена область с отрицательной плотность)",
            parent=window,
        )
    window.title(f"Примерная площадь:{surface:0.3f}")


def clickdxdy():
    window = Toplevel()
    surface = 0
    res = Scala.get()
    zoom = Scala2.get()

    try:
        dx.clear()
        dx.append(eval(dxmax1.get()))
        dx.append(eval(dxmin1.get()))
        dy.clear()
        dy.append(compile(dymax1.get(), "<string>", "exec"))
        dy.append(compile(dymax1.get(), "<string>", "exec"))
    except Exception as error:
        messagebox.showerror(
            "Error",
            f"В пределах интегрирования ошибки.\nНапример: неизвестные переменные или ошибки в формулах\n\nОшибка которая выводит сам Python:\n{error}",
        )
        return
    error = 0
    errorFlag = False
    anti = False
    frame = Frame(window, width=500, height=500)
    frame.pack(expand=True, fill=BOTH)
    h = ttk.Scrollbar(frame, orient=HORIZONTAL)
    v = ttk.Scrollbar(frame, orient=VERTICAL)
    c = Canvas(
        frame,
        scrollregion=(-500, -500, 500, 500),
        width=500,
        height=500,
        bg="black",
        yscrollcommand=v.set,
        xscrollcommand=h.set,
    )
    h.pack(side=BOTTOM, fill=X)
    v.pack(side=RIGHT, fill=Y)
    h["command"] = c.xview
    v["command"] = c.yview
    c.yview_moveto(0.25)
    c.xview_moveto(0.25)
    c.pack(side=LEFT, expand=True, fill=BOTH)

    dx[0] = eval(dxmax1.get())
    dx[1] = eval(dxmin1.get())
    if dx[0] < dx[1]:
        anti = True

    for x in np.arange(dx[1], dx[0], res / 50):
        if x > dx[0]:
            continue
        try:
            dy[0] = eval(dymax1.get())
            dy[1] = eval(dymin1.get())
        except:
            c.create_text(
                x * 50 / zoom, error, text=f"ERROR in X={x:.2f}", anchor=SE, fill="red"
            )
            errorFlag = True
            error += 10
            continue
        # for y in np.arange(dy[1],dy[0]+1,res/50):
        if dy[0] >= dy[1]:
            c.create_rectangle(
                x * 50 / zoom,
                -(dy[1] * 50 / zoom),
                x * 50 / zoom + 10 / zoom * res / 10,
                -(dy[0] * 50 / zoom),
                fill="white",
                outline="white",
            )
        else:
            anti = True
            c.create_rectangle(
                x * 50 / zoom,
                -(dy[1] * 50 / zoom),
                x * 50 / zoom + 10 / zoom * res / 10,
                -(dy[0] * 50 / zoom),
                fill="red",
                outline="red",
            )
        surface += res / 50 * ((dy[0]) - (dy[1]))

    for x in np.arange(int(dx[1]), int(dx[0]) + 1):
        c.create_text(x * 50 / zoom, 0, text=f"X={int(x)}", anchor=SE, fill="red")
    c.create_line(-10000, 0, 10000, 0, fill="green")
    c.create_line(0, -10000, 0, 10000, fill="green")
    window.title(f"Примерная площадь:{surface:0.3f}")
    if errorFlag:
        messagebox.showerror(
            "Math Error",
            "В пределах интегрирования ошибки. \nНапример sqrt(-2) или деление на ноль",
            parent=window,
        )
    if anti:
        messagebox.showerror(
            "Math Error",
            "Верхний предел меньше нижнего!\nМожет, ты перепутал границы интегрирования?\n(красным выделена область где перепутаны пределы)",
            parent=window,
        )


dxmax1 = ttk.Entry()
dxmax1.insert(0, "4")
dxmax1.grid(row=0, column=0)

dxmin1 = ttk.Entry()
dxmin1.insert(0, "-4")
dxmin1.grid(row=3, column=0)

dymax1 = ttk.Entry()
dymax1.insert(0, "sqrt(16-x**2)")
dymax1.grid(row=0, column=1)

dymin1 = ttk.Entry()
dymin1.insert(0, "-sqrt(16-x**2)")
dymin1.grid(row=3, column=1)


# label = ttk.Label(text="Разрешение",anchor="w", justify="left")
# label.grid(sticky="W",row=4,column=0)


Scala = Scale(
    from_=0.25, to=5, orient=HORIZONTAL, length=150, resolution=0.25, label="Разрешение"
)
Scala.grid(row=5, column=0)
Scala.set(3)
# label = ttk.Label(text="Маштаб",anchor="w", justify="left")
# label.grid(sticky="W",row=6,column=0)

Scala2 = Scale(
    from_=0.5, to=5, orient=HORIZONTAL, length=150, resolution=0.25, label="Маштаб"
)
Scala2.grid(row=5, column=1)
Scala2.set(1)

button = ttk.Button(text="Построить Интеграл Dx Dy", command=clickdxdy)
button.grid(row=8, column=0)

frame = Canvas(width=size[0], height=size[1])
frame.grid(row=1, column=0, columnspan=3)
frame.create_image(0, 0, anchor="nw", image=pimg)

dxmax2 = ttk.Entry()
dymin2 = ttk.Entry()
dymax2 = ttk.Entry()
dxmin2 = ttk.Entry()
dxmax2.insert(0, "sqrt(16-y**2)")
dymax2.grid(row=0, column=6)

dxmin2.insert(0, "-sqrt(16-y**2)")
dymin2.grid(row=3, column=6)

dymax2.insert(0, "2")
dxmax2.grid(row=0, column=8)

dymin2.insert(0, "-3")
dxmin2.grid(row=3, column=8)


# label = ttk.Label(text="Разрешение",anchor="w", justify="left")
# label.grid(sticky="W",row=4,column=0)
button = ttk.Button(text="Построить Интеграл Dy Dx", command=clickdydx)
button.grid(row=8, column=1)

img1 = Image.open("dydx.png").resize((300, 100))
pimg1 = ImageTk.PhotoImage(img1)
size1 = img.size
frame = Canvas(width=size[0], height=size[1])
frame.grid(row=1, column=6, columnspan=3)
frame.create_image(0, 0, anchor="nw", image=pimg1)

root.mainloop()
