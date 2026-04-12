import socket
import time
import datetime


IP_SERVER = "localhost"
PORT = 9999
ADDRESS = (IP_SERVER, PORT)

serverSocket = socket.socket()
# As a default, the server uses IPv4 and TCP for connection

serverSocket.bind(ADDRESS)
print("Server is Online")

serverSocket.listen(1) # Number of Clients available to join this connection

lstOfInquiry = ["what time it is", "what is todays date"]

while(True):

    connection, ADDRESS = serverSocket.accept() # ADDRESS returns address of client
    # stores the socket object of the connected device (file) allowing for transfer
    # of data, pausing until anything is receieved

    print(f"Client Connected -> {ADDRESS}")

    message = "Hello Client, Here are the server's questions:\n" + "\n".join(lstOfInquiry)
    connection.send(message.encode("utf-8"))
    connection.close()