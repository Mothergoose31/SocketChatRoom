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