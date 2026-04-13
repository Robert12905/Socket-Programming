import socket
import threading

from config import HOST, PORT, BUFFER_SIZE, ENCODING


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

            print(message)

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