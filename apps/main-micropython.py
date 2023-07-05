import gc
import network
import time
import machine
import urequests
import json
import uasyncio
from umqttsimple import MQTTClient
import esp
esp.osdebug(None)
gc.collect()

# Funcion para obtener los datos de temperatura, humedad y co2


def datosActual():
    global temp
    global humedad
    global co2
    url = 'http://api.weatherapi.com/v1/current.json?key=2367a071311c47f684d211141230207&q=Rio_Cuarto&aqi=yes'
    response = urequests.get(url)
    content = response.json()
    temp = content['current']['temp_c']
    humedad = content['current']['humidity']
    co2 = content['current']['air_quality']['co']

# Funcion que va a tratar los datos recibidos


def sub_cb(topic, msg):
    global message_received
    time.sleep(1)
    message_received = str(msg.decode("utf-8"))
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

# Conexion y suscripcion


def connect_and_subscribe():
    global client_id, mqtt_server, topic_rpc
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_rpc, qos=1)
    print('Connected to %s MQTT broker, subscribed to %s topic' %
          (mqtt_server, topic_rpc))
    return client

# En caso de fallo...


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

# Definimos las 2 tareas las cuales son:
# Envio periodico de datos
# Procesamiento y envio de comprobacion


async def waitmsg(delay):
    while True:
        client.check_msg()
        await uasyncio.sleep(delay)


async def main():

    uasyncio.create_task(waitmsg(1))

    while True:
        try:
            datosActual()
            datos = {
                "Humedad": humedad,
                "Temperatura": temp,
                "Dioxido de Carbono": co2
            }
            serial = json.dumps(datos)
            client.publish(topic_telemetry, serial)
        except OSError as e:
            restart_and_reconnect()
        await uasyncio.sleep(10)

# Nos conectamos a la red

ssid = "LabRedes"
pw = "labredes"

mqtt_server = "192.168.5.216"
client_id = "fede"
topic_rpc = "v1/devices/me/rpc/request/+"
topic_telemetry = "v1/devices/me/telemetry"


sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.connect('LabRedes', 'labredes')
    while not sta_if.isconnected():
        pass
print('network config:', sta_if.ifconfig())

# Conectamos al broker

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

# Inicializamos las tareas

try:
    uasyncio.run(main())
except KeyboardInterrupt:
    print("")
    client.disconnect()
    print("El cliente se ha desconectado exitosamente")
    time.sleep(5)
