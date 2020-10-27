import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

#Connection to the AWS IoT Core with Root CA certificate and unique device credentials (keys and certificate) previously retrieved

from gpiozero import LED
import time

ledYellow = LED(18)
ledBlue = LED(8)

def helloworld(self, params, packet):
    print ('received message from aws iot')
    print ('Topic: ' + packet.topic)
    print ("payload", (packet.payload))
    payload = packet.payload.replace('\n','')
    payload = payload.replace('\t', '')
    print ("payload: ", payload)
    ledobj = json.loads(payload)
    #attrs = vars(ledobj)
    print (ledobj)
    #print(', '.join("%s: %s" % item for item in attrs.items()))

    if ledobj["led"].lower() == 'yellow':
        if ledobj["state"].lower() == 'on':
            ledYellow.on()
        else:
            ledYellow.off()
    else:
        if ledobj["state"].lower() == 'on':
            ledBlue.on()
        else:
            ledBlue.off()

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("MyAWSIOTClientID1")
# For TLS mutual authentication
myMQTTClient.configureEndpoint("aa8m2nguu5nib-ats.iot.us-east-1.amazonaws.com", 8883) #Provide your AWS IoT Core endpoint (Example: "abcdef12345-ats.iot.us-east-1.amazonaws.com")
myMQTTClient.configureCredentials("/home/pi/awsiot/root-ca.pem", "/home/pi/awsiot/private.pem.key", "/home/pi/awsiot/certificate.pem.crt") #Set path for Root CA and unique device credentials (use the private key and certificate retrieved from the logs in Step 1)
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)
 
print ("Initiating IOT core topic ...")
myMQTTClient.connect()

#Publish gps coordinates to AWS IoT Core

#myMQTTClient.publish("gpsTopic", "{\"gpsDeviceID\":\"1\",\"gpsLat\":10.1,\"gpsLng\":10.1,\"gpsDatTm\":\"03/02/2020  08:03:20.200\"}", 0)
myMQTTClient.subscribe("home/helloworld", 1, helloworld)

while True:
    time.sleep(5)
