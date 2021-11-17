import sys
import time
import json
import paho.mqtt.client as mqtt
import time



host="esj44w.messaging.internetofthings.ibmcloud.com"  #connecting to cloud
clntid="d:esj44w:Dashcom:com-1"
usrname="use-token-auth"
password="53+CUj!v0nWpIX4oai"
topic="iot-2/evt/sndg1/fmt/json"

client = mqtt.Client(clntid)
client.username_pw_set(usrname,password)
client.connect(host, 1883, 60)

def publs():
                try:
                        payload={"r":"ATTENDEE SENT"}               #function to send message to cloud after attendee sent
                        client.publish(topic, json.dumps(payload))
                        print("SENT")
                        time.sleep(2)

                except IOError:
                        print("Error")

                         

publs()
