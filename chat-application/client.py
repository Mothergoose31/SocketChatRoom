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

        #  a while True loop that will infinitely attempt to receive any incoming messages. Once 
        # there are no more to receive, we will get an error. We'll handle for other expected errors,
        #  but if we get the specific error we're 
        # expecting to just be out of messages, then break the loop cleanly and repeat.
        while True:

            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server closes a connection, for example
            #  using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()
                # get the username
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')
            # get the message
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            # output to the screen
            print(f'{username} > {message}')
        #  to do add error handling with  errno