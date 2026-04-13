import socket
import threading

from config import HOST, PORT, BUFFER_SIZE, ENCODING

clients = []
clients_lock = threading.Lock()


def broadcast_message(message: str, sender_socket: socket.socket) -> None:
    """Send a message to all connected clients except the sender."""
    with clients_lock:
        disconnected_clients = []

        for client_socket in clients:
            if client_socket is sender_socket:
                continue

            try:
                client_socket.sendall(message.encode(ENCODING))
            except OSError:
                disconnected_clients.append(client_socket)

        for client_socket in disconnected_clients:
            if client_socket in clients:
                clients.remove(client_socket)
                client_socket.close()


def remove_client(client_socket: socket.socket) -> None:
    """Remove a client socket from the active clients list."""
    with clients_lock:
        if client_socket in clients:
            clients.remove(client_socket)


def handle_client(client_socket: socket.socket, client_address: tuple[str, int]) -> None:
    """Handle communication with one connected client."""
    print(f"[NEW CONNECTION] {client_address} connected.")

    with clients_lock:
        clients.append(client_socket)

    try:
        while True:
            message = client_socket.recv(BUFFER_SIZE).decode(ENCODING)

            if not message:
                print(f"[DISCONNECTED] {client_address} disconnected.")
                break

            cleaned_message = message.strip()
            formatted_message = f"Client {client_address[1]}: {cleaned_message}"

            print(f"[RECEIVED] {formatted_message}")
            broadcast_message(formatted_message, client_socket)

    except ConnectionResetError:
        print(f"[DISCONNECTED] {client_address} disconnected.")

    except OSError:
        print(f"[DISCONNECTED] {client_address} disconnected.")

    except Exception as error:
        print(f"[ERROR] Unexpected error with {client_address}: {error}")

    finally:
        remove_client(client_socket)
        client_socket.close()
        print(f"[CLOSED] Connection with {client_address} closed.")


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

                print(f"[ACTIVE CLIENTS] {threading.active_count() - 1}")

            except socket.timeout:
                pass

    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server is shutting down.")

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

        server_socket.close()


if __name__ == "__main__":
    start_server()