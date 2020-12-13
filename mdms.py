import paho.mqtt.client as mqtt

from client_mdms import MDMSClient

smclient = MDMSClient()
smclient.connect_and_loop()
