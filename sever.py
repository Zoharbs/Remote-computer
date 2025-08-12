import socket
import threading
from pynput import keyboard, mouse

# ---------- Safe send helper ----------
def safe_send(sock, data):
    try:
        sock.sendall(data.encode())
    except Exception as e:
        print(f"Send failed: {e}")

# ---------- Server setup ----------
def create_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create TCP Socket object
    server_socket.bind(("127.0.0.1", 8080))  # Define the IP + Port for the server
    server_socket.listen(5)  # Define maximum amount of connections waiting to be accepted
    print("Listening for new connections")
    return server_socket

def accept_client(server_socket):
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")
    return client_socket

# ---------- Keyboard listener ----------
def keyboard_thread(client_socket):
    def on_press(key):
        try:
            print(f"Key pressed: {key.char}")
            safe_send(client_socket, f"key {key.char}")
        except AttributeError:
            print(f"Special key pressed: {key}")
            safe_send(client_socket, f"special {key}")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# ---------- Mouse listener ----------
def mouse_THREAD(client_socket):
    def on_move(x, y):
        print(f"Pointer moved to {(x, y)}")
        safe_send(client_socket, f"move {x} {y}")

    def on_click(x, y, button, pressed):
        print(f"{'Pressed' if pressed else 'Released'} at {(x, y)} with {button}")
        safe_send(client_socket, f"click {x} {y} {button} {pressed}")

    def on_scroll(x, y, dx, dy):
        print(f"Scrolled {'down' if dy < 0 else 'up'} at {(x, y)}")
        safe_send(client_socket, f"scroll {x} {y} {dx} {dy}")

    with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()


if __name__ == "__main__":
    server_sock = create_server()
    client_sock = accept_client(server_sock)
    
    threading.Thread(target=mouse_THREAD, args=(client_sock,), daemon=True).start()
    keyboard_thread(client_sock)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Server stopped.")
        client_sock.close()
        server_sock.close()
