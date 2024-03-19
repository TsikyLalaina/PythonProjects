from tkinter import *
from TkinterMeth import draw
from math import sin, pi

class oscillo:
    def __init__(self, amplitude, frequency, phase = 0):
        self.amplitude, self.frequency, self.phase = amplitude, frequency, phase
        self.window1 = Tk()
        self.can1 = Canvas(self.window1, bg = "white", width = 1000, height = 500)
        self.can1.grid(row = 0, columnspan = 4)
        self.chk = BooleanVar(); 

    def createplan(self):
        make = draw(self.can1, [1000, 500])
        make.rectangle(40, 10, 950, 480, col1 = "black")
        amplitude = (make.dimensions[1] - 60) / (abs(self.amplitude) * 2 + 1)
        if amplitude >= 10:
            self.originy = 20 + ((abs(self.amplitude) + 1) * amplitude)
            self.can1.create_line(40, 20 + ((abs(self.amplitude) + 1) * amplitude), 990, 20 + ((abs(self.amplitude) + 1) * amplitude))
            for i in range(0, abs(self.amplitude) + 1):
                self.can1.create_text(20, 20 + ((abs(self.amplitude) + 1) * amplitude - amplitude * i), anchor = CENTER, text = str(i))
            for i in range(0, abs(self.amplitude)):
                self.can1.create_text(18, 20 + ((abs(self.amplitude) * 2 + 1) * amplitude - amplitude * i), anchor = CENTER, text = str(- (abs(self.amplitude) - i)))
            self.unit = amplitude
        else:
            j = 1
            while (make.dimensions[1] - 70) / ((abs(self.amplitude) * 2 + 1) // j) < 14:
                j += 1
            nbrclass = (abs(self.amplitude) * 2 + 1) // j
            realampl = j
            temp1 = []
            for i in range(0, ((nbrclass * j) // 2) + j, j):
                temp1.append(i)
            amplitude = (make.dimensions[1] - 70) / (len(temp1) * 2)
            self.originy = 20 + ((len(temp1) + 1) * amplitude)
            self.can1.create_line(40, 20 + ((len(temp1) + 1) * amplitude), 990, 20 + ((len(temp1) + 1) * amplitude))
            j = 0
            for i in temp1:
                self.can1.create_text(10, 20 + ((len(temp1) + 1) * amplitude - amplitude * j), anchor = CENTER, text = str(i))
                j += 1
            j = 0
            for i in temp1:
                if j != len(temp1) - 1:
                    self.can1.create_text(10, 20 + ((len(temp1) * 2 + 1) * amplitude - amplitude * (j + 1)), anchor = CENTER, text = str(-temp1[len(temp1) - 1 - j]))
                j += 1
            self.unit = amplitude / realampl

    def createcurve(self, amplitude, frequency, color = "red", phase = 0):
        t = 0
        while t < 951:
            et = float(amplitude) * sin(2 * pi * float(frequency) * 0.001 * t + (float(self.phase) * pi) / 180)#tokony atao e-3 foana ny frequence
            self.can1.create_line(40 + t, self.originy + et * self.unit, 41 + t, self.originy + et * self.unit, fill = color)
            t += 0.1#reduire pour grossir le courbe quand la frequence diminue

    def createcurvedefault(self):
        t = 0
        self.defalines = []
        while t < 950:
            et = float(self.amplitude) * sin(2 * pi * float(self.frequency) * 0.001 * t + (float(self.phase) * pi) / 180)#tokony atao e-3 foana ny frequence
            if self.chk.get():
                self.defalines.append(self.can1.create_line(40 + t, self.originy + et * self.unit, 41 + t, self.originy + et * self.unit))
            t += 0.1#reduire pour grossir le courbe quand la frequence diminue

    def newdefacurvefreq(self, newfreq):
        t = 0
        for line in self.defalines:
            et = float(self.amplitude) * sin(2 * pi * float(newfreq) * 0.001 * t + (float(self.phase) * pi) / 180)#tokony atao e-3 foana ny frequence
            if self.chk.get():
                self.can1.coords(line, 40 + t, self.originy + et * self.unit, 41 + t, self.originy + et * self.unit)
            t += 0.1#reduire pour grossir le courbe quand la frequence diminue
        self.frequency = newfreq

    def newdefacurveampl(self, newampl):
        t = 0
        for line in self.defalines:
            et = float(newampl) * sin(2 * pi * float(self.frequency) * 0.001 * t + (float(self.phase) * pi) / 180)#tokony atao e-3 foana ny frequence
            if self.chk.get():
                self.can1.coords(line, 40 + t, self.originy + et * self.unit, 41 + t, self.originy + et * self.unit)
            t += 0.1#reduire pour grossir le courbe quand la frequence diminue
        self.amplitude = newampl

    def newdefacurvepha(self, newpha):
        t = 0
        for line in self.defalines:
            et = float(self.amplitude) * sin(2 * pi * float(self.frequency) * 0.001 * t + (float(newpha) * pi) / 180)#tokony atao e-3 foana ny frequence
            if self.chk.get():
                self.can1.coords(line, 40 + t, self.originy + et * self.unit, 41 + t, self.originy + et * self.unit)
            t += 0.1#reduire pour grossir le courbe quand la frequence diminue
        self.phase = newpha

    def displaydefacurve(self):
        if not self.chk.get():
            for line in self.defalines:
                self.can1.delete(line)
        else:
            self.createcurvedefault()

    def createscale(self):   # 'objet-variable' tkinter	    
        Checkbutton(self.window1, variable = self.chk, text ='Display', command = self.displaydefacurve).grid(row =  1, column = 0)
        Scale(self.window1, length=250, orient=HORIZONTAL, label ='frequency(Hz):', showvalue= 0,
            troughcolor ='dark grey', sliderlength =20, from_= -20, to=20, tickinterval = 5,
            command = self.newdefacurvefreq).grid(row = 1, column = 1)
        Scale(self.window1, length=250, orient=HORIZONTAL, label ='amplitude(meter):',
            troughcolor ='dark grey', sliderlength =20, from_=-abs(self.amplitude), to=abs(self.amplitude), tickinterval = 5, showvalue= 0,
            command = self.newdefacurveampl).grid(row = 1, column = 2)
        Scale(self.window1, length=250, orient=HORIZONTAL, label ='phase(degree):',
            troughcolor ='dark grey', sliderlength =20, from_= 0, to = 360, tickinterval = 45, showvalue= 0,
            command = self.newdefacurvepha).grid(row = 1, column = 3)

if __name__ == '__main__':
    objet = oscillo(-10, 0)
    objet.createplan()
    objet.createcurvedefault()
    objet.createscale()
    objet.window1.mainloop()