#!/usr/bin/python3

# Usage:
#  ./display_ssl.py --help
#  ./display_ssl.py --url=????
#
# Example commands:
#  ./display_ssl.py --url=http://ut-images.s3.amazonaws.com/wp-content/uploads/2009/09/SED_wall_1920x1200.jpg
#  ./display_ssl.py --url=https://www.nasa.gov/wp-content/uploads/2024/11/sts051-75-036orig.jpg

import argparse
import socket
import ssl
import os
from subprocess import call
from urllib.parse import urlparse

# Size of receive buffer.
# Maximum number of bytes to get from network in one recv() call
max_recv = 64*1024

# Setup configuration
parser = argparse.ArgumentParser(description='Image download client for ECPE 170')
parser.add_argument('--url', 
                    action='store',
                    dest='url', 
                    required=True,
                    help='URL of image to download')

args = parser.parse_args()
url = args.url

print("Running image download client")
print("Image url: %s" % url)

# Split URL into its component pieces and
# display each piece for debugging....
u = urlparse(url)
print("Parsing URL:")
print(" * scheme=%s" % u.scheme)
print(" * netloc=%s" % u.netloc)
print(" * path+file=%s" % u.path)
print(" * path=%s" % os.path.dirname(u.path))
print(" * file=%s" %os.path.basename(u.path))
print()

# Download file (image) from http://host/path/filename
scheme = u.scheme
host = u.netloc
path = os.path.dirname(u.path) + '/'
filename = os.path.basename(u.path)

print("Preparing to download object from " + scheme + "://" + host + path + filename)

if scheme == "http":
    port = 80
elif scheme == "https":
    port = 443
else:
    raise Exception("Invalid URL - must be http or https")

# *****************************
# STUDENT WORK: 
#  (1) Build the HTTP request string to send to the server
#      and *print it* on the screen.

request = f"GET {u.path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
print("HTTP Request:")
print(request)
       #GET /about/ HTTP/1.1
       #Host: www.google.com
       #Connection: close 

#      Requirements:
#        HTTP 1.1
#        Use the Host header
#        Request the connection be closed after response sent.
#
#      Tip: What is the important sequence of characters that
#      must be provided at the end of the HTTP client request
#      to the server? (otherwise, the server won't begin processing) /r/n/r/n or enter twice after connection close using -C
# *****************************





# *****************************
# STUDENT WORK: 
#  (2) Create a IPv4 / TCP socket (AF_INIT, SOCK_STREAM)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#  (3) If this is a HTTPS (secure) URL, use
#      create_default_context() and wrap_socket()
#ssl is 
if scheme == "https":
    context = ssl.create_default_context()
    s = context.wrap_socket(s, server_hostname=host)


#      to wrap it in a library that will handle encyption
#  (4) Connect to the remote host using the socket

s.connect((host,port))


#  (5) Send the HTTP request to the remote host.
#      Tip: Look at the demo client program to see how
#      to convert a unicode string to a byte array
#      prior to transmitting it.
# *****************************


raw_bytes = bytes(request,'ascii')
bytes_sent = s.sendall(raw_bytes)


# *****************************
# STUDENT WORK: 
#  (6) Receive everything the remote host sends us
#      in chunks of 'max_recv' bytes (64kB).
#      When the server finishes sending us the data,
#      it will close the socket. That is detected locally
#      by receiving an array of length ZERO
#      (i.e. no bytes received)
#  (7) Close the socket - finished with the network now
# *****************************

response = b''

while True:
    data = s.recv(max_recv)
    if len(data) == 0:
        break
    response += data

s.close()



# *****************************
# STUDENT WORK: 
#  (8) Split the response into two parts:
#        1.) The part before the \r\n\r\n sequence - the HEADER
header, body = response.split(b"\r\n\r\n", 1)
#        2.) The part after the \r\n\r\n sequence - the DATA

#  (9) Print the HEADER out on the screen - it's ASCII text
print("HTTP Response Header:")
print(header.decode())
#  (10) Save the DATA to disk as a binary file. Somewhere
#      in the /tmp directory would be a great spot.

saved_filename = "/tmp/" + filename
with open(saved_filename, "wb") as f:
    f.write(body)
print("Saved image to:", saved_filename)
# *****************************





# *****************************
# END OF STUDENT WORK
# *****************************

# Assuming you downloaded the image, and placed its path/filename
# in the variable 'saved_filename', use the 'eog' utility to 
# display the image on screen
call(["eog", saved_filename])

#
