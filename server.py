import socket
import threading

from config import HOST, PORT, BUFFER_SIZE, ENCODING


def handle_client(client_socket: socket.socket, client_address: tuple[str, int]) -> None:
    """Handle communication with one connected client."""
    print(f"[NEW CONNECTION] {client_address} connected.")

    try:
        while True:
            message = client_socket.recv(BUFFER_SIZE).decode(ENCODING)

            if not message:
                print(f"[DISCONNECTED] {client_address} disconnected.")
                break

            cleaned_message = message.strip()
            print(f"[RECEIVED FROM {client_address}] {cleaned_message}")

            reply = f"Server received: {cleaned_message}"
            client_socket.sendall(reply.encode(ENCODING))

    except ConnectionResetError:
        print(f"[ERROR] Connection reset by {client_address}.")
    except Exception as error:
        print(f"[ERROR] Unexpected error with {client_address}: {error}")
    finally:
        client_socket.close()
        print(f"[CLOSED] Connection with {client_address} closed.")


def start_server() -> None:
    """Start the socket server and listen for incoming client connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()

        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address),
            daemon=True,
        )
        client_thread.start()

        print(f"[ACTIVE THREADS] {threading.active_count() - 1}")


if __name__ == "__main__":
    start_server()