# Solución MeliChallenge

En el presente proyecto se realizó el desarrollo de una API para procesar y clasificar bases de datos MySQL. 
Para realizar la correcta instalacion de la API, se debe contar con los pre-requisitos instalados en su maquina, además, se deben seguir los los pasos de la sección Instalación. 

Una vez desplegada la API, se pueden realizar los request mediante http://localhost:8080/ .


## Pre-Requisitos
Antes de realizar la instalación se debe contar con los siguientes requisitos:
- MySQL
- Docker
- Insomnia o Postman

## Instalación

La API fue desarrollada para ser desplegada mediante Docker, con un contenedor de MongoDB acoplado, por lo tanto debera ejecutar los siguientes comandos:

1) Clonar el repositorio.

    ```sh
    git clone https://github.com/paldava/meli_db_clasifier
    ```

2) Creamos la imagen docker de la aplicación; estando en la raiz del proyecto descargado en el paso anterior, ejecutamos el siguiente comando.

    ```sh
    docker build -t meli_db_clasifier .
    ```

3) Crear una red en Docker.

    ```sh
    docker network create meli_network
    ```

4) Correr contenedor de MongoDB en la red creada en el paso anterior.

    ```sh 
    docker run -d -it --network meli_network -e MONGO_INITDB_ROOT_PASSWORD=Me1iCh411enge -e MONGO_INITDB_ROOT_USERNAME=root --name mongodb mongo
    ```
	
5) Correr la API en la red creada en el paso 3).

    ```sh 
    docker run -it -p 8080:8080 --network meli_network --name meli_bd_clasifier meli_bd_clasifier:latest
    ```
	
**NOTA: ** Si estas ejecutando los comandos en Windows y obtienes el siguiente error: `the input device is not a TTY. If you are using mintty, try prefixing the command with 'winpty'`. Agrega `'winpty'` antes del comando que estas ejecutando.
  
## Endpoints

La API cuenta con los siguientes endpoints

### POST /api/v1/database

Mediante este endpoint se persisten los datos de conexión de una base de datos MySQL a escanear.

Metodo: `POST`
Path: `http://localhost:8080/api/v1/database`
Body:
```
    {
	    "host":"127.0.0.1",
	    "port":3306,
	    "username":"root",
	    "password":"Me1iCh411enge"
    }
```

Response Code: `201` en caso de éxito y en caso de error un status code correspondiente al tipo de error.

Response Body:

```
{
    "ID":"jhgr6uiyhg5643df678jhkyy5",
    "Status":"Succesfully Inserted"
}
```	

### GET /api/v1/database

Mediante este endpoint se obtienen los datos de conexión de las base de datos MySQL a escanear que se han guardado.

Metodo: `GET`
Path: `http://localhost:8080/api/v1/database`

Response Code: `200` en caso de éxito y en caso de error un status code correspondiente al tipo de error.

Response Body:

    {
		"collection":"database",
		"host":"127.0.0.1",
		"port":3306,
		"username":"root",
		"password":"Me1iCh411enge"
    }


### POST /api/v1/info_type

Mediante este endpoint se persisten los tipos de información con los que se van a clasificar las columnas en el escaneo de la base de datos.

Metodo: `POST`
Path: `http://localhost:8080/api/v1/info_type`
Body:

    {
		"name":"CREDIT_CARD_NUMBER",
		"regexp":"(credit|card)"
    }

Response Code: `201` en caso de éxito y en caso de error un status code correspondiente al tipo de error.

Response Body:

```
{
    "ID":"jhgr6uiyhg5643df678jhkyy5",
    "Status":"Succesfully Inserted"
}
```	

### GET /api/v1/info_type

Mediante este endpoint se obtienen los tipos de información con los que se van a clasificar las columnas en el escaneo de la base de datos.

Metodo: `GET`
Path: `http://localhost:8080/api/v1/database`

Response Code: `200` en caso de éxito y en caso de error un status code correspondiente al tipo de error.

Response Body:

    {
		"collection":"database",
		"host":"127.0.0.1",
		"port":3306,
		"username":"root",
		"password":"Me1iCh411enge"
    }
	
### POST /api/v1/database/:id

Mediante este endpoint se ejecuta la clasificación de una base de datos dado un id asociado a la misma.

Metodo: `POST`
Path: `http://localhost:8080/api/v1/database/jhgr6uiyhg5643df678jhkyy5`


Response Code: `201` en caso de éxito y en caso de error un status code correspondiente al tipo de error

### GET /api/v1/database/scan/:id

Mediante este endpoint se obtiene la estructura y clasificación del ultimo escaneo realizado de una base de datos dado un id asociado a la misma.

Metodo: `GET`
Path: `http://localhost:8080/api/v1/database/scan/jhgr6uiyhg5643df678jhkyy5`

Response Code: `200` en caso de éxito y en caso de error un status code correspondiente al tipo de error.

Response Body:

    {
		"collection" : "structure",
		"database_id" : "jhgr6uiyhg5643df678jhkyy5",
		"scan_date" : "2020-12-21, 10:15:52",
		"squemas" : [
			{
				"name" : "meli_db_clasifier",
				"tables" : [
					{
						"name" : "users",
						"columns" : [
							{
								"name" : "NAME",
								"information_type" : "N/A",
								"data_type" : "VARCHAR(200)"
							}
							...
						]
					}
					...
				]
			}
			...
		]
    }