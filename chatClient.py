import sys, socket, threading

class reception(threading.Thread):
    def __init__(self, clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket

    def run(self):
        print(self.clientSocket.recv(1024).decode("Utf-8"))
        while 1:
            try:
                messg = self.clientSocket.recv(1024).decode("Utf-8")
                print(messg)
            except:
                break
        self.clientSocket.close()

class emmission(threading.Thread):
    def __init__(self, clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket

    def run(self):
        while 1:
            try:
                messg = input()
                self.clientSocket.send(messg.encode("Utf-8"))
                if messg.upper() == "END":
                    break
            except:
                break
        self.clientSocket.close()

host = '192.168.43.135'
port = 4000
lock = threading.Lock()

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    clientSocket.connect((host, port))
except:
    print(f"Failed to connect to {host}:{port}")
else:
    print(f"Connected to {host}:{port}")
    thR = reception(clientSocket)
    thE = emmission(clientSocket)
    thE.start()
    thR.start()
