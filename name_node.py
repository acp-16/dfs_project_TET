import grpc
from concurrent import futures
import dfs_pb2
import dfs_pb2_grpc
import os
import random

# Variables globales
user_root_dir = os.getcwd()
current_directory = user_root_dir

# Simulación de autenticación (puedes ajustar esto según tus necesidades)
users = {
    "admin": "adminpass",
    "user1": "password123"
}

# Lista de DataNodes (actualiza con tus direcciones gRPC)
data_nodes = ['localhost:5001', 'localhost:5002', 'localhost:5003']

# Metadatos
metadatos = {}

# Implementación del servicio NameNode
class NameNodeServicer(dfs_pb2_grpc.NameNodeServicer):
    def UploadFile(self, request, context):
        # === Inicio de la sección de autenticación ===
        # Convertimos los metadatos en un diccionario para acceder a ellos por clave
        metadata = dict(context.invocation_metadata())
        username = metadata.get('username')
        password = metadata.get('password')

        # Verificamos que el nombre de usuario y contraseña sean válidos
        if not username or not password or users.get(username) != password:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Credenciales inválidas')
        # === Fin de la sección de autenticación ===

        filename = request.filename
        content = request.content

        # Dividir el archivo en bloques de 1024 bytes
        bloques = [content[i:i + 1024] for i in range(0, len(content), 1024)]
        ubicaciones = {}

        for i, bloque in enumerate(bloques):
            almacenado = False
            nodos_disponibles = list(data_nodes)

            while nodos_disponibles and not almacenado:
                try:
                    primary_datanode = random.choice(nodos_disponibles)
                    nodos_disponibles.remove(primary_datanode)

                    block_id = f'{filename}_block{i}'

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
        return dfs_pb2.UploadFileResponse(message=f'{filename} subido con éxito')

    def DownloadFile(self, request, context):
        # === Inicio de la sección de autenticación ===
        metadata = dict(context.invocation_metadata())
        username = metadata.get('username')
        password = metadata.get('password')

        if not username or not password or users.get(username) != password:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Credenciales inválidas')
        # === Fin de la sección de autenticación ===

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
            return dfs_pb2.DownloadFileResponse(content=file_data)
        else:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Archivo no encontrado')

    def Ls(self, request, context):
        # === Inicio de la sección de autenticación ===
        metadata = dict(context.invocation_metadata())
        username = metadata.get('username')
        password = metadata.get('password')

        if not username or not password or users.get(username) != password:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Credenciales inválidas')
        # === Fin de la sección de autenticación ===

        try:
            files = os.listdir(current_directory)
            return dfs_pb2.ListFilesResponse(files=files)
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f'Error al listar archivos: {str(e)}')

    def Cd(self, request, context):
        # === Inicio de la sección de autenticación ===
        metadata = dict(context.invocation_metadata())
        username = metadata.get('username')
        password = metadata.get('password')

        if not username or not password or users.get(username) != password:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Credenciales inválidas')
        # === Fin de la sección de autenticación ===

        global current_directory
        directory = request.directory
        new_directory = os.path.join(current_directory, directory)

        if os.path.isdir(new_directory):
            current_directory = new_directory
            return dfs_pb2.DirectoryResponse(message=f'Cambiado a {new_directory}')
        else:
            context.abort(grpc.StatusCode.NOT_FOUND, f'El directorio {directory} no existe')

    def Mkdir(self, request, context):
        # === Inicio de la sección de autenticación ===
        metadata = dict(context.invocation_metadata())
        username = metadata.get('username')
        password = metadata.get('password')

        if not username or not password or users.get(username) != password:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Credenciales inválidas')
        # === Fin de la sección de autenticación ===

        directory = request.directory
        target_directory = os.path.join(current_directory, directory)

        try:
            os.makedirs(target_directory)
            return dfs_pb2.DirectoryResponse(message=f'Directorio {directory} creado')
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f'Error al crear directorio: {str(e)}')

    def Rmdir(self, request, context):
        # === Inicio de la sección de autenticación ===
        metadata = dict(context.invocation_metadata())
        username = metadata.get('username')
        password = metadata.get('password')

        if not username or not password or users.get(username) != password:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Credenciales inválidas')
        # === Fin de la sección de autenticación ===

        directory = request.directory
        target_directory = os.path.join(current_directory, directory)

        try:
            os.rmdir(target_directory)
            return dfs_pb2.DirectoryResponse(message=f'Directorio {directory} eliminado')
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f'Error al eliminar directorio: {str(e)}')

    def Rm(self, request, context):
        # === Inicio de la sección de autenticación ===
        metadata = dict(context.invocation_metadata())
        username = metadata.get('username')
        password = metadata.get('password')

        if not username or not password or users.get(username) != password:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Credenciales inválidas')
        # === Fin de la sección de autenticación ===

        filename = request.filename
        file_path = os.path.join(current_directory, filename)

        try:
            os.remove(file_path)
            return dfs_pb2.FileResponse(message=f'Archivo {filename} eliminado')
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f'Error al eliminar archivo: {str(e)}')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dfs_pb2_grpc.add_NameNodeServicer_to_server(NameNodeServicer(), server)
    server.add_insecure_port('[::]:5000')  # Puerto donde correrá el NameNode
    server.start()
    print("NameNode gRPC server iniciado en el puerto 5000")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
