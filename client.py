import socket

from pynput import keyboard, mouse


def create_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create TCP Socket object
    client_socket.connect(("127.0.0.1", 8080))  # Connect to server
    print("Client connected")
    return client_socket

def click_keyboard(key):
    if "key" in key:
        pass
    else:
        print("pressing regular key:", key)



client_socket = create_client()
while True:
    key=client_socket.recv(1024)  # Receive data from server
    key = key.decode()  # Decode the received bytes
    print("received:", key)
    mouse_move = client_socket.recv(1024)  
    mouse_move = mouse_move.decode()  # Decode the received bytes
    #print("Mouse move:", mouse_move)
    mouse_click = client_socket.recv(1024)
    mouse_click = mouse_click.decode()  
  #  print("Mouse click:", mouse_click)
    mouse_scroll = client_socket.recv(1024)
    mouse_scroll = mouse_scroll.decode()  
   # print("Mouse scroll:", mouse_scroll)