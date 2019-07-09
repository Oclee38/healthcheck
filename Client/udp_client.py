import socket
import pickle
import sys
import json


UDP_IP_ADDRESS = '127.0.0.1'
UDP_PORT = 6698
message = 'DIR_INFO'

if len(sys.argv) > 1:
    UDP_IP_ADDRESS = sys.argv[1]
    UDP_PORT = int(sys.argv[2])
    message = sys.argv[3]

buffer_size = 2048


bytes_to_send = str.encode(message)

client_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_Socket.sendto(bytes_to_send, (UDP_IP_ADDRESS, UDP_PORT))
buffer_size = client_Socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)

data, addr = client_Socket.recvfrom(buffer_size)

message = pickle.loads(data)

try:
    for msg in message:
        print(msg)
except Exception as ex:
    print(message)
    print(ex)


# print(message)
