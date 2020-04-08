import errno
import select
import socket

HEADER_LENGTH = 10 
IP = '127.0.0.1'
PORT = 1234

my_username  = input('Username: ')
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
# recieved fuctionality wont be blocking
client_socket.socket.setblocking(False)

username = my_username.encode('utf-8')
username_header =  f"{len(username):<{HEADER_LENGTH}}".encode('uft-8')
client_socket.send(username_header + username)
#  main loop for the client, which will be there to accept new messages from the client.
while True:
    # an input, but adding  username in there to give it a chat app feel
    #  before just sending the message, make sure that there is  one
    message = input(f'{my_username} > ')
    if message:

        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)