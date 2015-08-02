import socket,sys,time

#SERVER_IP = input('Server local ip')
#PORT=input('Server port')
SERVER_IP='192.168.56.1'
PORT=3000
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    print("Connecting to %s:%d"%(SERVER_IP,PORT))
    s.connect((SERVER_IP,int(PORT)))
    exit_code = "-qc"
    time.sleep(10)
    s.sendall(exit_code.encode())
    s.close()
except socket.error as msg:
    print(msg)
