#!/usr/bin python3

import socket
import healthcheck
import pickle


UDP_IP_ADDRESS = '0.0.0.0'
UDP_PORT = 6698
buffer_size = 2048

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((UDP_IP_ADDRESS, UDP_PORT))

print('Server is listening')

while True:

    data, addr = server_socket.recvfrom(1024)
    message = str(data, 'utf-8')
    client_ip = addr
    print(f'message received from {client_ip} message: {message}')
    bytes_to_send = None
    hc = None
    pickle.dumps(None)
    if message == 'Health_Check':
        hc = healthcheck.get_health_check()
        print(hc)
        bytes_to_send = pickle.dumps(hc)
    if message == 'CPU_INFO':
        hc = pickle.dumps(healthcheck.get_cpu_info())
        print(hc)
        bytes_to_send = hc
    if message == 'MEM_INFO':
        hc = pickle.dumps(healthcheck.get_mem_info())
        print(hc)
        bytes_to_send = hc
    if message == 'DISK_INFO':
        hc = pickle.dumps(healthcheck.get_disk_info())
        print(hc)
        bytes_to_send = hc
    if message == 'NET_INFO':
        hc = pickle.dumps(healthcheck.get_network_info())
        print(hc)
        bytes_to_send = hc
    if message == 'CONN_INFO':
        hc = pickle.dumps(healthcheck.get_connections())
        print(hc)
        bytes_to_send = hc
    if message == 'SENSOR_INFO':
        hc = pickle.dumps(healthcheck.get_sensor_info())
        print(hc)
        bytes_to_send = hc
    if message == 'PROCESSES':
        hc = pickle.dumps(healthcheck.get_processes())
        print(hc)
        bytes_to_send = hc
    
    server_socket.sendto(bytes_to_send, addr)
