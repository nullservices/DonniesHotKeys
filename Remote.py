# remote.py
import socket
from pynput.keyboard import Controller, Key

keyboard = Controller()

def press_keys(keys):
    for key in keys:
        if key in ['shift', 'ctrl', 'alt']:
            key = getattr(Key, key)
        keyboard.press(key)
    for key in reversed(keys):
        if key in ['shift', 'ctrl', 'alt']:
            key = getattr(Key, key)
        keyboard.release(key)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 65432))
    server_socket.listen(1)
    print("Listening for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            key_combination = data.split('+')
            press_keys(key_combination)

        client_socket.close()

if __name__ == "__main__":
    start_server()
