from flask import Flask, request, send_file, jsonify
import os
import argparse

app = Flask(__name__)

@app.route('/store', methods=['POST'])
def store():
    block_id = request.json['blockId']
    data = request.json['data']
    with open(os.path.join(DATA_DIR, block_id), 'w') as f:
        f.write(data)
    return jsonify({'message': 'Bloque almacenado correctamente'})

@app.route('/block/<block_id>', methods=['GET'])
def get_block(block_id):
    block_path = os.path.join(DATA_DIR, block_id)
    if os.path.exists(block_path):
        return send_file(block_path)
    else:
        return jsonify({'error': 'Bloque no encontrado'}), 404

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Iniciar un DataNode en un puerto específico.')
    parser.add_argument('--port', type=int, default=5001, help='El puerto en el que se ejecutará el DataNode')
    args = parser.parse_args()
    
    DATA_DIR = f'./data{args.port}'
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(port=args.port)