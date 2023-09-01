import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket with IPV4 family, TCP 
s.connect((socket.gethostname(), 1234)) #connect instead of bind

msg = s.recv(1024) #recieve the data flow from TCP. recieve as bytes
print(msg.decode("utf-8")) #decode the utf-8 from server.py