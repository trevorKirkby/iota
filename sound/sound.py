import pygame.mixer

pygame.mixer.init()

SOUNDFILES = list()
SOUNDS = dict()

for soundfile in SOUNDFILES:
	SOUNDS[soundfile] = pygame.mixer.Sound(soundfile)

def playsound(soundname):
	try:
		sound = SOUNDS[soundname]
	except KeyError:
		return 0
	sound.play()
	return 1

while True:
	index = raw_input("Enter the index of the sound file to play: ")
	try:
		index = int(index)
		if len(SOUNDFILES) <= index or index < 0:
			print "There is no file located at that index."
		else:
			playsound(SOUNDFILES[index])
	except:
		print "Please specify something numeric."