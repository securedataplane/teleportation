#!/usr/bin/env python
# Author: Robert Kroesche
# Email: rkroesche@sec.t-labs.tu-berlin.de
# This module is used for a switch identificaton bases
# covert channel 

import time
import re
from subprocess import call
from datetime import datetime

def is_connected(delay, offset, t1):

	# wait some time because otherwise it is to fast! 
	t2 = max(0, delay - (time.time() - t1) - offset)
	time.sleep(t2)

	with open('/proc/net/tcp', 'r') as f:
		first_line = f.readline()
		for line in f:
			if re.search("19E9 01", line):
				del_controller("s2")
				return True

	del_controller("s2")
	return False

def set_controller(br, target):
	call(["ovs-vsctl", "set-controller", br, target])

def del_controller(br):
	call(["ovs-vsctl", "del-controller", br])

def del_switch():

	call(["./del_ovs_br.sh"])

def init_switch():

	call(["./add_ovs_br.sh"])

def send_message(binary, sendingWindow):
	t1 = time.time()
	print "sender starts at: " + datetime.now().strftime('%H:%M:%S:%f')
	print

	#sending start bit
	set_controller("s1", "tcp:10.0.0.2:6633")
	t2 = max(0, sendingWindow - (time.time() - t1))
	time.sleep(t2)
	
	#sending data bits 
	for bit in binary:
		t1 = time.time()
		if bit == "0":
			print datetime.now().strftime('%H:%M:%S:%f') + ": sending 0"
			#tx = time.time() 
			del_controller("s1")
			#print "del-controller took: " + str(time.time() - tx )
 		else:
			print datetime.now().strftime('%H:%M:%S:%f') + ": sending 1"
			#tx = time.time()
			set_controller("s1", "tcp:10.0.0.2:6633")
			#print "set-controller took: " + str(time.time() - tx )
		
		t2 = max(0, sendingWindow - (time.time()-t1))
		time.sleep(t2)

	del_controller("s1")

def receive_message(receivingWindow,frameLength, offset, delay,\
	startbitCounter):

	print "receiver starts at: " + datetime.now().strftime('%H:%M:%S:%f')
	print

	tempMessage = ""
	# infinite loop receives bits until one of the break conditions is met 
	while(True):
		t1 = time.time()
		set_controller("s2", "tcp:10.0.1.2:6633")

		if not is_connected(delay, offset, t1):
			t2 = max(0, receivingWindow - (time.time()-t1))
			time.sleep(t2)

			for _ in range(0, frameLength):
				t1 = time.time()	
				set_controller("s2", "tcp:10.0.1.2:6633")
				if is_connected(delay, offset, t1):
					tempMessage += "0"
				else:
				 	tempMessage += "1"
				print datetime.now().strftime('%H:%M:%S:%f') +\
				": s2 received: " + tempMessage 
				t2 = max(0, receivingWindow - (time.time() - t1))
				time.sleep(t2)
				# break conditions for the while loop, end of message or only ones received 
				if tempMessage == "0000000" or tempMessage == "1111111":
					break
			# break condition after an entire frame is received 
			break
		# condition if the receiver could not get the start of frame bit
		else:

			startbitCounter += 1
			# If the receiver missed the start bit, 
			# it should wait the whole frame until the next starts
			t2 = max(0, receivingWindow - (time.time() - t1))
			time.sleep(t2)
			print "Missed start bit, waiting one frame"
			for _ in range(0, frameLength):
				t1 = time.time()
				if is_connected(delay, offset, t1):
					tempMessage += "0"
				else:
				 	tempMessage += "1"
				t2 = max(0, receivingWindow - (time.time() - t1))
				time.sleep(t2)

			# After 5 consecutive missed start of frame bits, terminate the receiver 
			if startbitCounter >= 5:
				print "Too manny start bits missed!"
				tempMessage = "0000000"
			# the empty string indicates that a frame is missed 
			# (i.e. missed the start of frame bit)
			else:
				tempMessage = ""
			
			break 


	print

	return tempMessage, startbitCounter
