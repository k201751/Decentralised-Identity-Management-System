import socket

def receive_picture():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('0.0.0.0', 5000)  # Change the IP address and port as needed
    server_socket.bind(server_address)
    server_socket.listen(1)

    print("Server is ready to receive a picture.")

    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    with open('received_picture.jpg', 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)

    print("Picture received successfully.")
    client_socket.close()

if __name__ == '__main__':
    receive_picture()
