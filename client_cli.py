import click
import grpc
import dfs_pb2
import dfs_pb2_grpc
import os

NAME_NODE_ADDRESS = 'localhost:5000'  # Actualiza la dirección si es necesario

def get_stub():
    channel = grpc.insecure_channel(NAME_NODE_ADDRESS)
    stub = dfs_pb2_grpc.NameNodeStub(channel)
    return stub

@click.group()
def cli():
    """CLI para interactuar con el DFS."""
    pass

@cli.command()
@click.argument('filename')
@click.option('--username', prompt=True, help='Nombre de usuario')
@click.option('--password', prompt=True, hide_input=True, help='Contraseña')
def upload(filename, username, password):
    """Sube un archivo al DFS."""
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            content = f.read()

        stub = get_stub()
        metadata = [('username', username), ('password', password)]
        request = dfs_pb2.UploadFileRequest(filename=filename, content=content)
        try:
            response = stub.UploadFile(request, metadata=metadata)
            click.echo(response.message)
        except grpc.RpcError as e:
            click.echo(f'Error: {e.details()}')
    else:
        click.echo(f'El archivo {filename} no existe')

@cli.command()
@click.argument('filename')
@click.option('--username', prompt=True, help='Nombre de usuario')
@click.option('--password', prompt=True, hide_input=True, help='Contraseña')
def download(filename, username, password):
    """Descarga un archivo del DFS."""
    stub = get_stub()
    metadata = [('username', username), ('password', password)]
    request = dfs_pb2.DownloadFileRequest(filename=filename)
    try:
        response = stub.DownloadFile(request, metadata=metadata)
        with open(filename, 'wb') as f:
            f.write(response.content)
        click.echo(f'Archivo {filename} descargado con éxito')
    except grpc.RpcError as e:
        click.echo(f'Error: {e.details()}')

@cli.command()
@click.option('--username', prompt=True, help='Nombre de usuario')
@click.option('--password', prompt=True, hide_input=True, help='Contraseña')
def ls(username, password):
    """Lista archivos y directorios en el DFS."""
    stub = get_stub()
    metadata = [('username', username), ('password', password)]
    request = dfs_pb2.Empty()
    try:
        response = stub.Ls(request, metadata=metadata)
        click.echo('Contenido:')
        for item in response.files:
            click.echo(f'- {item}')
    except grpc.RpcError as e:
        click.echo(f'Error: {e.details()}')

@cli.command()
@click.argument('directory')
@click.option('--username', prompt=True, help='Nombre de usuario')
@click.option('--password', prompt=True, hide_input=True, help='Contraseña')
def cd(directory, username, password):
    """Cambia de directorio en el DFS."""
    stub = get_stub()
    metadata = [('username', username), ('password', password)]
    request = dfs_pb2.CdRequest(directory=directory)
    try:
        response = stub.Cd(request, metadata=metadata)
        click.echo(response.message)
    except grpc.RpcError as e:
        click.echo(f'Error: {e.details()}')

@cli.command()
@click.argument('directory')
@click.option('--username', prompt=True, help='Nombre de usuario')
@click.option('--password', prompt=True, hide_input=True, help='Contraseña')
def mkdir(directory, username, password):
    """Crea un nuevo directorio en el DFS."""
    stub = get_stub()
    metadata = [('username', username), ('password', password)]
    request = dfs_pb2.MkdirRequest(directory=directory)
    try:
        response = stub.Mkdir(request, metadata=metadata)
        click.echo(response.message)
    except grpc.RpcError as e:
        click.echo(f'Error: {e.details()}')

@cli.command()
@click.argument('directory')
@click.option('--username', prompt=True, help='Nombre de usuario')
@click.option('--password', prompt=True, hide_input=True, help='Contraseña')
def rmdir(directory, username, password):
    """Elimina un directorio en el DFS."""
    stub = get_stub()
    metadata = [('username', username), ('password', password)]
    request = dfs_pb2.RmdirRequest(directory=directory)
    try:
        response = stub.Rmdir(request, metadata=metadata)
        click.echo(response.message)
    except grpc.RpcError as e:
        click.echo(f'Error: {e.details()}')

@cli.command()
@click.argument('filename')
@click.option('--username', prompt=True, help='Nombre de usuario')
@click.option('--password', prompt=True, hide_input=True, help='Contraseña')
def rm(filename, username, password):
    """Elimina un archivo en el DFS."""
    stub = get_stub()
    metadata = [('username', username), ('password', password)]
    request = dfs_pb2.RmRequest(filename=filename)
    try:
        response = stub.Rm(request, metadata=metadata)
        click.echo(response.message)
    except grpc.RpcError as e:
        click.echo(f'Error: {e.details()}')

if __name__ == '__main__':
    cli()
