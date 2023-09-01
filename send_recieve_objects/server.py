import socket
import pickle

HEADER_SIZE = 20 #contant size for the header


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket with IPV4 family, TCP 
s.bind((socket.gethostname(), 1234)) #bind socket to IP (my comp) and port (any 4 digits (?)
s.listen(5) #listen / wait for a connection. 

while True: #just wait...
    clientsocket, address = s.accept() #accept any incoming connections. addresss = where they connecting from
                                       #clientsocket is essentially just another socket
    print(f"Connection from {address} established!")

    d = {1: "Hey", 2: "there"} #send this using pickle
    msg = pickle.dumps(d) 
    msg = bytes(f'{len(msg) :< {HEADER_SIZE}}', "utf-8") + msg #convert to bytes 

    clientsocket.send(msg) #send as bytes to clientsocket