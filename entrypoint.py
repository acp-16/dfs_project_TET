import os
import sys
import subprocess

# Determina si es NameNode o DataNode a partir de la variable de entorno
role = os.getenv('ROLE')

if role == 'namenode':
    print("Iniciando NameNode...")
    subprocess.run(["python", "name_node.py"])
elif role == 'datanode':
    port = os.getenv('DATANODE_PORT', '5001')  # El puerto puede venir de la variable de entorno, por defecto 5001
    print(f"Iniciando DataNode en el puerto {port}...")
    subprocess.run(["python", "data_node.py", "--port", port])
else:
    print("Por favor, establece la variable de entorno ROLE como 'namenode' o 'datanode'.")
    sys.exit(1)
