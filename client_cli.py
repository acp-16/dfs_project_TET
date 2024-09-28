import click
import requests
import os
from requests.auth import HTTPBasicAuth

NAME_NODE_URL = "http://localhost:5000"

@click.group()
def cli():
    """CLI para interactuar con el DFS."""
    pass


# Comando para subit un archivo al DFS
@cli.command()
@click.argument('filename')
@click.option('--username', prompt=True, help='Nombre de usuario')
@click.option('--password', prompt=True, hide_input=True, help='Contraseña')
def put(filename, username, password):
    """Sube un archivo al DFS."""
    if os.path.exists(filename):
        files = {'file': open(filename, 'rb')}
        auth = HTTPBasicAuth(username, password)
        response = requests.post(f'{NAME_NODE_URL}/put', files=files, auth=auth)
        if response.status_code == 200:
            click.echo(f'Archivo {filename} subido con éxito')
        else:
            click.echo('Error al subir el archivo')
    else:
        click.echo(f'El archivo {filename} no existe')


# Comando para descargar un archivo del DFS
@cli.command()
@click.argument('filename')
@click.option('--username', prompt=True, help='Nombre de usuario')
@click.option('--password', prompt=True, hide_input=True, help='Contraseña')
def get(filename, username, password):
    """Descarga un archivo del DFS."""
    auth = HTTPBasicAuth(username, password)
    response = requests.get(f'{NAME_NODE_URL}/get/{filename}', auth=auth)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        click.echo(f'Archivo {filename} descargado con éxito')
    else:
        click.echo('Error al descargar el archivo')
        

# Comando para listar archivos y directorios en el DFS
@cli.command()
@click.option('--username', prompt=True, help='Nombre de usuario')
@click.option('--password', prompt=True, hide_input=True, help='Contraseña')
def ls(username, password):
    """Lista archivos y directorios en el DFS."""
    auth = HTTPBasicAuth(username, password)
    response = requests.get(f'{NAME_NODE_URL}/ls', auth=auth)
    if response.status_code == 200:
        click.echo(f'Contenido: {response.json()}')
    else:
        click.echo('Error al listar el contenido')

# Comando para cambiar de directorio en el DFS
@cli.command()
@click.argument('directory')
@click.option('--username', prompt=True, help='Nombre de usuario')
@click.option('--password', prompt=True, hide_input=True, help='Contraseña')
def cd(directory, username, password):
    """Cambia de directorio en el DFS."""
    auth = HTTPBasicAuth(username, password)
    response = requests.post(f'{NAME_NODE_URL}/cd', json={'directory': directory}, auth=auth)
    if response.status_code == 200:
        click.echo(f'Directorio cambiado a {directory}')
    else:
        click.echo(f'Error al cambiar de directorio a {directory}')


# Comando para crear un nuevo directorio en el DFS

@cli.command()
@click.argument('directory')
@click.option('--username', prompt=True, help='Nombre de usuario')
@click.option('--password', prompt=True, hide_input=True, help='Contraseña')
def mkdir(directory, username, password):
    """Crea un nuevo directorio en el DFS."""
    auth = HTTPBasicAuth(username, password)
    response = requests.post(f'{NAME_NODE_URL}/mkdir', json={'directory': directory}, auth=auth)
    if response.status_code == 200:
        click.echo(f'Directorio {directory} creado')
    else:
        click.echo(f'Error al crear el directorio {directory}')


# Comando para eliminar un directorio en el DFS

@cli.command()
@click.argument('directory')
@click.option('--username', prompt=True, help='Nombre de usuario')
@click.option('--password', prompt=True, hide_input=True, help='Contraseña')
def rmdir(directory, username, password):
    """Elimina un directorio en el DFS."""
    auth = HTTPBasicAuth(username, password)
    response = requests.post(f'{NAME_NODE_URL}/rmdir', json={'directory': directory}, auth=auth)
    if response.status_code == 200:
        click.echo(f'Directorio {directory} eliminado')
    else:
        click.echo(f'Error al eliminar el directorio {directory}')


# Comando para eliminar un archivo en el DFS

@cli.command()
@click.argument('filename')
@click.option('--username', prompt=True, help='Nombre de usuario')
@click.option('--password', prompt=True, hide_input=True, help='Contraseña')
def rm(filename, username, password):
    """Elimina un archivo en el DFS."""
    auth = HTTPBasicAuth(username, password)
    response = requests.post(f'{NAME_NODE_URL}/rm', json={'filename': filename}, auth=auth)
    if response.status_code == 200:
        click.echo(f'Archivo {filename} eliminado')
    else:
        click.echo(f'Error al eliminar el archivo {filename}')


if __name__ == '__main__':
    cli()