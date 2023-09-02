import socket
import select 

HEADER_LENGTH = 10
IP = "127.0.0.1" #local 
PORT = 1234 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket 
server_socket.bind((IP, PORT)) #bind socket to my computer, port 1234 
server_socket.listen() #wait for connections...

sockets_list = [server_socket] #hold all sockets, including new client ones
clients = {} #dictionary of all clients. key = socket, value = user data


#receiving any messages from client
def recieve_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH) #get header
        if not len(message_header): #didn't recieve anything
          return False
        
        message_length = int(message_header.decode("utf-8").strip()) #strip the header
        return {"header": message_header, "data": client_socket.recv(message_length)} #header + message itself
    
    except:
        return False
    
    
while True:
    read_sockets, _, exception_socket = select.select(sockets_list, [], sockets_list) #sockets to read, sockets to write, and error sockets. read is the most important one

    for notified_socket in read_sockets:
        if notified_socket == server_socket: #somebody connected
            client_socket, client_address = server_socket.accept()
            user = recieve_message(client_socket)

            if user is False: #connection lost for the user, just ignore it
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user #in client dictionary, enter the socket, header / data for the new user 

            print(f"New connection from {client_address[0]} : {client_address[1]} username:{user['data'].decode('utf-8')}")

        else: #if they didn't just connect, a message has probably been sent instead 
            message = recieve_message(notified_socket)
            if message is False:  #no message somehow
                print(f"Closed connection")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user = clients[notified_socket] #get the user
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
            #print user / msg to the server

            for client_socket in clients: #displaying message to all the clients connected 
                if client_socket != notified_socket: #not sending message to the person who sent it 
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data']) #send to all other clients 