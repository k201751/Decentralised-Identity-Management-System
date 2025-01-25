import socket
import struct
import os

def receive_data(client_socket):
    # Receive name
    name_length = struct.unpack("!I", client_socket.recv(4))[0]
    name = client_socket.recv(name_length).decode()

    # Receive father's name
    father_name_length = struct.unpack("!I", client_socket.recv(4))[0]
    father_name = client_socket.recv(father_name_length).decode()

    # Receive date of birth
    dob_length = struct.unpack("!I", client_socket.recv(4))[0]
    dob = client_socket.recv(dob_length).decode()

    # Receive CNIC number
    cnic_length = struct.unpack("!I", client_socket.recv(4))[0]
    cnic = client_socket.recv(cnic_length).decode()

    # Receive picture file
    picture_size = struct.unpack("!Q", client_socket.recv(8))[0]
    picture_data = b""
    while len(picture_data) < picture_size:
        packet = client_socket.recv(1024)
        if not packet:
            break
        picture_data += packet

    return name, father_name, dob, cnic, picture_data

def save_picture(name, picture_data):
    with open(f"{name}_picture.jpg", "wb") as picture_file:
        picture_file.write(picture_data)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 8888))
    server_socket.listen(1)

    print("Server is listening for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Receive data from the client
        name, father_name, dob, cnic, picture_data = receive_data(client_socket)

        # Save the received picture file
        save_picture(name, picture_data)

        # Display received information
        print("\nReceived Information:")
        print(f"Name: {name}")
        print(f"Father's Name: {father_name}")
        print(f"Date of Birth: {dob}")
        print(f"CNIC Number: {cnic}")
        print("Picture file saved.")

        client_socket.close()

if __name__ == "__main__":
    main()
