import socket
# select is used because it's used to manage many connections , reguardless 
# of  the os linux/ windows / macm it will all work 
import select

HEADER_LENGTH = 10 
IP = '127.0.0.1'
PORT = 1234

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#  so that  when you are playing with sockets  it will not respond with "adress is  already in use 
# and you have to keep ticking up the adress"
# When retrieving a socket option, or setting it, you specify the option name as well as the level. 
# When level = SOL_SOCKET,
#  the item will be searched for in the socket itself.
# https://pubs.opengroup.org/onlinepubs/7908799/xns/getsockopt.html

# setsockopt(mysocket, SOL_SOCKET, SO_REUSEADDR, &value, sizeof(value));
# This will set the SO_REUSEADDR in my socket to 1.
server_socket.setsockopt(socket.SOL_SOCKET,socket.SOL_REUSEADRR,1)

server_socket.bind((IP, PORT))

server_socket.listen()
socket_list = [server_socket]

clients = {}


def recieve_message(client_socket):
    try:
        message_header =client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            # if we don't get any data the client closes the connection
            return False
            message_legth = int(message_header.decode("utf-8").strip())
            return {'header':message_header,'data':client_socket.socket.recv(message_legth)}

    except:
        return False

while True:
#                                                  sockets that we are going read| write | or error on
    read_sockets, _, exeption_sockets = select.select(socket_list, [],  socket_list)
    for notified_socket in read_sockets:
        # this means that someone just conected and we have to accept the  connection and also handle for for 
        if notified_socket == server_socket:
            client_socket,client_address = server_socket.accept()

            user = recieve_message(client_socket)

            if user is False:
                continue
            socket_list.append(client_socket)

            clients[client_socket] = user 

            print(f'accepted new connection from {client_address[0]}:{client_address[1]}')

        else:
            message = recieve_message(notified_socket)

            if message is False:
                print('Clossed connection')
                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user =clients[notified_socket]
            print(f'recieved message {user['data'].decode('utf-8')}:{message['data'].decode('utf-8')}')

            for client_socket in clients:
                if client_socket !=notified_socket:
                    client_socket.send(user['header'] + user['data']+ message['header'] + message['data'])
    for notified_socket in exeption_sockets:
        socket_list.remove(notified_socket)
        del clients[notified_socket]                    



