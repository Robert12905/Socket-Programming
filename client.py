import socket


IP_SERVER = "localhost"
PORT = 9999
ADDRESS = (IP_SERVER, PORT)

clientSocket = socket.socket()
clientSocket.connect(ADDRESS)

print("Connected to Server")


response = clientSocket.recv(1024).decode("utf-8")

print(response)

while True:
	try:
		userInput = int(input("Choose a server output: "))
		clientSocket.send(str(userInput).encode("utf-8"))
		break
	except:
		print("Invalid input. Please enter a number.")
