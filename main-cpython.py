import paho.mqtt.client as mqtt     # import client library
import time
import json
import requests

# Funciones Callbacks


def tempActual():
    global temp
    global humedad
    global co2
    url = 'http://api.weatherapi.com/v1/current.json?key=2367a071311c47f684d211141230207&q=Rio Cuarto&aqi=yes'
    response = requests.get(url)
    content = response.json()
    temp = content['current']['temp_c']
    humedad = content['current']['humidity']
    co2 = content['current']['air_quality']['co']


def on_connect(client, userdata, flags, rc):
    if rc == 0:  # Codigo de Error = 0, exitoso
        print("Se Ha Conectado y Estamos listos para operar")
        client.connected_flag = True
    else:  # Nos indica que hay algun error
        print("Bad connection Returned code=", rc)
        client.bad_connection_flag = True


def on_publish(client, userdata, mid):
    print("Datos enviados:", mid)  # Nos confirma que los datos fueron enviados


def on_subscribe(client, userdata, mid, granted_qos):
    print("Suscripciones satisfactorias")  # Suscripciones exitosas


def on_message(client, userdata, message):  # Le indicamos que hacer en cada caso
    global message_received
    time.sleep(1)
    message_received = str(message.payload.decode("utf-8"))
    # Recibimos el mensaje y lo pasamos a JSON
    msg = json.loads(message_received)
    print("received message =", message_received)
    if msg['method'] == "setValue":  # Opcion 1: Cambio en la intensidad de la Luz
        datos = {
            "Lumonosidad": msg["params"]
        }
        serial = json.dumps(datos)
        client.publish(topic_telemetry, serial, qos=1)
    if msg['method'] == "setValue2":  # Opcion 2: Cambio en el Led
        datos = {
            "value": msg["params"]
        }
        serial = json.dumps(datos)
        client.publish(topic_telemetry, serial, qos=1)


def on_disconnect(client, userdata, rc):
    # Cliente desconectado exitosamente
    print("El cliente se ha desconectado exitosamente")


# Flags a utilizar

mqtt.Client.connected_flag = False
mqtt.Client.bad_connection_flag = False

# Parametros A Utilizar

host = "192.168.5.216"  # host del Broker
id = "fede"
topic_rpc = "v1/devices/me/rpc/request/+"
topic_telemetry = "v1/devices/me/telemetry"

# Script Principal

client = mqtt.Client(id)  # Creamos el Objeto

# Asignamos los distintos Funciones a los callbacks

client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_disconnect = on_disconnect

# Comienza el Loop y nos encargamos de la suscripcion y conexion

client.loop_start()  # Empieza el Loop
print("Conectandose al Host:", host)
client.connect(host)  # Conexion al Broker
while not client.connected_flag and not client.bad_connection_flag:  # Esperamos la conexion
    print("Esperando la Conexion...")
    time.sleep(2)
print("Suscribiendome a los topics asignados...")
client.subscribe(topic_rpc, 1)

# Carga de Datos cada 5 Segundos

try:
    while True:
        tempActual()
        datos = {
            "Humedad": humedad,
            "Temperatura": temp,
            "Dioxido de Carbono": co2
        }
        serial = json.dumps(datos)
        client.publish(topic_telemetry, serial, qos=1)
        time.sleep(300)
# Una vez que se apaga el sistema a traves de la interfaz
# Detiene el Loop y realiza la desconexion
except KeyboardInterrupt:
    print("")
    client.disconnect()
    client.loop_stop()
    time.sleep(3)
