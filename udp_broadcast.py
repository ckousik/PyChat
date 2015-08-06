import socket, time,sys
from threading import Thread

class UDP_Broadcast(Thread):
    def __init__(self,PORT):
        self.PORT = PORT
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.init = False
        self.sock.bind((' ',self.PORT))
        self.sock.setblocking(0)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.Flag = True

    def run(self):
        while self.Flag:
            try:
                self.sock.sendto(''.encode(),('255.255.255.255',self.PORT))
            except Exception as e:
                print(e)
                self.join()
                break
        self.sock.shutdown(1)
        self.sock.close()

    def flipFlag(self):
        self.Flag = not self.Flag

try:
    udp = UDP_Broadcast(12345)
    udp.run()
except KeyboardInterrupt as e:
    print("Shutting down broadcast")
except Exception as e:
    print(e)
finally:
    sys.exit(0)
