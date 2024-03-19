from tkinter import *
import sys, socket, threading
from tkinter import messagebox

class chatInterface(threading.Thread):
    def __init__(self, win, can1, clientSocket):
        threading.Thread.__init__(self)
        self.can1 = can1
        self.win = win
        self.text = Text(self.win, width = 50, height = 3)
        self.text.pack(side = "left")
        self.makespace = 0
        self.text.bind("<Key>", self.validate_text)
        self.clientSocket = clientSocket
        self.end = False
        Button(self.win, text = "STOP", width =  6, height = 3, command = self.endsession).pack(side = "left", padx = 5)
        self.win.protocol("WM_DELETE_WINDOW", self.endsession)
        Button(self.win, text = "NAME", width = 6, height = 3,  command = self.getname).pack(side = "left")

    def endsession(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.end = True
            self.clientSocket.send("END".encode("Utf-8"))
            self.win.destroy()

    def validatename(self, en, win):
        name = en.get()
        self.clientSocket.send(("$NAME:" + name).encode("Utf-8"))
        win.destroy()

    def getname(self):
        win = Toplevel(self.win)
        win.attributes("-topmost", True)
        win.grab_set()
        Label(win, text = "Enter your name: ").grid(row = 0, column = 0)
        en = Entry(win, width = 50)
        en.grid(row = 0, columnspan = 2)
        bu = Button(win, text = "OK", width = 20, height = 2, command = lambda en = en, win = win : self.validatename(en, win))
        bu.grid(row = 1, columnspan = 2)
        win.protocol("WM_DELETE_WINDOW", lambda event : bu.invoke())
        en.bind("<Return>", lambda event : bu.invoke())

    def run(self):
        while 1:
            try:
                messg = self.clientSocket.recv(1024).decode("Utf-8")
                if self.end and  messg.upper() == "END":
                    break
                self.recievemessg(messg)
            except:
                break
        self.clientSocket.close()

    def sendmessg(self, mssg):
        try:
            self.clientSocket.send(mssg.encode("Utf-8"))
        except:
            print("Failed to send the message.")
        else:
            text = self.can1.create_text(0, 0, width = 200, anchor = "nw", text = mssg, font = "arial 11", fill = "white")
            x0, y0, x1, y1 = self.can1.bbox(text)
            self.bubble(x = self.can1.winfo_reqwidth() - (x1 - x0) - 50, y = self.makespace, long = x1 - x0, larg = y1 - y0, col =  "#0e72ff")
            self.can1.lift(text)
            self.can1.move(text, self.can1.winfo_reqwidth() - (x1 - x0) - 50, self.makespace)
            self.makespace += (y1 - y0) + 30
            self.can1.configure(scrollregion = self.can1.bbox("all"))
            self.can1.yview_moveto(1)

    def recievemessg(self, mssg):
        text = self.can1.create_text(0, 0, width = 200, anchor = "nw", text = mssg, font = "arial 11", fill = "white")
        x0, y0, x1, y1 = self.can1.bbox(text)
        self.bubble(x = 50, y = self.makespace, long = x1 - x0, larg = y1 - y0, col =  "#787878")
        self.can1.lift(text)
        self.can1.move(text, 50, self.makespace)
        self.makespace += (y1 - y0) + 30
        self.can1.configure(scrollregion = self.can1.bbox("all"))
        self.can1.yview_moveto(1)

    def validate_text(self, event):
        text_content = self.text.get("1.0", "end-1c")
        if event.keysym == "Return":
            self.text.delete("1.0", "end")
            if text_content.upper() == "END":
                text_content += "F"
            self.sendmessg(text_content)
            return "break"
        elif len(text_content) >= 150 and event.keysym != "BackSpace":
            return "break"

    def bubble(self, x, y, long, larg, col):
        coo = [x , y - 10, x + long, y + larg + 10]
        self.can1.create_rectangle(coo, fill = col, width = 0)
        self.can1.create_arc(coo[0] - 2 * long / 9, coo[1], coo[0] + 2 * long / 9, coo[3] - 1, fill = col, start = 90, extent = 180, width = 0, outline = col)
        self.can1.create_arc(coo[2] - 2 * long / 9, coo[1], coo[2] + 2 * long / 9, coo[3] - 1, fill = col, start = -90, extent = 180, width = 0, outline = col)
