import socket
from threading import Thread
from flask import Flask, request, jsonify
from multichain import *
import json
from subprocess import run, PIPE

app = Flask(__name__)

# Replace these values with your MultiChain configuration
multichain_rpc_user = "multichainrpc"
multichain_rpc_password = "6XWJ9D3qjfs7bLL4pU2UskvHWrvkyJRrE14UavYmeJGR"
multichain_rpc_port = 2890
multichain_chain_name = "test"

def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode("utf-8")
    
    # Parse the HTTP request to get the JSON data
    try:
        start_index = request_data.find('{')
        end_index = request_data.find('}')
        json_data = json.loads(request_data[start_index:end_index + 1])
        #print(json_data['name'])
        #input()
    except json.JSONDecodeError as e:
        response = "HTTP/1.1 400 Bad Request\r\n\r\nInvalid JSON data"
        client_socket.send(response.encode("utf-8"))
        client_socket.close()
        return

    try:
        # Connect to MultiChain
        chain = multichain.api_call(multichain_rpc_user, multichain_rpc_password,'127.0.0.1', multichain_rpc_port, multichain_chain_name)
        """
        multichain = MultiChain(
            user=multichain_rpc_user,
            password=multichain_rpc_password,
            port=multichain_rpc_port,
            chainname=multichain_chain_name
        )
"""
        # Example: Creating a stream named 'identity_stream' if not exists
        stream_name = 'identity_stream'
        #multichain.create('stream', stream_name, True)

        # Example: Publishing data to the 'identity_stream'
        #print(json.dumps(json_data))
        #print(json_data)
        #input()
        name = json_data['name']
        fname = json_data['father\'s name']
        DOB = json_data['DOB']
        CNIC = json_data['CNIC']
        pic_hash = json_data['person\'s picture hash']
        pic_loc = json_data['picture location']
        #txid = chain.publish(stream_name, 'key1', json.dumps(json_data),)
        json_data_pub='\"{\\"json\\":{\\"name\\":\\"'+name+'\\",\\"father\'s name\\":\\"'+fname+'\\", \\"DOB\\": \\"'+DOB+'\\", \\"CNIC\\": \\"'+CNIC+'\\", \\"person\'s picture hash\\": \\"'+pic_hash+'\\", \\"picture location\\": \\"'+pic_loc+'\\"}}\"'
        print(json_data_pub)
        input()
        #txid = chain.publish(stream_name, 'key1', json_data_pub)
        command = f"multichain-cli test publish identity_stream key1 {json_data_pub}" 
        print(command)
        #input() 

        result = run(command, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        if result.returncode == 0:
            print(f"Message uploaded to blockchain stream successfully.")
        else:
            print(f"Error uploading message to blockchain: {result.stderr}")
        #txid = chain.publish(stream_name, 'key1', json_data_pub)

        response = f"HTTP/1.1 200 OK\r\n\r\n{{\"status\": \"success\", \"txid\": \"{txid}\"}}"
    except Exception as e:
        response = f"HTTP/1.1 500 Internal Server Error\r\n\r\n{{\"status\": \"error\", \"message\": \"{str(e)}\"}}"

    client_socket.send(response.encode("utf-8"))
    client_socket.close()

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 443))
    server_socket.listen(5)
    print("Server listening on port 443...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_handler = Thread(target=handle_request, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    run_server()
