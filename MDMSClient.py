import random
import time
import paho.mqtt.client as mqtt
import sched, time
import threading
from datetime import datetime

class MDMSClient (mqtt.Client):

    def __init__(self):
        self.id=f'python-mqtt-{random.randint(0, 1000)}'
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connection to MQTT Broker was a success!")
        else:
            print("Connection failure with return code %d\n", rc)
        client.subscribe("production/#")
        client.subscribe("consommation/#")

    @staticmethod
    def on_message(client, userdata, msg):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        payload = msg.payload.decode('utf-8')[1:-1]
        id_part,value_part=payload.split(",")
        id_n=id_part.split(":")[1]
        value=value_part.split(":")[1]
        print(f"[{current_time}] Received payload from{id_n} => {msg.topic}: {value}")

    def publish_prix(self,prix=10):
        result = self.client.publish("prix",qos=1, payload=str({"id": self.id, "prix":prix}))
	# result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{prix}` to topic prix")
        else:
            print(f"Failed to send message to topic prix")
        threading.Timer(60*60, self.publish_prix).start()

    def publish_reduction(self, reduction=5):
        time.sleep(1)
        result = self.client.publish("reduction",qos=2,payload=str({"id": self.id, "reduction":reduction}))
	# result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{reduction}` to topic reduction")
        else:
            print(f"Failed to send message to topic reduction")
        threading.Timer(60, self.publish_reduction).start()

    def main(self):
        self.client.connect("localhost",1883)
        self.publish_prix()
        self.publish_reduction()
        self.client.loop_forever()

if __name__=="__main__":
    mdmsclient = MDMSClient()
    mdmsclient.main()
