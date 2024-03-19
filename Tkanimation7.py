from tkinter import *
from TkinterMeth import draw
from tkinter import ttk
from math import log2, ceil
from random import randrange, random
from StringMeth import isin

class statistic:#I still have to use another method if the data are not all integer
    def __init__(self, data = []):
        self.data = data
        self.table = []
        self.nbrclass = 0
        self.amplitude = 0
        self.classes = []#[[limite infer, limite sup, centre de classe, effectif]]
        self.window = Tk()

    def sortdata(self):#Hafaka tonga de intervalle no omena, de eo am zay no mampiasa an le formula-na hauteur iny rehefa tsy mitovy le amplitude
        self.data.sort()
        for i in self.data:
            if not([i, self.data.count(i)] in self.table):
                self.table.append([i, self.data.count(i)])#[value, effectif]

    def initvar(self):
        self.nbrclass = int(log2(len(self.table)) + 1)
        self.amplitude = ceil((max(self.data) - min(self.data)) / self.nbrclass)#only works if all the data are integer

    def createclass(self):
        minlim = self.table[0][0]
        for i in range(0, self.nbrclass):
            self.classes.append([minlim, minlim + self.amplitude, 0, 0])
            minlim += self.amplitude
        j = 0
        for i in self.classes:
            self.classes[j][2] = (i[0] + i[1]) / 2
            j += 1

    def classlen(self):#effectif des intervales
        for i in self.table:
            t = 0
            for j in self.classes:
                if j[0] <= i[0]  <= j[1]:
                    self.classes[t][3] += i[1]
                t += 1

    def graph1(self):
        tree = ttk.Treeview(self.window)
        tree["columns"] = ("one", "two", "three")

        tree.column("one", width=100, anchor="center")
        tree.column("two", width=100, anchor="center")
        tree.column("three", width=100, anchor="center")

        tree.heading("one", text="Classes")
        tree.heading("two", text="Centre de classes")
        tree.heading("three", text="Effectifs")

        j = 0
        for i in self.classes:
            tree.insert("", j, text = str(j + 1), values = ("[{:.4f};{:4f}[".format(i[0], i[1]), i[2], i[3]))
            j += 1

        tree.pack()

    def graph2(self):
        tree = ttk.Treeview(self.window)
        tree["columns"] = ("one", "two")

        tree.column("one", width=100, anchor="center")
        tree.column("two", width=100, anchor="center")

        tree.heading("one", text="Classes")
        tree.heading("two", text="Effectifs")

        j = 0
        for i in self.table:
            tree.insert("", j, text = str(j + 1), values = (i[0], i[1]))
            j += 1

        tree.pack()
        
    def creategraph1(self):
        can1 = Canvas(self.window, width = 1000, height = 450, bg = "white")
        can1.pack()
        make = draw(can1, dimensions = [1000, 450])
        make.rectangle(40, 10, make.dimensions[0] -  80, make.dimensions[1] - 50, col1 = "black")
        amplitude = (make.dimensions[0] - 60) / (self.nbrclass + 1)
        amplx = amplitude
        j = 0
        for i in self.classes:
            can1.create_text(60 + j * amplitude, make.dimensions[1] - 25, anchor = CENTER, text = "{:.3f}".format(i[0]))
            if j == len(self.classes) - 1:
                can1.create_text(60 + (j + 1) * amplitude, make.dimensions[1] - 25, anchor =CENTER, text = "{:.3f}".format(i[1]))
            j += 1
        temp1 = []
        for i in self.classes:
            temp1.append(i[3])
        amplitude = (make.dimensions[1] - 60) / (max(temp1) + 1)
        if amplitude >= 10:
            for i in range(0, max(temp1) + 1):
                can1.create_text(20, 20 + ((max(temp1) + 1) * amplitude - amplitude * i), anchor = CENTER, text = str(i))
            unit = amplitude
        else:
            j = 1
            while (make.dimensions[1] - 70) / ((max(temp1) + 1) // j) < 14:
                j += 1
            nbrclass = (max(temp1) + 1) // j
            realampl = j
            temp1 = []
            for i in range(0, (nbrclass + 1) * j + 1, j):
                temp1.append(i)
            amplitude = (make.dimensions[1] - 70) / len(temp1)
            j = 0
            for i in temp1:
                can1.create_text(20, 20 + ((len(temp1) + 1) * amplitude - amplitude * j), anchor = CENTER, text = str(i))
                j += 1
            unit = amplitude / realampl
        j = 0
        for i in self.classes:
            make.rectangle(60 + j * amplx, make.dimensions[1] - 40 - unit * i[3], amplx, unit * i[3], col2 = "red", col1 = "black")
            j += 1

    def creategraph2(self):
        can1 = Canvas(self.window, width = 1000, height = 450, bg = "white")
        can1.pack()
        make = draw(can1, dimensions = [1000, 450])
        make.rectangle(40, 10, make.dimensions[0] -  80, make.dimensions[1] - 50, col1 = "black")
        amplitude = (make.dimensions[0] - 60) / len(self.table)
        amplx = amplitude
        j = 0
        for i in self.table:
            can1.create_text(60 + j * amplitude, make.dimensions[1] - 25, anchor = CENTER, text = i[0])
            j += 1
        temp1 = []
        for i in self.table:
            temp1.append(i[1])
        amplitude = (make.dimensions[1] - 60) / (max(temp1) + 1)
        if amplitude >= 10:
            for i in range(0, max(temp1) + 1):
                can1.create_text(20, 20 + ((max(temp1) + 1) * amplitude - amplitude * i), anchor = CENTER, text = str(i))
            unit = amplitude
        else:
            j = 1
            while (make.dimensions[1] - 70) / ((max(temp1) + 1) // j) < 14:
                j += 1
            nbrclass = (max(temp1) + 1) // j
            realampl = j
            temp1 = []
            for i in range(0, (nbrclass + 1) * j + 1, j):
                temp1.append(i)
            amplitude = (make.dimensions[1] - 70) / len(temp1)
            j = 0
            for i in temp1:
                can1.create_text(20, 20 + ((len(temp1) + 1) * amplitude - amplitude * j), anchor = CENTER, text = str(i))
                j += 1
            unit = amplitude / realampl
        j = 0
        for i in self.table:
            make.rectangle(60 + j * amplx, make.dimensions[1] - 40 - unit * i[1], amplx / 4, unit * i[1], col2 = "red", col1 = "black")
            j += 1

#data = [15,1,2,3,4,5,6,7,15,6,17,17,17]
#palet = ["rouge", "blanc", "noir", "jaune", "orange", "vert", "bleu", "violet", "gris", "noir", "blanc", "grenad", "beige"]
data =  []
for i in range(0,300):
    data.append(random()*100)
"""for i in range(0, 3000):
    data.append(palet[randrange(0, len(palet))])"""
stat = statistic(data)
print("Initialising...")
stat.sortdata()
print("Sorting data...")
stat.initvar()
print("Initialising variables...")
stat.createclass()
print("Creating classes...")
stat.classlen()
print("Initialising classes...")
print("Sorted datas:",stat.table)
print("Number of class:", stat.nbrclass)
print("Amplitude:",stat.amplitude)
print("Classes:",stat.classes)
stat.graph1()
print("Displaying datas...")
stat.creategraph1()
print("Createing plan...")
print("Displaying plan...")
print("Creating histogram...")
print("Displaying histogram...")
stat.window.mainloop()
print("Finished")