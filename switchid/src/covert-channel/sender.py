#!/usr/bin/env python
# Author: Robert Kroesche
# Email: rkroesche@sec.t-labs.tu-berlin.de
# This script is used for the cover channel
# on the sender side

import sys
import switchID
import randomString
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
	message = argv[0]
	messageLength = len(message)
	sendingWindow = float(argv[1])
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

	# end of message frame 
	endOfMessage = "0000000"

	# calulationg of tau_hold
	delay = sendingWindow / delayDivider
	
	sentDict = {messageLength: {offset: {delayDivider: {frameLength: {sendingWindow: {run: None}}}}}, "ovs_log": None}

	print "Initialization"
	print "setup sending bridge"
	print 
	# initialize the switch
	switchID.init_switch()

	# wait until the next full minute before start
	now = datetime.now().time()
	sleep = (60 - (float(now.second))) - (float(now.microsecond) / 10 ** 6)

	print "waiting " + str(sleep) + " seconds"
	time.sleep(sleep)

	binList = []
	# sending each frame of the message
	for i in range(0, messageLength, numberOfCharacters):
		

		# converting the messgae (i.e. the letter) to the binary ASCII representation
		binary = ''.join('{0:07b}'.format(ord(x), 'b') for x in message[i:i+numberOfCharacters])

		switchID.send_message(binary, sendingWindow)
		binList.append(binary)
		print
		# IDF, wait until the next full second
		now = datetime.now().time()
		sleep = 1 - float(now.microsecond) / 10 ** 6
		time.sleep(sleep)

	print "Sending end of message"
	switchID.send_message(endOfMessage, sendingWindow)
	print
	print "sent message: " + message
	print 
	sentDict[messageLength][offset][delayDivider][frameLength][sendingWindow][run] = (binList, message)

	# for better file naming
	run = "0" + run if int(run) < 10 else run

	ovsLog = []
	# open and read the OvS log 
	with open(pathOVSLog, "r") as fp:
		for line in fp:
			ovsLog.append(line)

	# add the OvS log to the dict
	sentDict["ovs_log"] = ovsLog

	# store the sentDict in a json compatible file 
	if load == "True":
		fileName = "sent-" + str(messageLength) + "-" + str(offset) + "-" + str(round(delayDivider, 2)) \
		+ "-" + frameLength + "-" + str(sendingWindow) + "-withLoad-" + run + ".json"
		with open(pathWithLoad + fileName, "w") as fp:
			json.dump(sentDict,fp)

	else:
		fileName = "sent-" + str(messageLength) + "-" + str(offset) + "-" + str(round(delayDivider, 2)) \
		+ "-" + frameLength + "-" + str(sendingWindow) + "-noLoad-" + run + ".json"
		with open(pathNoLoad + fileName, "w") as fp:
			json.dump(sentDict,fp)

	

	print "Transmisson finined!"
	print "Tear down switch"
	# delete the switch (i.e. the OvS bridge)
	switchID.del_switch()

if __name__ == "__main__":
	main(sys.argv[1:])
