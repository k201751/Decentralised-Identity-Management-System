import socket
import struct
import os

def send_data(client_socket, name, father_name, dob, cnic, picture_path):
    # Send name
    name_data = name.encode()
    client_socket.send(struct.pack("!I", len(name_data)))
    client_socket.send(name_data)

    # Send father's name
    father_name_data = father_name.encode()
    client_socket.send(struct.pack("!I", len(father_name_data)))
    client_socket.send(father_name_data)

    # Send date of birth
    dob_data = dob.encode()
    client_socket.send(struct.pack("!I", len(dob_data)))
    client_socket.send(dob_data)

    # Send CNIC number
    cnic_data = cnic.encode()
    client_socket.send(struct.pack("!I", len(cnic_data)))
    client_socket.send(cnic_data)

    # Send picture file
    with open(picture_path, "rb") as picture_file:
        picture_data = picture_file.read()
        client_socket.send(struct.pack("!Q", len(picture_data)))
        client_socket.sendall(picture_data)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 8888))

    # Input information from the user
    name = input("Enter Name: ")
    father_name = input("Enter Father's Name: ")
    dob = input("Enter Date of Birth: ")
    cnic = input("Enter CNIC Number: ")
    picture_path = input("Enter Picture Path: ")

    # Send data to the server
    send_data(client_socket, name, father_name, dob, cnic, picture_path)

    print("Data sent successfully.")

    client_socket.close()

if __name__ == "__main__":
    main()
