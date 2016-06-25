import paho.mqtt.client as mqtt
import pygame.mixer

SOUNDFILES = ['doorbell-1.mp3', 'doorbell-2.wav']
SOUNDS = dict()

for soundfile in SOUNDFILES:
	SOUNDS[soundfile] = pygame.mixer.Sound(soundfile)

def playsound(soundname):
	try:
		sound = SOUNDS[soundname]
	except KeyError:
		return 0
	print 'Playing [{0}]'.format(soundname)
	sound.play()
	return 1

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('alexa/play')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if not playsound(msg.payload):
    	print "Error: \"" + msg.payload + "\" is not a valid file path."

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('pidev.local', 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()
try:
    rc = 0
    while rc == 0:
        rc = client.loop()
except KeyboardInterrupt:
    print('bye')
