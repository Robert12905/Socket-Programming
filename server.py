import socket
import threading
import sys

from config import HOST, PORT, BUFFER_SIZE, ENCODING

clients = []
usernames = {}
clients_lock = threading.Lock()

USER_COLORS = [
    "\033[91m",
    "\033[92m",
    "\033[93m",
    "\033[94m",
    "\033[95m",
    "\033[96m",
]
RESET_COLOR = "\033[0m"
SYSTEM_COLOR = "\033[90m"
ERROR_COLOR = "\033[91m"


def get_username_color(username: str) -> str:
    """Return a deterministic terminal color for a username."""
    if not username:
        return SYSTEM_COLOR

    color_index = sum(ord(char) for char in username) % len(USER_COLORS)
    return USER_COLORS[color_index]


def print_colored(message: str, color: str = SYSTEM_COLOR) -> None:
    """Print a message with terminal color support when available."""
    if sys.stdout.isatty():
        print(f"{color}{message}{RESET_COLOR}")
    else:
        print(message)


def broadcast_message(message: str, sender_socket: socket.socket | None = None) -> None:
    """Send a message to all connected clients except the sender, if provided."""
    with clients_lock:
        disconnected_clients = []

        for client_socket in clients:
            if sender_socket is not None and client_socket is sender_socket:
                continue

            try:
                client_socket.sendall(message.encode(ENCODING))
            except OSError:
                disconnected_clients.append(client_socket)

        for client_socket in disconnected_clients:
            if client_socket in clients:
                clients.remove(client_socket)
                usernames.pop(client_socket, None)
                client_socket.close()


def remove_client(client_socket: socket.socket) -> None:
    """Remove a client socket from the active clients list and username mapping."""
    with clients_lock:
        if client_socket in clients:
            clients.remove(client_socket)
        usernames.pop(client_socket, None)


def handle_client(client_socket: socket.socket, client_address: tuple[str, int]) -> None:
    """Handle communication with one connected client."""
    print_colored(f"[NEW CONNECTION] {client_address} connected.")

    username = f"Client {client_address[1]}"

    try:
        received_username = client_socket.recv(BUFFER_SIZE).decode(ENCODING).strip()
        if received_username:
            username = received_username
        else:
            username = "Anonymous"

        with clients_lock:
            if username in usernames.values():
                client_socket.sendall(
                    "[ERROR] Username already taken. Please choose a different username.".encode(ENCODING)
                )
                print_colored(
                    f"[REJECTED] {client_address} tried duplicate username '{username}'.",
                    ERROR_COLOR,
                )
                client_socket.close()
                return

            clients.append(client_socket)
            usernames[client_socket] = username

        client_socket.sendall("[SERVER] Username accepted.".encode(ENCODING))
        print_colored(
            f"[USERNAME] {client_address} is using username '{username}'.",
            get_username_color(username),
        )
        broadcast_message(f"[SERVER] {username} joined the chat.", client_socket)

        while True:
            message = client_socket.recv(BUFFER_SIZE).decode(ENCODING)

            if not message:
                print_colored(f"[DISCONNECTED] {username} disconnected.", get_username_color(username))
                broadcast_message(f"[SERVER] {username} left the chat.", client_socket)
                break

            cleaned_message = message.strip()
            formatted_message = f"{username}: {cleaned_message}"

            print_colored(f"[RECEIVED] {formatted_message}", get_username_color(username))
            broadcast_message(formatted_message, client_socket)

    except ConnectionResetError:
        print_colored(f"[DISCONNECTED] {username} disconnected.", get_username_color(username))
        broadcast_message(f"[SERVER] {username} left the chat.", client_socket)

    except OSError:
        print_colored(f"[DISCONNECTED] {username} disconnected.", get_username_color(username))
        broadcast_message(f"[SERVER] {username} left the chat.", client_socket)

    except Exception as error:
        print_colored(f"[ERROR] Unexpected error with {client_address}: {error}", ERROR_COLOR)
        
    finally:
        remove_client(client_socket)
        client_socket.close()
        print_colored(f"[CLOSED] Connection with {client_address} closed.", get_username_color(username))


def start_server() -> None:
    """Start the socket server and listen for incoming client connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    # Prevent accept() from blocking forever, allowing Ctrl+C to be handled
    server_socket.settimeout(1.0)

    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    try:
        while True:
            try:
                client_socket, client_address = server_socket.accept()

                client_thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket, client_address),
                )
                client_thread.start()

                print_colored(f"[ACTIVE CLIENTS] {threading.active_count() - 1}")

            except socket.timeout:
                pass

    except KeyboardInterrupt:
        print_colored("\n[SHUTDOWN] Server is shutting down.")

    finally:
        with clients_lock:
            for client_socket in clients:
                try:
                    client_socket.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                finally:
                    client_socket.close()

            clients.clear()
            usernames.clear()

        server_socket.close()


if __name__ == "__main__":
    start_server()