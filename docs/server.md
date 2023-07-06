## ThingsBoard

## Introduccion

ThingsBoard es una plataforma IoT de código abierto para la recolección, procesamiento, visualización y gestión de dispositivos. Permite la conectividad de dispositivos a través de protocolos estándar de IoT como MQTT, CoAP y HTTP, y admite implementaciones tanto en la nube como en local. ThingsBoard combina escalabilidad, tolerancia a fallos y rendimiento para que nunca pierdas tus datos.

### Instalacion del servicio

Para instalar el servidor hacemos uso de la plataforma Docker que es una plataforma de contenedores que permite la creación, distribución y ejecución de aplicaciones de forma eficiente y portátil. Proporciona un entorno aislado para cada aplicación, facilitando la gestión y la escalabilidad de los servicios, sin depender del sistema operativo subyacente. Utilizaremos docker compose por lo tanto haremos uso del archivo de configuracion en formato .yml

```yml
version: "3.0"
services:
  mytb:
    restart: always
    image: "thingsboard/tb-postgres"
    ports:
      - "8080:9090"
      - "1883:1883"
      - "7070:7070"
      - "5683-5688:5683-5688/udp"
    environment:
      TB_QUEUE_TYPE: in-memory
    volumes:
      - ~/.mytb-data:/data
      - ~/.mytb-logs:/var/log/thingsboard
```

Necesitamos tambien crear carpetas que contengan los datos y logs del sistema

```sh
mkdir -p ~/.mytb-data && sudo chown -R 799:799 ~/.mytb-data
mkdir -p ~/.mytb-logs && sudo chown -R 799:799 ~/.mytb-logs
```

Para ponerlo en funcionamiento ejecutamos los comandos:

```sh
docker compose up -d
docker compose logs -f mytb
```

## Ngrok

Ngrok es una herramienta que permite crear túneles seguros desde internet hacia una red local. Actúa como un intermediario entre la red pública y una computadora local, permitiendo acceder a servicios y aplicaciones alojados localmente desde cualquier lugar. Ngrok asigna una URL única que redirige el tráfico externo a través de un canal seguro hasta el servidor local. Esto facilita la exposición de servicios locales para pruebas, demostraciones o acceso remoto. Ngrok es ampliamente utilizado en desarrollo web, pruebas de aplicaciones y en entornos de colaboración remota.

### Instalacion del servicio

Para realizar un tunel debemos crear una cuenta e instalar el servicio en el servidor con el comando:

```
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
```

Una vez realizamos la autentificacion en el servicio
```
ngrok config add-authtoken <token>
```

Utilizamos un archivo de configuracion para poder crear 1 tunel con 2 servicios simultaneos, uno para la interfaz grafica y otra para la comunicacion por MQTT
```

```

Por ultimo, ponemos en marcha el servicio

```
ngrok start -all
```
