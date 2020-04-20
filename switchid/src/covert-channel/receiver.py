#!/usr/bin/env python
# Author: Robert Kroesche
# Email: rkroesche@sec.t-labs.tu-berlin.de
# This script is used for the cover channel
# on the reveiver side

import sys
import time
import switchID
import time
import json
from datetime import datetime



def main(argv):
	# change the paths where the json files should be stored
	pathWithLoad = "jsons/with_load/"
	pathNoLoad = "jsons/no_load/" 
	# OvS default path for the log file
	pathOVSLog = "/usr/local/var/log/openvswitch/ovs-vswitchd.log"
	# command line arguments
	messageLength = str(argv[0])
	receivingWindow = float(argv[1])
	numberOfCharacters = int(argv[2])
	delayDivider = float(argv[3])
	offset = float(argv[4])
	run = str(argv[5])
	load = str(argv[6])
	# calulation of the frame length depending on the number 
	# of characters per frame
	frameLength = numberOfCharacters * 7

	# for better file naming
	if frameLength < 10:
		frameLength = "0" + str(frameLength)
	else: 
		frameLength = str(frameLength)
	
	receivedDict = {messageLength: {offset: {delayDivider: {frameLength: {receivingWindow: {run: None}}}}}, "ovs_log": None}

	# calulationg of tau_hold
	if delayDivider >= 1.0:
		delay = receivingWindow / delayDivider
	else: 
		delay = receivingWindow * delayDivider
	# initialize the start bit counter
	startBitCounter = 0
	receivedMessage = ""
	binList = []

	print "Initialization"
	
	print "setup receiving bridge"
	print 
	# initialize the switch
	switchID.init_switch()

	# wait until the next full minute before start
	now = datetime.now().time()
	sleep = offset + ((60 - float(now.second)) - (float(now.microsecond) / 10 ** 6))
	print "waiting " + str(sleep) + " seconds"
	time.sleep(sleep)
	# infinite loop receives frames until one of the break conditions is met 
	while (True):

		binary = ""
		# receive the binary of a frame and the current start bit counter
		binary, count = switchID.receive_message(receivingWindow, int(frameLength), offset, delay, startBitCounter)
		# reset the start bit conter
		if count == startBitCounter:
			startBitCounter = 0
		else: 
			startBitCounter = count
		# break conditions for the while loop, end of message or only ones received 
		if binary[0:7] == "0000000":
			print "End of message frame received or too many start bits missed"
			break
		elif binary[0:7] == "1111111":
			print "Something went wrong. Received only ones"
			break 

		binList.append(binary)
		# convert the binary to ACSII characters 
		tempMessage = ''.join(chr(int(binary[i*7:i*7+7],2)) for i in range(len(binary)//7))
		receivedMessage +=tempMessage
		# IDF, wait until the next full second
		now = datetime.now().time()
		sleep = offset + (1 - float(now.microsecond) / 10 ** 6)
		time.sleep(sleep)

	print "received Message: " + receivedMessage
	print
	receivedDict[messageLength][offset][delayDivider][frameLength][receivingWindow][run] = (binList, receivedMessage)
	
	# for better file naming
	run = "0" + run if int(run) < 10 else run
	frameLength = "0" + frameLength if frameLength < 10 else frameLength
	
	ovsLog = []
	# open and read the OvS log 
	with open(pathOVSLog, "r") as fp:
		for line in fp:
			ovsLog.append(line)

	# add the OvS log to the dict
	receivedDict["ovs_log"] = ovsLog	
	
	# store the receivedDict in a json compatible file 
	if load == "True":
		fileName = "received-" + str(messageLength) + "-" + str(offset) + "-" + str(round(delayDivider, 2)) \
		+ "-" + str(frameLength) + "-" + str(receivingWindow) + "-withLoad-" + run + ".json"
		
		with open(pathWithLoad + fileName, "w") as fp:
			json.dump(receivedDict,fp)
	else:
		fileName = "received-" + str(messageLength) + "-" + str(offset) + "-" + str(round(delayDivider, 2)) \
		+ "-" + str(frameLength) + "-" + str(receivingWindow) + "-noLoad-" + run + ".json"
		
		with open(pathNoLoad + fileName, "w") as fp:
			json.dump(receivedDict,fp)

	print "Transmisson finined!"
	print "Tear down switch"
	# delete the switch (i.e. the OvS bridge)
	switchID.del_switch()

if __name__ == "__main__":
	main(sys.argv[1:])
