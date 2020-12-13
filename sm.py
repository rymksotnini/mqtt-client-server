import paho.mqtt.client as mqtt

from client_sm import SMClient

smclient = SMClient()
smclient.connect_and_loop()
