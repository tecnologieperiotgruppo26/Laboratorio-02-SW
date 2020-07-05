import paho.mqtt.client as PahoMQTT
import time
import threading
import json
import random

class MyMQTT:
    # praicamente da quel che ho capito sta classe è un qualcosa di più specifico rispetto ad un publisher
    # creato un po meglio
    def __init__(self, clientID, broker, port, notifier, clean_session=False):
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
        self._paho_mqtt.on_message = self.myOnMessageReceived

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connected to %s with result code: %d" % (self.broker, rc))

    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
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

    def myPublish(self, topic, message):
        # publichiamo un messagio relativo ad un certo topic. l'int inviato come parametro
        # indica il grado di QOS relativo a quella comunicazione
        self._paho_mqtt.publish(topic, message, 2)

    def myUnsubscribe(self):
        if self._isSubscriber:
            # remember to unsuscribe if it is working also as subscriber
            self._paho_mqtt.unsubscribe(self._topic)

    def notify(self, topic, msg):
        #SE I MESSAGGI TI ARRIVANO QUI L'IMPORTANTE è METTERE LA RISORSA DA AGGIORNARE CHE
        #POI RICHIAMI DA FUORI CON UNA GET
        print("received '%s' under topic '%s'" % (msg, topic))
#        if topic == self.myTopic + "/res":
#            self.deviceID = msg


class myThread(threading.Thread):
    def __init__(self, name, topic, value, timeToStop):
        threading.Thread.__init__(self, name = name)
        self.myTopic = topic
        self.myValue = value
        self.myClient = MyMQTT(self.name, "mqtt.eclipse.org", 1883, self)
        self.timeToStop = timeToStop
        self.deviceID = "unregistered"

    def run(self):
        self.myClient.start()
        self.myClient.mySubscribe(self.myTopic+"/+")
        while True:
            self.myValue += 1
            valore = ValoreJson("temperature", self.myValue, "c", self.deviceID)
            self.myClient.myPublish(self.myTopic, valore.toString())
            print("sto inviando {}".format(valore.toString()))
            time.sleep(10)
            if timeToStop:
                break

    def terminate(self):
        self._running = False
        self.myClient.myUnsubscribe()



if __name__ == '__main__':
    counterThread = 0
    threads = []
    timeToStop = False
    topic = "/tiot/26/catalog/"
    topicMessage = ""
    menu = "s = inserire il subtopic del device\n" \
           "v = inserire il valore letto dal device\n" \
           "a = automatizza il publisher tramite thread. occhio ad aver inizilizzato almeno il topic\n" \
           "q = esci da tutto\n"
    while (True):
        command = input(menu)
        if command == 's':
            subTopic = input("Inserire il subtopic del device:\n")
            topicMessage = topic + subTopic
            value = int(input("inserire il valore letto dal device\n"))
            #client.mySecondPublish(topicMessage, value)
        elif command == 'v':
            if (topicMessage == ""):
                print("Hei ti sei dimenticato di inserire il topic. FALLO!")
                pass
            else :
                value = int(input("inserire il valore letto dal device\n"))

        elif command == 'a':
            if (topicMessage == ""):
                print("Hei ti sei dimenticato di inserire il topic. FALLO!")
                pass
            else:
                #crea il thread
                thread = myThread("thread-" + "{}".format(counterThread), topicMessage, 0, timeToStop)
                threads.append(thread)
                thread.start()
        elif command == 'q':
            break

    for t in threads:
        t.timeToStop=True
        t.join()
        #threads[n].terminate()

#
#
#
#
#THREAD CON SEMAFORO
class semaphore_thread (threading.Thread):

    available_tables = ['A', 'B', 'C', 'D', 'E']      #ipotizziamo la presenza di 5 casse e 15 utenti.

    def __init__(self, thread_name, semaphore):
        threading.Thread.__init__(self, name=thread_name)
        self.sleep_time = random.randint(3, 7)
        self.thread_sempaphore = semaphore

    def run(self):
        #acquire a semaphore, print something e release a semaphore
        self.thread_sempaphore.acquire()
        table = semaphore_thread.available_tables.pop()
        """
        ora qui posso inserire il codice del comportamento del thread. 
        prima gli ho dato l'accesso alla risorsa tramite semaforo e subito dopo 
        aver fatto cose lo rilascio
        """
        print(f"Thread {self.getName()} ha avuto accesso alla cassa {table}, e si appresta a pagare per poi uscire")
        time.sleep(self.sleep_time)
        print(f"Thread {self.getName()} ha finito di pagare in {self.sleep_time} secondi ed esce! {table} è libera!")
        semaphore_thread.available_tables.append(table)
        self.thread_sempaphore.release()

