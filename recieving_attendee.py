
import json
import paho.mqtt.client as mqtt


host="esj44w.messaging.internetofthings.ibmcloud.com"  #connecting to cloud
clntid="d:esj44w:S_ViSION:cnt-1"
username="use-token-auth"
password="++wbTOXaFos0rfti&h"
topic="iot-2/cmd/state/fmt/json"

def on_connect(client,userdata,flags,rc):             #function to get attendee sent
    print("status:"+str(rc))

def on_message(client,userdata,msg):
    atten=json.loads(msg.payload)["state"]
    print(atten)
    
client = mqtt.Client(clntid)                          #retrive from cloud application
client.username_pw_set(username,password)
client.connect(host, 1883, 60)
client.subscribe(topic)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()
