from flask import Flask, request, send_file, jsonify
import os
import argparse
import base64

app = Flask(__name__)

@app.route('/store', methods=['POST'])
def store():
    try:
        # Recibir los datos del bloque y decodificarlos
        block_id = request.json['blockId']
        data = request.json['data']
        
        # Decodificar el bloque de base64 a binario
        block_data = base64.b64decode(data)
        
        # Crear o escribir en el archivo correspondiente
        with open(os.path.join(DATA_DIR, block_id), 'wb') as f:
            f.write(block_data)
        
        # Retornar una respuesta de éxito
        return jsonify({'message': 'Bloque almacenado correctamente'})
    
    except Exception as e:
        # Si ocurre un error, capturarlo y retornar una respuesta de error
        print(f"Error al almacenar el bloque: {e}")
        return jsonify({'error': f'Error al almacenar el bloque: {str(e)}'}), 500


@app.route('/block/<block_id>', methods=['GET'])
def get_block(block_id):
    try:
        # Buscar el bloque en el directorio DATA_DIR
        block_path = os.path.join(DATA_DIR, block_id)
        
        # Verificar si el archivo existe
        if os.path.exists(block_path):
            return send_file(block_path)
        else:
            return jsonify({'error': 'Bloque no encontrado'}), 404
    
    except Exception as e:
        # Manejar errores si ocurren durante la lectura del archivo
        print(f"Error al obtener el bloque: {e}")
        return jsonify({'error': f'Error al obtener el bloque: {str(e)}'}), 500

if __name__ == '__main__':
    # Argumentos para especificar el puerto del DataNode
    parser = argparse.ArgumentParser(description='Iniciar un DataNode en un puerto específico.')
    parser.add_argument('--port', type=int, default=5001, help='El puerto en el que se ejecutará el DataNode')
    args = parser.parse_args()
    
    # Crear el directorio donde se almacenarán los bloques de datos
    DATA_DIR = f'./data{args.port}'
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # Iniciar la aplicación Flask en el puerto especificado
    app.run(host='0.0.0.0', port=args.port)
