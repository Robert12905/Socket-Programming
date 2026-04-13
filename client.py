import socket
import threading

from config import HOST, PORT, BUFFER_SIZE, ENCODING


def receive_messages(client_socket: socket.socket) -> None:
    """Continuously receive messages from the server."""
    try:
        while True:
            message = client_socket.recv(BUFFER_SIZE).decode(ENCODING)

            if not message:
                print("[DISCONNECTED] Server closed the connection.")
                break

            print(message)

    except (ConnectionResetError, OSError):
        pass

    except Exception as error:
        print(f"[ERROR] Unexpected receive error: {error}")
        
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

    receive_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket,),
        daemon=True,
    )
    receive_thread.start()

    try:
        while True:
            user_input = input()

            if user_input.strip().lower() == "quit":
                print("[DISCONNECTING] Closing connection...")
                break

            client_socket.sendall(user_input.encode(ENCODING))

    except KeyboardInterrupt:
        print("\n[DISCONNECTING] Client interrupted by user.")

    except OSError:
        print("[DISCONNECTED] Connection to server was lost.")

    except Exception as error:
        print(f"[ERROR] Unexpected send error: {error}")
        
    finally:
        try:
            client_socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        finally:
            client_socket.close()


if __name__ == "__main__":
    start_client()