'''
Author: Chinmay Jayaram Kousik
SRM University

Description: PyChat is a simple socket based chat
application to communicate on a network.
'''

import socket
import signal,time
from threading import Thread,Lock

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
port = 3000
clients = {}
threadCount=0
clientThreads={}
s.bind((host, port))
try:
    s.listen(1)
except OSError:
    print("Error...operation not supported")
#Thread class to handle client activity
class ClientHandler(Thread):
    def __init__(self,c,addr):
        global clients,clientThreads,threadCount
        self.c=c
        self.addr=addr
        self.lock=Lock()
        self.lock.acquire()
        clients[str(addr)]=c
        clientThreads[str(addr)]=self
        threadCount=threadCount+1
        self.lock.release()
        Thread.__init__(self)
        print("Thread running for",self.addr)

    def run(self):
        global clients
        while True:
#Recieve data from the client
            req=str(self.c.recv(1024).decode())
            print(req)
            #Mechanism to safely quit
            if(req=='-qc'):
                print(self.addr,"disconnecting")
                self.join()

            time.sleep(2)
#Handle requests from clients on the network
            if(req[0:2]=="-sm"):
                rec,msg=rec[3:].split("<||")
                try:
                    self.lock.acquire()

                    target = clients[rec]
                    print(self.addr,">>",msg,">>",rec)
                    self.c.send("Message recieved on server")
                    target.send(str(self.addr)+msg)

                    self.lock.release()

                except KeyError as e:
                    print("Invalid recipient by",self.addr)
                    self.c.send("Invalid recipient",rec)

            if(req=="-lo"):
                self.lock.acquire()
                online = ""
                for i in clients.keys:
                    online=online+i
                self.lock.release()
                self.c.send(online)

    def join(self):
        global clients,clientThreads,threadCount
        try:
            self.lock.acquire()
            clients.pop(str(self.addr))
            threadCount=threadCount-1
            clientThreads.pop(str(self.addr))
            print("Thread handling address",self.addr,"was joined")
            print(threadCount,"threads currently active")
            self.lock.release()

        except KeyError as e:
            print(e.args[0])
        finally:
            try:
                Thread.join(self)
            except Exception as e :
                print(e.args)

#End of ClientHandler
#Interrupt handler
def sigint_handler(signum,frame):
    raise KeyboardInterrupt()

signal.signal(signal.SIGINT,sigint_handler)

#Server code
try:
    print("Server started on",host,":",port)
    while True:
        ct=None
        c,addr=s.accept()
        print("Connection from",addr)
        ct = ClientHandler(c,addr)
        ct.start()
except (KeyboardInterrupt,SystemExit):
    print("Process has been stopped")
finally:
    print("Closing server...")
    print("Joining threads")
    for i in clientThreads.values():
        i.join()
    print("All threads successfully joined")
    s.close()
