import sys, socket, threading

class clientHandle(threading.Thread):
    def __init__(self, clientId):
        threading.Thread.__init__(self)
        self.clientId = clientId

    def run(self):
        self.clientId.send("Server> You can chat now. Enter END to leave the chat.".encode("Utf-8"))
        self.broadcast(f"Server> {self.name} has joined the chat.")
        while 1:
            messg = self.clientId.recv(1024).decode("Utf-8")
            if messg.upper() != "END":
                self.broadcast(f"{self.name}> {messg}")
            else:
                break
        self.broadcast(f"Server> {self.name} has left the chat.")
        lock.acquire()
        del client[self.name]
        lock.release()
        self.clientId.close()

    def broadcast(self, messg):
        print(messg)
        for i in client:
            if i != self.name:
                client[i].send(messg.encode("Utf-8"))

host = '192.168.43.135'
port = 4000
client = {}
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
        th.start()
        lock.acquire()
        client[th.name] = clientId
        lock.release()
        print(f"{th.name} connected to {address[0]}:{address[1]}")