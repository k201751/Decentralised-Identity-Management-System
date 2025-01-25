from web3 import Web3

# Ethereum node endpoint
eth_node_endpoint = "http://localhost:8545"  # Replace with your Ethereum node endpoint

# Smart contract address and ABI (replace with your actual values)
contract_address = "0x1234567890123456789012345678901234567890"
contract_abi = [...]
private_key = "0x0123456789012345678901234567890123456789012345678901234567890123"

# Connect to the Ethereum node
web3 = Web3(Web3.HTTPProvider(eth_node_endpoint))

# Create an Ethereum account using the private key
account = web3.eth.account.from_key(private_key)

# Set the default account
web3.eth.defaultAccount = account.address

# Load the smart contract ABI
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def addIdentityInfo(name, age, address):
    # Assume your smart contract has a function named addIdentityInfo
    # This function takes parameters such as name, age, and address
    # and appends them to the blockchain

    # Sign the transaction
    transaction = contract.functions.addIdentityInfo(name, age, address).buildTransaction({
        'from': account.address,
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': web3.eth.getTransactionCount(account.address),
    })

    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    transaction_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    return transaction_hash

# Example usage
name = "John Doe"
age = 25
address = "123 Main St, City"
transaction_hash = addIdentityInfo(name, age, address)
print(f"Transaction Hash: {transaction_hash}")
