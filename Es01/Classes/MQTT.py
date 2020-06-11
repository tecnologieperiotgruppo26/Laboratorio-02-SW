import paho.mqtt.client as PahoMQTT
import requests
from Classes.resource import *
from Classes.resource import Resource
from Classes.device import *


class MyMQTT:
    # praicamente da quel che ho capito sta classe è un qualcosa di più specifico rispetto ad un publisher
    # creato un po meglio
    def __init__(self, clientID, broker, port, notifier):
        self.broker = broker
        self.port = port
        self.notifier = notifier
        self.clientID = clientID
        self._topic = ""
        self._isSubscriber = False

        # create an instance of paho.mqtt.client
        self._paho_mqtt = PahoMQTT.Client(clientID, False)
        # register the callback
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnmessageReceived

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connected to %s with result code: %d" % (self.broker, rc))

    def myOnmessageReceived(self, paho_mqtt, userdata, msg):
        # A new message is received
        self.notifier.notify(msg.topic, str(msg.payload.decode("utf-8")))

    def mySubscribe(self, topic):
        # if needed, you can do some computation or error-check before subscribing
        print("subscribing to %s" % (topic))
        # subscribe for a topic
        self._paho_mqtt.subscribe(topic, 2)
        # just to remember that it works also as a subscriber
        self._isSubscriber = True
        self._topic = topic

    def start(self):
        # manage connection to broker
        self._paho_mqtt.connect(self.broker, self.port)
        self._paho_mqtt.loop_start()

    def stop(self):
        if (self._isSubscriber):
            # remember to unsuscribe if it is working also as subscriber
            self._paho_mqtt.unsubscribe(self._topic)
        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()

    def mySubPublish(self, topic, message):
        # publichiamo un messagio relativo ad un certo topic. l'int inviato come parametro
        # indica il grado di QOS relativo a quella comunicazione
        self._paho_mqtt.publish(topic, message, 2)


class ClientMQTT():
    def __init__(self, clientID, deviceManager):
        # create an instance of MyMQTT class
        self.clientID = clientID
        self.myMqttClient = MyMQTT(self.clientID, "mqtt.eclipse.org", 1883, self)
        self.deviceManager = deviceManager

    def run(self):
        # if needed, perform some other actions befor starting the mqtt communication
        print("running %s" % (self.clientID))
        self.myMqttClient.start()

    def end(self):
        # if needed, perform some other actions befor ending the software
        print("ending %s" % (self.clientID))
        self.myMqttClient.stop()

    def notify(self, topic, msg):
        # manage here your received message. You can perform some error-check here
        end_point = str(topic).split('/')[-1]
        print(topic)
        print(end_point)
        obj = dict(json.loads(msg))
        deviceID = obj['bn']
        resources = obj['e']
        print(deviceID)
        print(resources)
        if deviceID == "unregistered":
            idNew = self.deviceManager.addDevice(time.time(), resources, rest=[''], mqtt=end_point)
            self.myPublish(topic + "/res", str(idNew))
        else:
            print("sono nell'else")
            try:
                self.deviceManager.updateDevice(int(msg["bn"]), time.time(), resources)
            except:
                print("Uno ci prova, ma qui proprio non ci si riesce!")

    def mySubscribe(self, topic: str):
        self.myMqttClient.mySubscribe(topic)
        print("Mi sono sottoscritto al topic : {}".format(topic))

    def myPublish(self, topic, msg):
        self.myMqttClient.mySubPublish(topic, msg)
        print(f"Published {msg} under topic {topic}")

