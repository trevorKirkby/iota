#!/usr/bin/env python

import pigpio
import time

PIN = 21

def handler(pin, level, tick):
	print pin, level, tick

io = pigpio.pi()

io.set_mode(PIN, pigpio.INPUT)

io.set_pull_up_down(PIN, pigpio.PUD_UP)

io.set_glitch_filter(PIN,10000)

cb = io.callback(PIN, pigpio.FALLING_EDGE, handler)

while 1:
	time.sleep(1)
	#print cb.tally()
