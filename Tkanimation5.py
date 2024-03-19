from tkinter import *
from math import pi, cos, sin
from datetime import datetime

window1 = Tk()
dimension = 500
can1 = Canvas(window1, width = dimension, height = dimension, bg = "white")
can1.pack()
long = 3 * (dimension / 2) / 4
larg = dimension / 100
o = dimension / 2

can1.create_oval(o - (long + 30), o - (long + 30), o + (long + 30), o + (long + 30), outline = "black", fill = "gray", width = 4)

for l in range(0, 360, 30):
    can1.create_line(o + cos(l / 180 * pi) * (long + 5), o + sin(l / 180 * pi) * (long + 5), o + cos(l / 180 * pi) * (long + 30), o + sin(l / 180 * pi) * (long + 30), width = 10)
second = can1.create_polygon(0,0,0,0,0,0,0,0, fill = "red", outline = "red")
minute = can1.create_polygon(0,0,0,0,0,0,0,0, fill = "black", outline = "black")
hour = can1.create_polygon(0,0,0,0,0,0,0,0, fill = "black", outline = "black")

can1.create_oval(o - (larg + 5), o - (larg + 5), o + (larg + 5), o + (larg + 5), outline = "black", fill = "white")


def movesecond():
    myobj = datetime.now()
    i = -myobj.second * 6 - 180
    j = -myobj.minute * 6 - 180
    k = -((myobj.hour % 12) * 360 / 12) - 180
    a1x = o + cos(i / 180 * pi) * larg / 2
    a1y = o - sin(i / 180 * pi) * larg / 2
    a2x = a1x + long * cos(90 / 180 * pi - i / 180 * pi)
    a2y = a1y + long * sin(90 / 180 * pi - i / 180 * pi)
    a4x = o - cos(i / 180 * pi) * larg / 2
    a4y = o + sin(i / 180 * pi) * larg / 2
    point = [a1x, a1y, a2x, a2y, a2x - (a1x - a4x), a2y + (a4y - a1y), a4x, a4y]
    can1.coords(second, point)
    movehour(k)
    moveminute(j)
    window1.after(1000, movesecond)

def moveminute(j):
    a1x = o + cos(j / 180 * pi) * (larg + 5) / 2
    a1y = o - sin(j / 180 * pi) * (larg + 5) / 2
    a2x = a1x + long * cos(90 / 180 * pi - j / 180 * pi)
    a2y = a1y + long * sin(90 / 180 * pi - j / 180 * pi)
    a4x = o - cos(j / 180 * pi) * (larg + 5) / 2
    a4y = o + sin(j / 180 * pi) * (larg + 5) / 2
    point = [a1x, a1y, a2x, a2y, a2x - (a1x - a4x), a2y + (a4y - a1y), a4x, a4y]
    can1.coords(minute, point)

def movehour(k):
    a1x = o + cos(k / 180 * pi) * (larg + 5) / 2
    a1y = o - sin(k / 180 * pi) * (larg + 5) / 2
    a2x = a1x + (long - 50) * cos(90 / 180 * pi - k / 180 * pi)
    a2y = a1y + (long - 50) * sin(90 / 180 * pi - k / 180 * pi)
    a4x = o - cos(k / 180 * pi) * (larg + 5) / 2
    a4y = o + sin(k / 180 * pi) * (larg + 5) / 2
    point = [a1x, a1y, a2x, a2y, a2x - (a1x - a4x), a2y + (a4y - a1y), a4x, a4y]
    can1.coords(hour, point)


movesecond()


mainloop()