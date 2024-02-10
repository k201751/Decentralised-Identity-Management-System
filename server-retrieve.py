import socket
import json
#from multichain import MultiChain  # Replace with the actual library you use for MultiChain interaction
from subprocess import run, PIPE
from deepface import DeepFace
import cv2
from threading import Thread
import struct
import os

def extract_name(cnic1):
    command = "multichain-cli IDChain liststreamitems identity_stream"
    result = run(command, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    
    if result.returncode == 0:
        try:
            # Parse the JSON from the command output
            json_result = json.loads(result.stdout)

            # Extract information for each entry in the 'json_result' variable
            for entry in json_result:
                data_json = entry.get("data", {}).get("json", {})

                cnic = data_json.get("CNIC", "")
                if cnic == cnic1:
                    pic_loc = data_json.get("name", "")
                    return pic_loc
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print(f"Error running command: {result.stderr}")

def extract_loc(cnic1):
    command = "multichain-cli IDChain liststreamitems identity_stream"
    result = run(command, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    
    if result.returncode == 0:
        try:
            # Parse the JSON from the command output
            json_result = json.loads(result.stdout)

            # Extract information for each entry in the 'json_result' variable
            for entry in json_result:
                data_json = entry.get("data", {}).get("json", {})

                cnic = data_json.get("CNIC", "")
                if cnic == cnic1:
                    pic_loc = data_json.get("picture location", "")
                    print(pic_loc)
                    return pic_loc
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print(f"Error running command: {result.stderr}")

def extract(cnic1):
    # Assume the 'result' variable contains the provided JSON text
    command = "multichain-cli IDChain liststreamitems identity_stream"
    result = run(command, shell=True, stdout=PIPE, stderr=PIPE, text=True)

    # Check if the command was successful
    if result.returncode == 0:
        try:
            # Parse the JSON from the command output
            json_result = json.loads(result.stdout)

            # Extract information for each entry in the 'json_result' variable
            for entry in json_result:
                data_json = entry.get("data", {}).get("json", {})

                cnic = data_json.get("CNIC", "")
                if cnic == cnic1:
                    name = data_json.get("name", "")
                    fname = data_json.get("father's name", "")
                    DOB = data_json.get("DOB", "")
                    pic_hash = data_json.get("person's picture hash", "")
                    pic_loc = data_json.get("picture location", "")
                    #txid = chain.publish(stream_name, 'key1', json.dumps(json_data),)
                    json_data_pub='"{"json":{"name":"'+name+'","father\'s name":"'+fname+'", "DOB": "'+DOB+'", "CNIC": "'+cnic+'"}}"'
                    """
                    print(f"Name: {name}")
                    print(f"Father's Name: {father_name}")
                    print(f"Date of Birth: {dob}")
                    print(f"CNIC: {cnic}")
                    print(f"Picture Hash: {picture_hash}")
                    print(f"Picture Location: {picture_location}")
                    print("-----")
                    """
                    return json_data_pub
                    break

            print("Not found!")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print(f"Error running command: {result.stderr}")


def face_matching_algorithm(cnic, name):
    # Replace this with your actual face-matching algorithm implementation
    # For simplicity, we'll assume all faces match for this example
    cwd = os.getcwd()
    img1_loc = cwd+ "\\" + name + "_picture.jpg"
    print(img1_loc)
    img1=cv2.imread(img1_loc)
    print(cwd)
    img2_loc = cwd+ "\\" + name + "_verify_picture.jpg"
    img2=cv2.imread(img2_loc)

    result = DeepFace.verify(img1, img2)
    return result['verified']

def handle_client(client_socket):
    # Receive CNIC number
    cnic_length = struct.unpack("!I", client_socket.recv(4))[0]
    cnic = client_socket.recv(cnic_length).decode()

    # Receive picture file
    picture_size = struct.unpack("!Q", client_socket.recv(8))[0]
    picture_data = b""
    while len(picture_data) < picture_size:
        packet = client_socket.recv(1024)
        if not packet:
            print("z")
            break
            
        picture_data += packet

    name = extract_name(cnic)

    with open(f"{name}_verify_picture.jpg", "wb") as picture_file:
        picture_file.write(picture_data)

    # Assuming you have a face-matching algorithm implementation
    is_match = face_matching_algorithm(cnic, name)

    if is_match:
        user_info = extract(cnic)

        if user_info:
            response_data = {"status": "success", "user_info": user_info}
        else:
            response_data = {"status": "error", "message": "User not found in MultiChain"}
    else:
        response_data = {"status": "error", "message": "Face doesn't match"}

    response = json.dumps(response_data)
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(5)
    print("Server listening on port 5000...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_handler = Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    run_server()
