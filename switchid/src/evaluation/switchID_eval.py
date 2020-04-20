#!/usr/bin/env python
#Author: Robert Kroesche
#Email: rkroesche@sec.t-labs.tu-berlin.de
#This script is intented to test a SDN covert channel using
#switch identification technique


import paramiko
import os
import sys
from subprocess import call
import time
import string
import randomString
import multiprocessing as mp
from pprint import pprint
from datetime import datetime
import time

# ssh username and hostnames
username="root"
sender="md00"
receiver="md02"
controller="md01"
ofcprobe = "md03"
# set the frame lengths, i.e. (without the start bit) 1 means Fl=7, 2 means Fl=14, 4 menas Fl=28
numberOfCharacters = [1, 2, 4]
# set the message lengths
messageLengths = [64, 512, 1024]
# set the time intervals
timeIntervals = [0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03]
# set the timeout value tau_hold
delayDividers = [2.0/3.0]
# set the timeout for the offet (i.e. tau_offset)
offset = 0.005 # fixed to 5ms
# wait for controller to start up
waitForController = 60
# wait for OFCProbe to start and ramp up
waitForOfcProbe = 60
# set the number o runs per experiment
numberOfRuns = 1
# set the start number for the file naming
startNumberOfRuns = 1

# set to True if the eval should run with load on the controller
withLoad = [False]
# set to True if the eval should sample the CPU load on the controller
withSampling = False

def start_sampling(messageLength, timeInterval, framelength, withLoad):

	# connects to the controller and starts sampling
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(controller, username=username)

	pid = "$(ps -ef | grep karaf.jar | grep -v grep | cut -c10-15 | tr -d ' ')"
	if withLoad:
		command = "top -p " + pid + " -b -d 1 >> onosCpuMem/onosCpuMem-" + pid + "-" + str(messageLength) \
		+ "-" + str(timeInterval) + "-" + str(framelength) + "-withLoad &"

		print "Starting sampling the CPU utilization with: " +  command
	else:
		command = "top -p " + pid + " -b -d 1 >> onosCpuMem/onosCpuMem-" + pid + "-" + str(messageLength) \
		+ "-" + str(timeInterval) + "-" + str(framelength) + "-noLoad &"

		print "Starting sampling the CPU utilization with: " +  command

	try:
		stdin, stdout, stderr = ssh.exec_command(command)
		#pprint(stdout.readlines())
		ssh.close()

	except paramiko.SSHException:
		print "Caught paramiko ssh exception in start_sampling(). Exit!"
		print stdout.readlines()
		print stderr.readlines()
		ssh.close()
		exit()

def start_controller(withSampling=False):

	# connects to the controller, deletes the data directory and starts ONOS
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(controller, username=username)

	command = "rm -rf onos-1.10.2/apache-karaf-3.0.8/data/*"

	print "Deleting ONOS data: " + command

	try:
		stdin, stdout, stderr = ssh.exec_command(command)
		pprint(stdout.readlines())

	except paramiko.SSHException:
		print "Caught paramiko ssh exception in start_controller(). Exit!"
		print stdout.readlines()
		print stderr.readlines()
		ssh.close()
		exit()

	if withSampling:
		command = "taskset -c 0 ./onos-1.10.2/bin/onos-service server 2>/tmp/onoslog.err &"
	else:
		command = "./onos-1.10.2/bin/onos-service server 2>/tmp/onoslog.err &"
	print "Now starting ONOS with: " + command

	try:
		stdin, stdout, stderr = ssh.exec_command(command)
		print "sleeping " + str(waitForController) + " seconds"
		time.sleep(waitForController)
		ssh.close()

	except paramiko.SSHException:
		print "Caught paramiko ssh exception in start_controller(). Exit!"
		print stdout.readlines()
		print stderr.readlines()
		ssh.close()
		exit()

def start_ofcprobe():

	print "Starting ofcProbe..."
	# connects to host ofcprobe and starts ofcprobe
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ofcprobe, username=username)

	command = "java -jar ofcProbe/ofcprobe-1.0.4-SNAPSHOT.one-jar.jar ofcProbe/teleportLoad.ini >> /tmp/ofcLog.out&"
	print "Starting ofcprobe with: " + command

	try:
		stdin, stdout, stderr = ssh.exec_command(command)
		print "Waiting " + str(waitForOfcProbe) + " seconds for ofcProbe to ramp up"
		time.sleep(waitForOfcProbe)
		ssh.close()

	except paramiko.SSHException:
		print "Caught paramiko ssh exception in start_ofcprobe(). Exit!"
		print stdout.readlines()
		print stderr.readlines()
		ssh.close()
		exit()

def shutdown_onos():

	#connects to the controller and shutdown ONOS
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(controller, port=8101, username=username)

	command = "shutdown -f"
	print "Shutting down ONOS with: " + command

	try:
		stdin, stdout, stderr = ssh.exec_command(command)
		pprint(stdout.readlines())
		ssh.close()

	except paramiko.SSHException:
		print "Caught paramiko ssh exception in shoutdown_onos(). Exit!"
		print stdout.readlines()
		print stderr.readlines()
		ssh.close()
		exit()

def wipe_out():

	#connects to the controller and wipe-out ONOS
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(controller, port=8101, username=username)

	command = "wipe-out please"
	print "Wipe out with: " + command

	try:
		stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
		pprint(stdout.readlines())
		ssh.close()

	except paramiko.SSHException:
		print "Caught paramiko ssh exception in shoutdown_onos(). Exit!"
		print stdout.readlines()
		print stderr.readlines()
		ssh.close()
		exit()

def kill_ofcprobe():

	# connects to host ofcprobe and kills ofcprobe
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ofcprobe, username=username)

	command = "killall java"
	print "Killing ofcprobe with: " + command

	try:
		stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
		pprint(stdout.readlines())
		ssh.close()

	except paramiko.SSHException:
		print "Caught paramiko ssh exception in kill_ofcprobe(). Exit!"
		print stdout.readlines()
		print stderr.readlines()
		ssh.close()
		exit()

def kill_onos():

	# connects to md03 and kills ofcprobe
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(controller, username=username)

	command = "killall java"
	print "Killing ONOS with: " + command

	try:
		stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
		pprint(stdout.readlines())
		ssh.close()

	except paramiko.SSHException:
		print "Caught paramiko ssh exception in kill_onos(). Exit!"
		print stdout.readlines()
		print stderr.readlines()
		ssh.close()
		exit()

def kill_top():

	#connects to the controller and kills top (used for sampling CPU utilization)
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(controller, username=username)
	command = "killall top"
	print "Killing top with: " + command

	try:
		stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
		pprint(stdout.readlines())
		ssh.close()

	except paramiko.SSHException:
		print "Caught paramiko ssh exception in kill_top(). Exit!"
		print stdout.readlines()
		print stderr.readlines()
		ssh.close()
		exit()

def kill_all(load):

	print "Killing ofcprobe and top on md03 and md01"
	if load:
		kill_ofcprobe()
	kill_top()
	kill_onos()


def send_message(message, timeInterval, numberOfCharacters, delayDivider, offset, run, load):

	# connects to sending switch (i.e. sender) and excecutes the sender script with the given values
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(sender, username=username)
	command = "python sender.py " + str(message) + " " + str(timeInterval) + " " + str(numberOfCharacters) \
			+ " " + str(delayDivider) + " " + str(offset) + " " + str(run) + " " + str(load)
	try:
		stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
		pprint(stdout.readlines())
		ssh.close()

	except paramiko.SSHException:
		print "Caught paramiko ssh exception in init_switch(). Exit!"
		print stdout.readlines()
		print stderr.readlines()
		ssh.close()
		exit()

def receive_message(messageLength, timeInterval, numberOfCharacters, delayDivider, offset, run, load):

	# connects to receiving switch (i.e. receiver) and executes the receivert script with the given values
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(receiver, username=username)
	command = "python receiver.py " + str(messageLength) +" " + str(timeInterval) + " " + str(numberOfCharacters) \
			+ " " + str(delayDivider) + " " + str(offset) + " " + str(run) + " " + str(load)
	try:
		stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
		pprint(stdout.readlines())
		ssh.close()

	except paramiko.SSHException:
		print "Caught paramiko ssh exception in init_switch(). Exit!"
		print stdout.readlines()
		print stderr.readlines()
		ssh.close()
		exit()

def first_connect():

	# connects to sending switch (i.e. sender) and executes a first connection to the controller
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(sender, username=username)
	command = "./first_connection.sh"
	try:
		stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
		pprint(stdout.readlines())
		ssh.close()

	except paramiko.SSHException:
		print "Caught paramiko ssh exception in init_switch(). Exit!"
		print stdout.readlines()
		print stderr.readlines()
		ssh.close()
		exit()

	# connects to receiving switch (i.e. receiver) and executes a first connection to the controller
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(receiver, username=username)
	command = "./first_connection.sh"
	try:
		stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
		pprint(stdout.readlines())
		ssh.close()

	except paramiko.SSHException:
		print "Caught paramiko ssh exception in init_switch(). Exit!"
		print stdout.readlines()
		print stderr.readlines()
		ssh.close()
		exit()


def main(argv):

	kill_all(True)

	for load in withLoad:
		for messageLength in messageLengths:
			message = randomString.random_string(messageLength)
			for delayDivider in delayDividers:
				for j in numberOfCharacters:
					for timeInterval in timeIntervals:
						for run in range(startNumberOfRuns,numberOfRuns + startNumberOfRuns):
							t1 = time.time()
							print "The current experiment starts at: " + datetime.now().strftime('%H:%M:%S:%f')
							print "with the following values:"
							print "message length:\t" + str(messageLength)
							print "delayDivider:\t" + str(delayDivider)
							print "frame length:\t" + str(j*7)
							print "time interval:\t" + str(timeInterval)
							print "run:\t\t" + str(run)

							if withSampling:
								start_controller(withSampling)
								start_sampling(messageLength, timeInterval, j*7, load)
							else:
								start_controller()

							# if load is True, start ofcprobe
							if load:
								start_ofcprobe()

							now = datetime.now().time()
							sleep = 5 - float(now.microsecond) / 10 ** 6

							print "waiting " + str(sleep) + " seconds"
							time.sleep(sleep)

							# let sender and receiver connect a first time to controller
							first_connect()

							sender = mp.Process(target=send_message, args=(message, timeInterval, j, delayDivider, offset,  run, load))
							receiver = mp.Process(target=receive_message, args=(messageLength, timeInterval, j, delayDivider, offset, run, load))

							sender.start()
							receiver.start()

							sender.join()
							receiver.join()

							print "The run took: " + str(time.time() - t1)
							if withSampling:
								kill_top()

							if load:
								kill_ofcprobe()
							shutdown_onos()


if __name__ == "__main__":
	main(sys.argv[1:])
