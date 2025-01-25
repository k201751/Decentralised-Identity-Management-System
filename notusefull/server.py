from flask import Flask, request, jsonify
import multichain as MultiChain
import json

app = Flask(__name__)

# Replace these values with your MultiChain configuration
multichain_rpc_user = "multichainrpc"
multichain_rpc_password = "6XWJ9D3qjfs7bLL4pU2UskvHWrvkyJRrE14UavYmeJGR"
multichain_rpc_port = 2890
multichain_chain_name = "test"

@app.route('/', methods=['POST'])
def receive_data():
    try:
        data = request.json
        
        # Connect to MultiChain
        multichain = MultiChain(
            user=multichain_rpc_user,
            password=multichain_rpc_password,
            port=multichain_rpc_port,
            chainname=multichain_chain_name
        )
        
        # Example: Creating a stream named 'identity_stream' if not exists
        stream_name = 'identity_stream'
        multichain.create('stream', stream_name, True)
        
        # Example: Publishing data to the 'identity_stream'
        txid = multichain.publish(stream_name, data['name'], json.dumps(data))
        
        return jsonify({"status": "success", "txid": txid})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=443)
