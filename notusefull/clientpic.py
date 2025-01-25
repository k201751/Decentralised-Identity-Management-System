import socket

def send_picture(picture_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 5000)  # Change the IP address and port of the server
    client_socket.connect(server_address)

    with open(picture_path, 'rb') as file:
        picture_data = file.read()
        client_socket.sendall(picture_data)

    print("Picture sent successfully.")
    client_socket.close()

if __name__ == '__main__':
    picture_path = 'D:\Dev projects\IDmanage\OIP.jpeg'  # Replace with the actual path to your picture
    send_picture(picture_path)
