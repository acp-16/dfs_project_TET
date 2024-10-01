# TÓPICOS TELEMÁTICA - ST0263

## Estudiantes: 
- Antonio Carbonó Pedroza, hacarbonop@eafit.edu.co
- David Elias Franco Vélez, defrancov@eafit.edu.co
- Daniel Vélez Duque, dvelezd2@eafit.edu.co  
- Juan José Villada Calle, jjvilladac@eafit.edu.co

## Profesor: 
- Alvaro Enrique Ospina Sanjuan, aeospinas@eafit.edu.co

## 1. Descripción
Este proyecto se centra en la implementación de un sistema de archivos distribuido (DFS) orientado a bloques, inspirado en sistemas como GFS (Google File System). Una característica clave de este DFS es la funcionalidad WORM (Write Once Read Many), que se toma del almacenamiento por objetos. El DFS está diseñado para permitir la lectura y escritura eficiente de archivos distribuidos entre varios DataNodes, mientras que un NameNode lidera la coordinación y distribución de bloques de datos.

### 1.1. Aspectos Cumplidos (Requerimientos Funcionales y No Funcionales)
- **Distribución de Bloques**: Cada archivo es dividido en bloques y distribuido en varios `DataNodes`, con un mínimo de replicación para garantizar la disponibilidad.
- **Canales de Comunicación**: Se implementan dos tipos de canales: uno para el control (`NameNode y DataNode`) y otro para la transferencia de datos (`Cliente y DataNode`).
- **NameNode Líder y Follower**: El sistema incluye un `NameNode` principal encargado de la asignación de bloques, mientras que un `NameNode` secundario actúa como respaldo en caso de fallos.
- **CLI/API/SDK**: Los clientes pueden interactuar con el sistema mediante una interfaz de línea de comandos (CLI) o mediante API/SDK, permitiendo la escritura, lectura y borrado de archivos.
- **Despliegue en AWS:** Se logró realizar el despliegue en `AWS`, garantizando el uso de IPs elásticas.

### 1.2. Aspectos No Cumplidos
No hubo aspectos mayores con los que el proyecto no haya cumplido, se cumplió con todos los requisitos.

## 2.  Información General de Diseño de Alto Nivel
El sistema de archivos distribuido sigue una arquitectura maestro-esclavo, donde el NameNode lidera la distribución de bloques y coordina las réplicas entre los DataNodes. Los clientes se comunican directamente con los DataNodes para leer y escribir archivos, mientras que las decisiones de asignación de bloques son gestionadas por el NameNode. El NameNode mantiene una tabla de metadatos con la ubicación de cada bloque y los DataNodes responsables de su almacenamiento.

### 2.1 Arquitectura
- **`NameNode`**: Encargado de gestionar la ubicación de los bloques de archivos y la replicación entre DataNodes. También maneja las solicitudes de los clientes para lectura y escritura de archivos.
- **`DataNode`**: Almacena los bloques de archivos, y se sincroniza con otros DataNodes para mantener réplicas consistentes.
- **`Cliente CLI`**: Permite al usuario realizar operaciones de subida, descarga, y consulta de archivos en el DFS.

### 2.2 Protocolos de Comunicación
- **Canal de Control**: Comunicación entre NameNode y DataNodes para la coordinación de replicación y asignación de bloques.
- **Canal de Datos**: Comunicación directa entre el Cliente y los DataNodes para la lectura y escritura de archivos.

## 3. Descripción del Ambiente de Desarrollo
El desarrollo de este proyecto se realizó utilizando tecnologías como Python y herramientas de simulación de sistemas distribuidos.

### 3.1 Tecnologías y Versiones:
- `Python`: 3.8
- `Flask`: 2.1.1 (para API REST)
- `requests`:  2.25.1 (para solicitudes HTTP)
- `flask-httpauth`:  4.2.0 (para autenticación)
 
### 3.2 Detalles Técnicos
- **Archivo de Configuración**: El archivo `requirements.txt` especifica las dependencias del proyecto.
- **Dockerfile**: Se provee un `Dockerfile` para contenerizar la aplicación y asegurar que todos los componentes se desplieguen correctamente en cualquier entorno.
- **Archivo de Entrada**: `entrypoint.py` sirve como punto de entrada para iniciar el sistema.
- **Cliente CLI**: `client_cli.py` permite interactuar con el sistema de archivos.
  
#### 3.2.1 Estructura del Proyetco:
  ```
  ├── Dockerfile
  ├── README.md
  ├── archivo.txt
  ├── client_cli.py
  ├── data_node.py
  ├── entrypoint.py
  ├── name_node.py
  └── requirements.txt
  ```

## 4. Guía de Uso

### 4.1 Instalación y Dependencias
Para instalar las dependencias, ejecute el siguiente comando dentro del directorio del proyecto:
  ```
  RUN pip install --no-cache-dir --upgrade pip
  RUN pip install --no-cache-dir -r /app/requirements.txt
  ```
### 4.2 Ejecución del Proyecto
#### 4.2.1 Iniciar el NameNode
El `NameNode` es el coordinador principal. Para iniciarlo, ejecute el siguiente comando:
  ```
  python name_node.py --port 5000
  ```
#### 4.2.2 Iniciar los DataNodes
Para iniciar los `DataNodes`, ejecute en terminales separadas:
  ```
  python data_node.py --port [PUERTO]
  ```
  el puerto puede ser 5001, 5002 o 5003 dependiendo si es el data_node1, data_node2 o data_node3
  
#### 4.2.3 Usar el Cliente CLI
El `cliente CLI` permite interactuar con el sistema para subir, descargar y consultar archivos.
  ```
  python client_cli.py
  ```
Los comandos disponibles en el cliente son:
- **`put <file>`**: Sube un archivo al DFS.
- **`get <file>`**: Descarga un archivo del DFS.
- **`rm <file>`**: Elimina un archivo del DFS.
- **`ls`**: Lista los archivos disponibles en el DFS.
- **`cd <directory>`**: Cambia al directorio especificado dentro del DFS.
- **`mkdir <directory>`**: Crea un nuevo directorio en el DFS.
- **`rmdir <directory>`**: Elimina un directorio vacío del DFS.

### 4.3 Uso con Docker
#### 4.3.1 `NameNode`: 
El proyecto puede ser ejecutado en contenedores `Docker`. Para construir la imagen del NameNode, ejecute:
  ```
  sudo docker build -t dfs_project_image .
  ```
Y luego, para ejecutar el contenedor:
  ```
  sudo docker run -d -p 5000:5000 -e ROLE=namenode dfs_project_image
  ```
#### 4.3.2 `DataNode`:
Para la imagen de cada DataNode, ejecutar
  ```
  sudo docker build -t dfs_project_image .
  ```
Y luego, dependiendo el puerto, ejecutar: (en este caso se muestra el 5001, pero puede ser 5002 o 5003)
  ```
  sudo docker run -d -p 5001:5001 -e ROLE=datanode -e DATANODE_PORT=5001 dfs_project_image
  ```

### 4.4. Imágenes del Proyecto
![1](https://github.com/user-attachments/assets/ff6fae7c-3d33-4692-94d2-c2a9e58b7135)
![2](https://github.com/user-attachments/assets/7ad8403b-bfa8-4d24-82b8-d29fad464710)
![3](https://github.com/user-attachments/assets/8ebcb896-a20f-4a67-83da-6d7175f5d636)
![4](https://github.com/user-attachments/assets/267e2cf5-0c50-40ff-9569-dae83443765e)

### 4.5 [Video](https://drive.google.com/file/d/1kgXeLMJ-qyoylkpxjmVsMAUmofE4BtMU/view?usp=sharing)
 
## 5. Referencias:
- Ghemawat, S., Gobioff, H., & Leung, S.-T. (2003). The Google file system. ACM SIGOPS Operating Systems Review, 37(5), 29-43.
- [Flask Documentation](https://flask.palletsprojects.com)
