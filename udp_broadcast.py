import socket
from threading import Thread

class UDP_Broadcast(Thread):
    def __init__(self,SERVER_IP,PORT):
        self.IP = SERVER_IP
        self.PORT = PORT
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.init = False

    def run(self):
        broadcast_data = str(self.IP)+str(self.PORT)
        while True:
            try:
                sock.sendto(broadcast_data.encode(),('255.255.255.255',self.PORT))
            except Exception as e:
                print(e)
                self.join()

    def join(self):
        try:
            sock.shutdown(1)
            sock.close()
            Thread().join()
        except:
            print("Could not join broadcast thread...killing thread...")
            self.stop()

    def stop(self):
        try:
            sock.close()
        except:
            print("Error closing socket...")
        finally:
            Thread().stop()
