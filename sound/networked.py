import sys
import os.path
import paho.mqtt.client as mqtt
import pygame.mixer

pygame.mixer.init()

SOUNDFILES = ['doorbell.wav',]
SOUNDS = dict()

# Sound files must be in OGG or uncompressed WAV format.
# Loading an MP3 works fine but play() is silent?!
for soundfile in SOUNDFILES:
	name, extension = os.path.splitext(soundfile)
	if extension not in ('.wav',):
		print 'Invalid soundfile extension for "{0}".'.format(soundfile)
		sys.exit(-1)
	print 'Loading [{0}]'.format(name)
	try:
		SOUNDS[name] = pygame.mixer.Sound(file=soundfile)
	except pygame.error, e:
		print 'Load error: {0}.'.format(e)
		sys.exit(-1)

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
    	print 'Invalid sound name: {0}'.format(msg.payload)

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
