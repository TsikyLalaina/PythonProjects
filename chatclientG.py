from tkinter import *
from chatInterface import chatInterface
import sys, socket, threading, os

window = Tk()
frame = Frame(window)
frame.pack()

can = Canvas(frame, width = 510, height = 500, bg = "#151f17", scrollregion=(0, 0, 500, 500))

vbar = Scrollbar(frame, orient = "vertical", command = can.yview)
vbar.pack(side="right", fill="y")
can.config(yscrollcommand = vbar.set)

host = '192.168.43.135'
port = 4000
lock = threading.Lock()

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chat = chatInterface(window, can, clientSocket)
can.pack(side = "top")
try:
    clientSocket.connect((host, port))
except:
    print(f"Failed to connect to {host}:{port}")
else:
    print(f"Connected to {host}:{port}")
    chat.getname()
    chat.start()
    window.mainloop()