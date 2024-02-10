import socket
from threading import Thread
from flask import Flask, request, jsonify
from multichain import *
import json
from subprocess import run, PIPE
from ecdsa import SigningKey, SECP256k1
import base64
import struct
import os


app = Flask(__name__)

# Replace these values with your MultiChain configuration
multichain_rpc_user = "multichainrpc"
multichain_rpc_password = "6XWJ9D3qjfs7bLL4pU2UskvHWrvkyJRrE14UavYmeJGR"
multichain_rpc_port = 2890
multichain_chain_name = "IDChain"


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


def generate_key_pair():
    private_key = SigningKey.generate(curve=SECP256k1)
    command = f"multichain-cli IDChain getnewaddress"
    result = run(command, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    public_key = result.stdout.strip()
    if result.returncode == 0:
        command1 = f"multichain-cli IDChain dumpprivkey {public_key}"
        result1 = run(command1, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        private_key = result1.stdout.strip()
        if result1.returncode == 0:
            return private_key, public_key
        else:
            print(f"{result1.stderr}")
            return None
    else:
        print(f"{result.stderr}")
        return None

    return private_key.to_string().hex(), public_key

def create_multisig_address(pubkeys, threshold):
    pubkeys_json = ', '.join([f'\\"{key}\\"' for key in pubkeys])
    command = f"multichain-cli IDChain createmultisig {threshold} \"[{pubkeys_json}]\""
    result = run(command, shell=True, stdout=PIPE, stderr=PIPE, text=True)

    if result.returncode == 0:
        return result.stdout.strip()
    else:
        print(f"Error creating multisignature address: {result.stderr}")
        return None

def handle_request(client_socket, multisig_address, privkeys):
    name, fname, DOB, CNIC, picture_data = receive_data(client_socket)
    save_picture(name, picture_data)
    try:
        json_data_pub='\"{\\"json\\":{\\"name\\":\\"'+name+'\\",\\"father\'s name\\":\\"'+fname+'\\", \\"DOB\\": \\"'+DOB+'\\", \\"CNIC\\": \\"'+CNIC+'\\"}}\"'

        chain = multichain.api_call(multichain_rpc_user, multichain_rpc_password,'127.0.0.1', multichain_rpc_port, multichain_chain_name)
        stream_name = 'identity_stream'

        signatures = []
        for privkey in privkeys:
            addrload=json.loads(multisig_address)
            msaddr=addrload["address"]
            command = f"multichain-cli IDChain signmessage {privkey} {json_data_pub} "
            result = run(command, shell=True, stdout=PIPE, stderr=PIPE, text=True)
            
            if result.returncode == 0:
                signatures.append(result.stdout.strip())
            else:
                print(f"Error signing message: {result.stderr}")
                return

        multisig = ",".join(signatures)

        command = f"multichain-cli IDChain publish {stream_name} key1 {json_data_pub}"
        result = run(command, shell=True, stdout=PIPE, stderr=PIPE, text=True)

        if result.returncode == 0:
            print(f"Message uploaded to blockchain stream successfully.")
        else:
            print(f"Error uploading message to blockchain: {result.stderr}")

        response = f"HTTP/1.1 200 OK\r\n\r\n{{\"status\": \"success\"}}"

    except Exception as e:
        response = f"HTTP/1.1 500 Internal Server Error\r\n\r\n{{\"status\": \"error\", \"message\": \"{str(e)}\"}}"

def run_server():
    pubkeys = []
    privkeys = []
    for _ in range(3):
        private_key, public_key = generate_key_pair()
        pubkeys.append(public_key)
        privkeys.append(private_key)

    threshold = 2
    # Create a multisignature address
    multisig_address = create_multisig_address(pubkeys, threshold)
    if(multisig_address):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 443))
        server_socket.listen(5)
        print("Server listening on port 443...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            client_handler = Thread(target=handle_request, args=(client_socket, multisig_address, privkeys))
            client_handler.start()

if __name__ == '__main__':
    run_server()
