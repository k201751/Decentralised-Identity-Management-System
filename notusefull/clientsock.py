import socket
import json
import hashlib

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
    pic_hash = hash_image(pic_loc)
    input(pic_hash)
    input(pic_loc)
    user_data = {
        "name": name,
        "father's name" : fname,
        "DOB": DOB,
        "CNIC": CNIC,
        "person's picture hash": pic_hash,
        "picture location": pic_loc
    }

    return user_data, pic_loc

def main():
    user_data, pic_loc = get_user_input()
    send_data_to_server(user_data, pic_loc)

if __name__ == "__main__":
    main()
