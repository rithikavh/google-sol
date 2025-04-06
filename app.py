from flask import Flask, render_template, jsonify, request, send_from_directory
import datetime
import hashlib
import json

app = Flask(__name__)

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = str(self.index) + str(self.timestamp) + json.dumps(self.data) + str(self.previous_hash)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.contracts = [] # Store contract data

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), {"message": "Genesis Block"}, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def add_contract(self, contract):
        self.contracts.append(contract)

# Move blockchain instantiation here, after both classes are defined
blockchain = Blockchain()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/mine_contract', methods=['POST'])
def mine_contract():
    data = request.get_json()
    if not data or 'transactions' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    new_block = Block(len(blockchain.chain), datetime.datetime.now(), data, blockchain.get_latest_block().hash)
    blockchain.add_block(new_block)
    return jsonify({'message': 'New block mined!', 'block': new_block.__dict__}), 201

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [block.__dict__ for block in blockchain.chain]
    return jsonify({'chain': chain_data, 'length': len(chain_data)}), 200

@app.route('/validate', methods=['GET'])
def validate_chain():
    is_valid = blockchain.is_chain_valid()
    if is_valid:
        return jsonify({'message': 'Blockchain is valid'}), 200
    else:
        return jsonify({'message': 'Blockchain is not valid'}), 400

@app.route('/upload_contract', methods=['POST'])
def upload_contract():
    contract_data = request.get_json()
    if not contract_data or 'contractName' not in contract_data or 'contractCode' not in contract_data:
        return jsonify({'error': 'Invalid contract data'}), 400

    new_contract = {
        'contract_name': contract_data['contractName'],
        'contract_code': contract_data['contractCode'],
        'status': 'Active'
    }

    blockchain.add_contract(new_contract)

    return jsonify({'message': 'Contract uploaded successfully'}), 201

@app.route('/api/contracts', methods=['GET'])
def get_contracts():
    return jsonify(blockchain.contracts), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)