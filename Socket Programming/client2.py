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
	userInput = input("Choose a server output (1/2/3): ").strip()
	if userInput in ("1", "2", "3"):
		clientSocket.sendall((userInput + "\n").encode("utf-8"))
		break
	print("Invalid input. Please enter 1, 2, or 3.")

print(f"Server response -> {clientSocket.recv(1024).decode('utf-8')}")
clientSocket.close()

