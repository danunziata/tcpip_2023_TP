# ThingsBoard

ThingsBoard is an open-source IoT platform for data collection, processing, visualization, and device management. It enables device connectivity via industry standard IoT protocols - MQTT, CoAP and HTTP and supports both cloud and on-premises deployments. ThingsBoard combines scalability, fault-tolerance and performance so you will never lose your data.

## Instalacion del servicio

Para instalar el servidor hacemos uso de la plataforma Docker que es una plataforma de contenedores que permite la creación, distribución y ejecución de aplicaciones de forma eficiente y portátil. Proporciona un entorno aislado para cada aplicación, facilitando la gestión y la escalabilidad de los servicios, sin depender del sistema operativo subyacente. Utilizaremos docker compose por lo tanto haremos uso del archivo de configuracion en formato .yml

```
version: '3.0'
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

```
mkdir -p ~/.mytb-data && sudo chown -R 799:799 ~/.mytb-data
mkdir -p ~/.mytb-logs && sudo chown -R 799:799 ~/.mytb-logs
```

Para ponerlo en funcionamiento ejecutamos los comandos

```
docker compose up -d
docker compose logs -f mytb
```
