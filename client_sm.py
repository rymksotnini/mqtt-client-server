import random
import time
import paho.mqtt.client as mqtt
import threading
from datetime import datetime

class SMClient (mqtt.Client):
    def __init__(self):
        self.id=f'python-mqtt-{random.randint(0, 1000)}'
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
    
    def connect(self):
        self.client.connect("localhost", 1883)

    def connect_and_loop(self):
        self.connect()
        self.publish_consommation()
        self.publish_production()
        self.client.loop_forever()

    def publish_consommation(self,consommation=4):
        time.sleep(1)
        result = self.client.publish("consommation",qos=2,payload=str({"id":self.id,"consommation":consommation}))
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{consommation}` to topic consommation")
        else:
            print(f"Failed to send message to topic consommation")
        threading.Timer(60.0*60.0, self.publish_consommation).start()

    def publish_production(self, production=6):
        time.sleep(1)
        result = self.client.publish("production",qos=2,payload=str({"id": self.id, "production":production}))
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{production}` to topic production")
        else:
            print(f"Failed to send message to topic production")
        threading.Timer(60.0*15.0, self.publish_production).start()

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
        client.subscribe("reduction/#")
        client.subscribe("prix/#")

    @staticmethod
    def on_message(client, userdata, msg):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        payload = msg.payload.decode('utf-8')[1:-1]
        id_part,value_part=payload.split(",")
        id_n=id_part.split(":")[1]
        value=value_part.split(":")[1]
        print(f"[{current_time}] Received payload from{id_n} => {msg.topic}: {value}")
