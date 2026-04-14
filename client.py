import socket
import threading
import sys

from config import HOST, PORT, BUFFER_SIZE, ENCODING

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


def format_incoming_message(message: str) -> str:
    """Apply consistent username colors to incoming chat messages."""
    if not sys.stdout.isatty():
        return message

    if message.startswith("[ERROR]"):
        return f"{ERROR_COLOR}{message}{RESET_COLOR}"

    if message.startswith("["):
        return f"{SYSTEM_COLOR}{message}{RESET_COLOR}"

    if ": " in message:
        username, content = message.split(": ", 1)
        username_color = get_username_color(username)
        return f"{username_color}{username}{RESET_COLOR}: {content}"

    return message


def receive_messages(client_socket: socket.socket, connection_closed: threading.Event) -> None:
    """Continuously receive messages from the server."""
    try:
        while True:
            message = client_socket.recv(BUFFER_SIZE).decode(ENCODING)

            if not message:
                if not connection_closed.is_set():
                    print("[DISCONNECTED] Server closed the connection.")
                    connection_closed.set()
                break

            print(format_incoming_message(message))

    except (ConnectionResetError, OSError):
        if not connection_closed.is_set():
            print("[DISCONNECTED] Server closed the connection.")
            connection_closed.set()

    except Exception as error:
        if not connection_closed.is_set():
            print(f"[ERROR] Unexpected receive error: {error}")
            connection_closed.set()

    finally:
        client_socket.close()

def start_client() -> None:
    """Connect to the server and allow the user to send messages."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    username = input("Enter username: ").strip()
    if not username:
        username = "Anonymous"

    client_socket.sendall(username.encode(ENCODING))

    server_response = client_socket.recv(BUFFER_SIZE).decode(ENCODING)

    if server_response.startswith("[ERROR]"):
        print(server_response)
        client_socket.close()
        return

    print(f"[CONNECTED] Connected to server at {HOST}:{PORT}")
    print("Type messages and press Enter to send.")
    print("Type 'quit' to disconnect.\n")

    connection_closed = threading.Event()

    receive_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket, connection_closed),
        daemon=True,
    )
    receive_thread.start()

    try:
        while True:
            user_input = input()

            if connection_closed.is_set():
                break

            if user_input.strip().lower() == "quit":
                print("[DISCONNECTING] Closing connection...")
                break

            client_socket.sendall(user_input.encode(ENCODING))

    except KeyboardInterrupt:
        print("\n[DISCONNECTING] Client interrupted by user.")

    except OSError:
        if not connection_closed.is_set():
            print("[DISCONNECTED] Connection to server was lost.")
            connection_closed.set()

    except Exception as error:
        if not connection_closed.is_set():
            print(f"[ERROR] Unexpected send error: {error}")
            connection_closed.set()

    finally:
        try:
            client_socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        finally:
            client_socket.close()


if __name__ == "__main__":
    start_client()