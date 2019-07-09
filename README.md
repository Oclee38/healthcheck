# healthcheck
Health check - pulling server data

Health Check is remotely pulling server information from a Server - identified by the System Arguments. 
As Example: 
udp_client.py 192.168.1.100 6698 Health_Check
Where
udp_client.py is the client > IP address of the server > Port number to connect to > The Data you would like to receive.


Possible data:
Health_Check gives </br>
  Basic CPU information
  Basic Memory information
  Disk Usage 
  Network data (sent and received in bytes)
  NIC information
  Uptime 
  Logged in users and what terminal they using

CPU_INFO 
  Has additional information on the CPU and will only publish CPU data
 MEM_INFO
  Has more memory information and only publish MEM info
 DISK_INFO
  Will give you only the DISK usage information
 NET_INFO
  Gives only the basic Networking info and the NIC information 
 CONN_INFO
  Gives you an extended list of all open connections with the remote address, port, pid
 SENSOR_INFO
  Gives the information like battery (if used) Temperature (Unix / Linux only) and Uptimes and user information
 PROCESSES
  Gives a list of all Processes information, including memory and cpu usage, network usage and the PID
  
