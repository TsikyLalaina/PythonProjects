import sys, socket, threading, os

class clientHandle(threading.Thread):
    def __init__(self, clientId):
        threading.Thread.__init__(self)
        self.clientId = clientId

    def restorehistory(self, content, i, limit):
        self.clientId.send(content[i].encode("Utf-8"))
        if i != limit:
            t = threading.Timer(2e-2, lambda a = 0 : self.restorehistory(content, i + 1, limit))
            t.start()

    def run(self):
        self.clientId.send("Server> You can chat now".encode("Utf-8"))
        if os.path.exists("chatlog.txt"):
            file = open("chatlog.txt", "r")
            content = file.read()
            if content != "":
                content = content.split("\n")
                t = threading.Timer(1e-10, lambda a = 0: th.restorehistory(content, a, len(content) - 1))
                t.start ()
        file.close()
        self.broadcast(f"Server> {surname[self.name]} has joined the chat.")
        while 1:
            messg = self.clientId.recv(1024).decode("Utf-8")
            if messg.upper() != "END":
                if messg.upper() == "ENDF":
                    messg = messg[:len(messg) - 1]
                if messg[:6] == "$NAME:":
                    handlename(self, self.clientId, messg[6:])
                    continue
                self.broadcast(f"{surname[self.name]}> {messg}")
            else:
                self.clientId.send("END".encode("Utf-8"))
                break
        self.broadcast(f"Server> {surname[self.name]} has left the chat.")
        lock.acquire()
        del client[self.name]
        del surname[self.name]
        lock.release()
        self.clientId.close()

    def broadcast(self, messg):
        file = open("chatlog.txt", "a")
        file.write(messg + '\n')
        file.close()
        print(messg)
        for i in client:
            if i != self.name:
                client[i].send(messg.encode("Utf-8"))

def handlename(th, clientId, name):
    exist  = False
    first = True
    for i in surname:
        if surname[i] == name:
            exist = True
    if not exist:
        if th.name in surname:
            first = False
            oldname = surname[th.name]
        if name == "":
            name = th.name
        surname[th.name] = name
        print(th.name, "has changed his name to ", name)
        if not first:
            th.broadcast(f"{oldname} has changed his name to {name}")
            clientId.send(f"Server> You have changed your name to {name}".encode("Utf-8"))
    else:
        print("Failed changing the name of ", th.name, "to ", name)

host = '192.168.43.135'
port = 4000
client = {}
surname = {}
if not os.path.exists("chatlog.txt"):
    file = open("chatlog.txt", "w")
    file.close()
lock = threading.Lock()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind((host, port))
    server.listen(5)
except:
    server.close()
    print(f"Error connecting to the address {host}:{port}")
else:
    print(f"Server is listening on {host}:{port}. Waiting for request...")
    while 1:
        clientId, address = server.accept()
        th = clientHandle(clientId)
        name = clientId.recv(50).decode("Utf-8")
        handlename(th, clientId, name[6:])
        th.start()
        lock.acquire()
        client[th.name] = clientId
        lock.release()
        print(f"{th.name} connected to {address[0]}:{address[1]}")