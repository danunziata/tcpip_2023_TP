# Mosquitto Broker

Eclipse Mosquitto is an open source (EPL/EDL licensed) message broker that implements the MQTT protocol versions 5.0, 3.1.1 and 3.1. Mosquitto is lightweight and is suitable for use on all devices from low power single board computers to full servers. 

## Instalacion del servicio

Para poder utilizar el servicio debemos instalarlo en nuestro servidor

```
sudo apt-get update
sudo apt-get install mosquitto
sudo apt-get install mosquitto-clients
```

## Archivo de configuracion

Este archivo contiene todas las funcionalidades que se van a activar en el broker para su utilizacion

```
#permite a los clientes sin usuario conectarse
allow_anonymous true
#puerto el cual escucha peticiones el broker
listener 1883
 
#marca el inicio de una nueva conexión bridge
Connection mybridge
#Especifica la dirección y opcionalmente el puerto del bridge al que se va a conectar
address red:puerto

 
#Define el id del cliente para la conexión
remote_clientid admin
#Define el usuario del broker a conectarse
remote_username fede
#Define la contraseña del broker a conectarse
remote_password 123
#El bridge le intentará indicar al broker remoto que es un conexion bridge y no un cliente, pero como no queremos eso lo ponemos en false
try_private false
#Controla como inicia la conexion el bridge, en este caso se conecta automáticamente y se reinicia cada 30 segundos
start_type automatic
 

#Define los patrones de temas que se compartirán entre los 2 brokers.
topic v1/devices/me/rpc/request/+ both 1
topic # both 1
```

## Inicio del servicio

Para comenzar y monitoriar el servicio broker utilizamos el siguiente comando

```
mosquitto -v -c /etc/mosquitto/conf.d/config.conf
```