import grpc
from concurrent import futures
import dfs_pb2
import dfs_pb2_grpc
import os
import random

users = {
    "admin": "adminpass",
    "user1": "password123"
}

data_nodes = ['localhost:5001', 'localhost:5002', 'localhost:5003']

# Metadatos de archivos
metadatos = {}

# Directorio actual (puedes ajustar según tus necesidades)
user_root_dir = os.getcwd()
current_directory = user_root_dir

class NameNodeServicer(dfs_pb2_grpc.NameNodeServicer):
        def Put(self, request, context):
            filename = request.filename
            content = request.content

            # Divide el archivo en bloques de 1024 bytes
            bloques = [content[i:i + 1024] for i in range(0, len(content), 1024)]
            ubicaciones = {}

            for i, bloque in enumerate(bloques):
                almacenado = False
                nodos_disponibles = list(data_nodes)

                while nodos_disponibles and not almacenado:
                    primary_datanode = random.choice(nodos_disponibles)
                    nodos_disponibles.remove(primary_datanode)
                    block_id = f'{filename}_block{i}'

                    try:
                        # Conexión al DataNode
                        channel = grpc.insecure_channel(primary_datanode)
                        stub = dfs_pb2_grpc.DataNodeStub(channel)
                        store_request = dfs_pb2.StoreBlockRequest(
                            block_id=block_id,
                            data=bloque
                        )
                        store_response = stub.StoreBlock(store_request)
                        ubicaciones[i] = {'leader': primary_datanode, 'follower': None}
                        almacenado = True
                        print(f"Bloque {i} almacenado exitosamente en el líder {primary_datanode}")

                        # Replicación en un follower
                        follower_almacenado = False
                        while nodos_disponibles and not follower_almacenado:
                            follower_datanode = random.choice(nodos_disponibles)
                            nodos_disponibles.remove(follower_datanode)
                            try:
                                channel = grpc.insecure_channel(follower_datanode)
                                stub = dfs_pb2_grpc.DataNodeStub(channel)
                                store_response = stub.StoreBlock(store_request)
                                ubicaciones[i]['follower'] = follower_datanode
                                follower_almacenado = True
                                print(f"Bloque {i} replicado exitosamente en el follower {follower_datanode}")
                            except Exception as e:
                                print(f"Error replicando bloque {i} en el follower {follower_datanode}: {e}")
                    except Exception as e:
                        print(f"Error almacenando bloque {i} en el líder {primary_datanode}: {e}")

                if not almacenado:
                    context.abort(grpc.StatusCode.INTERNAL, f'No se pudo almacenar el bloque {i}')

            metadatos[filename] = ubicaciones
            return dfs_pb2.PutResponse(message=f'{filename} subido con éxito')
        
        def Get(self, request, context):
            filename = request.filename
            if filename in metadatos:
                file_data = b''
                for i, datanode_info in metadatos[filename].items():
                    primary_datanode = datanode_info['leader']
                    follower_datanode = datanode_info['follower']
                    block_id = f'{filename}_block{i}'

                    try:
                        channel = grpc.insecure_channel(primary_datanode)
                        stub = dfs_pb2_grpc.DataNodeStub(channel)
                        get_request = dfs_pb2.GetBlockRequest(block_id=block_id)
                        get_response = stub.GetBlock(get_request)
                        file_data += get_response.data
                    except Exception as e:
                        print(f"Error al obtener bloque {i} de {primary_datanode}: {e}")
                        # Intentar con el follower
                        try:
                            channel = grpc.insecure_channel(follower_datanode)
                            stub = dfs_pb2_grpc.DataNodeStub(channel)
                            get_response = stub.GetBlock(get_request)
                            file_data += get_response.data
                        except Exception as e:
                            print(f"Error también en {follower_datanode}: {e}")
                            context.abort(grpc.StatusCode.INTERNAL, f'Bloque {i} no disponible')
                return dfs_pb2.GetResponse(content=file_data)
            else:
                context.abort(grpc.StatusCode.NOT_FOUND, 'Archivo no encontrado')


    # Implementa los demás métodos: ListFiles, ChangeDirectory, etc.
