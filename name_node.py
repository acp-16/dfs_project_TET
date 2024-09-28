from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import random
import requests

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("adminpass"),
    "user1": generate_password_hash("password123")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None

data_nodes = ['http://localhost:5001', 'http://localhost:5002', 'http://localhost:5003']

metadatos = {}

@app.route('/put', methods=['POST'])
@auth.login_required
def put():
    file = request.files['file']
    filename = file.filename
    content = file.read()

    # Particionar el archivo en bloques
    bloques = [content[i:i + 1024] for i in range(0, len(content), 1024)]

    # Elegir DataNodes para almacenar los bloques y replicarlos
    ubicaciones = {}
    for i, bloque in enumerate(bloques):
        primary_datanode = random.choice(data_nodes)
        follower_datanode = random.choice([dn for dn in data_nodes if dn != primary_datanode])

        # Enviar el bloque al DataNode primario (Leader)
        response = requests.post(f'{primary_datanode}/store', json={'blockId': f'{filename}_block{i}', 'data': bloque.decode('latin1')})
        if response.status_code == 200:
            # Almacenar la ubicación del bloque
            ubicaciones[i] = {'leader': primary_datanode, 'follower': follower_datanode}

            # Replicar el bloque en el DataNode follower
            requests.post(f'{follower_datanode}/store', json={'blockId': f'{filename}_block{i}', 'data': bloque.decode('latin1')})

    metadatos[filename] = ubicaciones
    return jsonify({'message': f'{filename} subido con éxito', 'ubicaciones': ubicaciones})

@app.route('/get/<filename>', methods=['GET'])
@auth.login_required
def get(filename):
    if filename in metadatos:
        file_data = b''
        for i, datanode_info in metadatos[filename].items():
            primary_datanode = datanode_info['leader']
            follower_datanode = datanode_info['follower']
            try:
                response = requests.get(f'{primary_datanode}/block/{filename}_block{i}')
                if response.status_code != 200:
                    raise requests.exceptions.RequestException
            except requests.exceptions.RequestException:
                print(f'Error al obtener bloque {i} de {primary_datanode}, intentando con follower...')
                try:
                    response = requests.get(f'{follower_datanode}/block/{filename}_block{i}')
                except requests.exceptions.RequestException:
                    print(f'Error también en {follower_datanode}. El bloque {i} está inaccesible.')
                    return jsonify({'error': f'Bloque {i} no disponible'}), 500
            if response.status_code == 200:
                file_data += response.content
            else:
                return jsonify({'error': 'Archivo no encontrado'}), 404
        return file_data

if __name__ == '__main__':
    app.run(port=5000)


        # for i, datanode_info in metadatos[filename].items():
        #     primary_datanode = datanode_info['leader']
        #     follower_datanode = datanode_info['follower']

        #     response = requests.get(f'{primary_datanode}/block/{filename}_block{i}')
        #     if response.status_code != 200:
        #         response = requests.get(f'{follower_datanode}/block/{filename}_block{i}')

        #     if response.status_code == 200:
        #         file_data += response.content