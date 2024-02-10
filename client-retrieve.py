import socket
import json
import struct

def receive_response(client_socket):
    response_data = b""
    while True:
        packet = client_socket.recv(1024)
        if not packet:
            break
        response_data += packet

    return json.loads(response_data.decode('utf-8'))

def send_data(cnic, picture_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        server_address = ('127.0.0.1', 5000)
        client_socket.connect(server_address)

        # Send CNIC number
        cnic_data = cnic.encode()
        client_socket.send(struct.pack("!I", len(cnic_data)))
        client_socket.send(cnic_data)

        # Send picture file
        with open(picture_path, "rb") as picture_file:
            picture_data = picture_file.read()
            client_socket.send(struct.pack("!Q", len(picture_data)))
            client_socket.sendall(picture_data)

        # Receive and process server response
        response = receive_response(client_socket)

        if response["status"] == "success":
            user_info = response["user_info"]
            print("User Info:")
            print(json.dumps(user_info, indent=2))
        else:
            print(f"Error: {response['message']}")

def main():
    cnic = input("Enter CNIC: ")
    picture_location = input("Enter the location of the new picture taken: ")

    send_data(cnic, picture_location)

if __name__ == "__main__":
    main()
