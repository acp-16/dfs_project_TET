import click
import requests
import os
from requests.auth import HTTPBasicAuth

NAME_NODE_URL = "http://localhost:5000"

@click.group()
def cli():
    """CLI para interactuar con el DFS."""
    pass

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

if __name__ == '__main__':
    cli()