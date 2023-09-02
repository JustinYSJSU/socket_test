import socket
import select
import errno
import sys

HEADER_LENGTH = 10
IP = "127.0.0.1" #local 
PORT = 1234 

my_username = input("Enter your username: ") #each user gets a name (could be duplicate right now)
print("Welcome! Right now, you'll have to hit 'enter' or send another message to update the chat")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False) #do not block other operations 

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

#Now in an infinite loop; send and recieve messages. you will have to hit "enter" to update the chat
while True:
    message = input(f"{my_username} > ") #will be like: username > <message here>
    
    if message: #message was not empty
        message = message.encode('utf-8')
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode('utf-8') #get the msg header 
        client_socket.send(message_header + message) #send the message 

    try: 
        while True: #receive other messages 
            username_header = client_socket.recv(HEADER_LENGTH) #get that user header
            if not len(username_header): #didn't get a header 
                print("connection closed")
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8') #get actual username 

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8') #get actual message 

            print(f"{username} > {message}")

    except IOError as e: #input / output error
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK: #don't want to handle if no more messages 
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error: ', str(e))
        sys.exit()