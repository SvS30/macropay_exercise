# Address Book API-Rest

API-Rest de contactos con FastAPI.

### 🚧 Configuración
Luego de clonar el proyecto, necesitara:
- Instalar las dependencias del proyecto (ya sea directamente en su maquina o en un entorno)
    ```
    pip install -r requirements.txt
    ```
- Cree una base de datos en su servicio de MongoDB.
- Importe el archivo `data/data.json` en una colección llamada **contacts**.
- Duplique el archivo `.env.example` y renombre la copia a `.env`
    - Ingrese los datos y credenciales solicitadas.
        ```
        # Entorno en el que correra el proyecto
        APP_ENV=local
        # Host o IP en el que desea levantar el servidor
        APP_HOST=localhost
        # Puerto en el que desea levantar el servidor
        APP_PORT=8000

        # URI de su conexión a MongoDB
        DB_HOST=mongodb://user:pass@host/
        # Puerto en el que esta corriendo su instancia de MongoDB
        DB_PORT=27017
        # Nombre de la base de datos
        DB_NAME=
        ```


### 🌐 Ejecutar
Deberas ejecutar en una bash
```
python main.py
```

### 🧰 Dependencias || plugins
| Name | Version |
| ---- | ---- |
| fastapi | 0.79.0 |
| pydantic | 1.9.2 |
| python-dotenv | 0.20.0 |
| uvicorn | 0.18.2 |