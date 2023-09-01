import socket

HEADER_SIZE = 20 #contant size for the header. have for the client too 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket with IPV4 family, TCP 
s.connect((socket.gethostname(), 1234)) #connect instead of bind

#this will not server the connection after the initial message
while True: 
    full_msg = b"" #entire message from the server
    new_msg = True #keep track of recieving a new message
    while True: 
        msg = s.recv(16) #recieve part of message
        if new_msg: #if you get a new message, how big is it?
            print(f"New message length: {msg[:HEADER_SIZE]}")
            msglen = int(msg[:HEADER_SIZE].strip()) #convert from byte to string to int
            new_msg = False #read in the message already 
        full_msg += msg
        
        if len(full_msg) - HEADER_SIZE == msglen: #if this is true, the entire msg has been recieve
            print("Full message received")
            new_msg = True #accept new messages now
            full_msg = b"" #reset the message to hold new ones