import socket

HEADER_SIZE = 20 #contant size for the header

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket with IPV4 family, TCP 
s.bind((socket.gethostname(), 1234)) #bind socket to IP (my comp) and port (any 4 digits (?)
s.listen(5) #listen / wait for a connection. 

while True: #just wait...
    clientsocket, address = s.accept() #accept any incoming connections. addresss = where they connecting from
                                       #clientsocket is essentially just another socket
    print(f"Connection from {address} established!")

    msg = "Welcome to the server!" #message
    message = msg.encode("utf-8")
    header = f"{len(message) :< {HEADER_SIZE}}".encode("utf-8") #ensures that msg will be 20 characters

    clientsocket.send(header + message) #send as bytes to clientsocket