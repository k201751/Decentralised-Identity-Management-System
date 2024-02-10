import socket
import json
import hashlib
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


def hash_image(file_path, hash_algorithm='sha256'):
    """Generate a hash for the content of an image file."""
    hash_obj = hashlib.new(hash_algorithm)
    
    with open(file_path, 'rb') as file:
        # Read the file in chunks to handle large files
        for chunk in iter(lambda: file.read(4096), b""):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()


def send_data_to_server(data, pic_loc):
    # Server address and port
    server_address = ('127.0.0.1', 443)

    # Create a socket connection to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(server_address)

        # Send JSON data to the server
        json_data = json.dumps(data)
        client_socket.sendall(json_data.encode('utf-8'))

        with open(pic_loc, 'rb') as file:
            picture_data = file.read()
            client_socket.sendall(picture_data)

        print("Picture sent successfully.")
        # Receive and print the server's response
        response = client_socket.recv(1024)
        print(response.decode('utf-8'))



def get_user_input():
    name = input("Enter the person's name: ")
    fname = input("Enter the person's father's name: ")
    DOB = input("Enter the person's DOB: ")
    CNIC = input("Enter the person's CNIC number: ")
    pic_loc = input("Enter person's picture location: ")
    input(pic_loc)

    

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 443))
    name = input("Enter the person's name: ")
    fname = input("Enter the person's father's name: ")
    DOB = input("Enter the person's DOB: ")
    CNIC = input("Enter the person's CNIC number: ")
    pic_loc = input("Enter person's picture location: ")
    input(pic_loc)
    send_data(client_socket, name, fname, DOB, CNIC, pic_loc)
    print("Data sent successfully.")

if __name__ == "__main__":
    main()
