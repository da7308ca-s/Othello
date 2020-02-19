import socket
import sys

try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print("Socket successfully created")
except socket.error as err: 
    print("socket creation failed with error %s" %(err))
  
# default port for socket 
port = 9035
  
try: 
    host_ip = socket.gethostbyname('vm33.cs.lth.se') 
except socket.gaierror: 
    # this means could not resolve the host 
    print("there was an error resolving the host")
    sys.exit() 
  
# connecting to the server 
s.connect((host_ip, port)) 

print("the socket has successfully connected")
  
