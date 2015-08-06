import socket
from threading import Thread
import time

class UDPBroadcastReciever(Thread):
    def __init__(self,PORT):
        try:
            self.PORT = PORT
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #UDP
            self.sock.setblocking(0) #Non blocking socket
            self.sock.bind((socket.gethostbyname(socket.gethostname()),PORT))
        except Exception as e:
            print(e)
            del self

    def run(self):
        while True:
            try:
                data = self.sock.recvfrom(1024)
                print(data[1])
                time.sleep(10)
            except Exception as e:
                print(e)
                break

b = UDPBroadcastReciever(12345)
b.run()
