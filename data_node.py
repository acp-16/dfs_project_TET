import grpc
from concurrent import futures
import dfs_pb2
import dfs_pb2_grpc
import os
import argparse

# Clase que implementa el servicio DataNode
class DataNodeServicer(dfs_pb2_grpc.DataNodeServicer):
    def StoreBlock(self, request, context):
        try:
            block_id = request.block_id
            data = request.data

            with open(os.path.join(DATA_DIR, block_id), 'wb') as f:
                f.write(data)

            return dfs_pb2.StoreBlockResponse(message='Bloque almacenado correctamente')
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f'Error al almacenar el bloque: {str(e)}')

    def GetBlock(self, request, context):
        try:
            block_id = request.block_id
            block_path = os.path.join(DATA_DIR, block_id)

            if os.path.exists(block_path):
                with open(block_path, 'rb') as f:
                    data = f.read()
                return dfs_pb2.GetBlockResponse(data=data)
            else:
                context.abort(grpc.StatusCode.NOT_FOUND, 'Bloque no encontrado')
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f'Error al obtener el bloque: {str(e)}')

# Función para iniciar el servidor
def serve():
    parser = argparse.ArgumentParser(description='Iniciar un DataNode en un puerto específico.')
    parser.add_argument('--port', type=int, default=5001, help='El puerto en el que se ejecutará el DataNode')
    args = parser.parse_args()

    global DATA_DIR
    DATA_DIR = f'./data{args.port}'
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dfs_pb2_grpc.add_DataNodeServicer_to_server(DataNodeServicer(), server)
    server.add_insecure_port(f'[::]:{args.port}')
    server.start()
    print(f"DataNode gRPC server iniciado en el puerto {args.port}")
    server.wait_for_termination()

# Punto de entrada del script
if __name__ == '__main__':
    serve()
