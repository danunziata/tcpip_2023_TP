# Smart Green House

Este proyecto proporciona una solución para implementar un Invernadero Inteligente utilizando tecnología IoT.

## Requisitos

1. Cuenta en ThingsBoard: Para utilizar la plataforma ThingsBoard, se requiere crear una cuenta en su sitio web o utilizar una instancia local. Proporciona una plataforma IoT para la gestión de dispositivos y la visualización de datos.

2. Cuenta en Ngrok: Ngrok es utilizado para establecer una conexión segura y remota entre la Raspberry Pi y el servidor en la nube. Se requiere crear una cuenta en Ngrok y obtener un token de autenticación para poder utilizarlo.

3. aspberry Pi 2: La Raspberry Pi 2 es utilizada como la computadora central en el proyecto. Se requiere tener una Raspberry Pi 2 o superior y configurarla adecuadamente para su uso.

4. ESP8266: El ESP8266 es utilizado como el sensor inalámbrico en el proyecto. Se requiere tener un ESP8266 o un dispositivo compatible y configurarlo correctamente para la adquisición de datos.

5. Mosquitto: Mosquitto es un broker de mensajes MQTT utilizado en el proyecto. Se requiere instalar y configurar Mosquitto en la Raspberry Pi para permitir la comunicación entre los dispositivos.

6. Weather API: La API de pronóstico del tiempo es utilizada para obtener datos simulados de temperatura y humedad. Se requiere tener acceso a una API de pronóstico del tiempo compatible y obtener una clave de API para su uso.

7. MicroPython y CPython: MicroPython se utiliza en el ESP8266 para la recolección de datos, mientras que CPython se puede utilizar en la Raspberry Pi para el procesamiento de datos. Se requiere tener conocimientos y experiencia en el uso de MicroPython y CPython para trabajar con los dispositivos.

## Instrucciones de Uso

### Configuración del Servicio Mosquitto

1. Abre el archivo `config.conf` ubicado en la carpeta apps.
2. Modifica los parámetros necesarios para configurar el servicio Mosquitto según tus necesidades.
3. Guarda los cambios realizados en el archivo `config.conf`.

#### Parametros

1. Configuración de acceso de clientes:

- allow_anonymous: Indica si se permite que los clientes se conecten sin un usuario especificado. Puede establecerse como true o false según los requisitos de seguridad.

2. Configuración del puerto del Broker:

- listener: Especifica el número de puerto en el cual el Broker MQTT escuchará las solicitudes de conexión. Debes modificar este valor según tus necesidades.

3. Configuración de la conexión bridge:

- Connection mybridge: Marca el inicio de una nueva conexión bridge.

- address red:puerto: Especifica la dirección IP y, opcionalmente, el puerto del bridge al que se va a conectar. Debes reemplazar "red" con la dirección IP del bridge y "puerto" con el número de puerto correspondiente.

4. Configuración de la conexión remota:

- remote_clientid: Define el ID del cliente para la conexión remota.
- remote_username: Define el nombre de usuario del broker al que se va a conectar.
- remote_password: Define la contraseña del broker al que se va a conectar.

5. Opciones adicionales de configuración:

- try_private: Controla si el bridge intentará indicar al broker remoto que es una conexión bridge en lugar de un cliente. Puedes establecer este valor como true o false según tus necesidades.
- start_type: Controla cómo se inicia la conexión del bridge. En este caso, se establece en "automatic" para que se conecte automáticamente y se reinicie cada 30 segundos.

6. Definición de patrones de temas:

- topic v1/devices/me/rpc/request/+ both 1: Define un patrón de tema que se compartirá entre los dos brokers. Debes modificar este valor según tus necesidades.

### Configuración del Servidor en ThingsBoard

1. Abre el archivo `docker-compose.yml` ubicado en la apps.
2. Edita los parámetros del servidor en ThingsBoard según tus preferencias.
3. Guarda los cambios realizados en el archivo `docker-compose.yml`.

#### Parametros

1. Versión de Docker Compose:

- Asegúrate de que la versión de Docker Compose especificada sea compatible con tu entorno. En este caso, se utiliza la versión '3.0', pero puedes ajustarla según sea necesario.

2. Configuración del servicio mytb:

- restart: always: Esta configuración asegura que el contenedor se reinicie automáticamente en caso de errores o reinicios del sistema.

- image: "thingsboard/tb-postgres": Especifica la imagen utilizada para el contenedor. En este caso, se utiliza la imagen "thingsboard/tb-postgres", pero puedes cambiarla si tienes una imagen personalizada o necesitas una versión específica de ThingsBoard.

3. Puertos expuestos:

Modifica los puertos en la sección ports según tus necesidades. En el ejemplo proporcionado, se exponen los siguientes puertos:

- Puerto 8080 del host se mapea al puerto 9090 del contenedor para acceder a la interfaz web de ThingsBoard.
- Puerto 1883 del host se mapea al puerto 1883 del contenedor para permitir la conectividad MQTT.
- Puerto 7070 del host se mapea al puerto 7070 del contenedor para la conectividad HTTP.
- Puertos 5683-5688 del host se mapean a los puertos 5683-5688/udp del contenedor para permitir la conectividad CoAP.

4. Variables de entorno:

- TB_QUEUE_TYPE: in-memory: Establece el tipo de cola que se utiliza en ThingsBoard. En este caso, se utiliza la opción "in-memory" para una configuración simple. Puedes ajustar esta configuración según tus necesidades específicas.

5. Volúmenes:

- Asegúrate de configurar adecuadamente los volúmenes en la sección volumes para garantizar la persistencia de los datos y los registros. En el ejemplo proporcionado, se utilizan los directorios ~/.mytb-data y ~/.mytb-logs en el host para almacenar los datos y los registros de ThingsBoard, respectivamente. Puedes cambiar estos directorios según tus preferencias.

### Código Base para la Recolección de Datos en el Sensor con C-python

1. Abre el archivo `main-cpython.py` ubicado en la apps.
2. Examina el código y realiza las modificaciones necesarias para adaptarlo a tu entorno y requisitos específicos.
3. Guarda los cambios realizados en el archivo `main-cpython.py`.

#### Parametros

1. Configuración del Broker MQTT:

- host: Dirección IP del servidor MQTT al que el dispositivo debe conectarse.

2. Configuración del cliente MQTT:

- id: Identificador del cliente MQTT.
- topic_rpc: Tema MQTT al que el dispositivo se suscribirá para recibir mensajes de control.
- topic_telemetry: Tema MQTT al que el dispositivo publicará los datos de telemetría.

3. Configuración de la API de pronóstico del tiempo:

- url: URL de la API de pronóstico del tiempo utilizada para obtener los datos simulados de temperatura, humedad y CO2. Si deseas utilizar una API diferente o cambiar la ubicación, debes modificar esta URL.

### Código Base para la Recolección de Datos en el Sensor con micro-python

1. Abre el archivo `main-micropython.py` ubicado en la apps.
2. Examina el código y realiza las modificaciones necesarias para adaptarlo a tu entorno y requisitos específicos.
3. Guarda los cambios realizados en el archivo `main-micropython.py`.

#### Parametros

1. Configuración de la red:

- ssid: Nombre de la red Wi-Fi a la que el dispositivo se debe conectar.
- pw: Contraseña de la red Wi-Fi.

2. Configuración del servidor MQTT:

- mqtt_server: Dirección IP del servidor MQTT al que el dispositivo debe conectarse.
- client_id: Identificador del cliente MQTT.
- topic_rpc: Tema MQTT al que se suscribirá el dispositivo para recibir mensajes de control.
- topic_telemetry: Tema MQTT al que el dispositivo publicará los datos de telemetría.

3. Configuración de la API de pronóstico del tiempo:

- url: URL de la API de pronóstico del tiempo utilizada para obtener los datos simulados de temperatura, humedad y CO2. Si deseas utilizar una API diferente o cambiar la ubicación, debes modificar esta URL.

4. Configuración de la red Wi-Fi:

- sta_if.connect('LabRedes', 'labredes'): Aquí debes reemplazar 'LabRedes' con el nombre de tu red Wi-Fi y 'labredes' con la contraseña correspondiente.

## Contribuciones

Si deseas contribuir a este proyecto, sigue los siguientes pasos:

1. Realiza un fork de este repositorio.
2. Realiza las modificaciones necesarias en tu fork.
3. Envía un pull request con tus cambios.

## Soporte

Si necesitas ayuda o tienes alguna pregunta, no dudes en contactarnos a través la apertura de un problema en este repositorio.
