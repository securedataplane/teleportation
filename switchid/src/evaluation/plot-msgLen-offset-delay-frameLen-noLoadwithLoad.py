#!/usr/bin/env python
#Author: Robert Kroesche, Kashyap Thimmaraju
#Email: rkroesche@sec.t-labs.tu-berlin.de, kash@fgsect.de

import re
import json
import glob
import itertools
from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt
from pprint import pprint
import Levenshtein

noLoadPath = "../../data/no_load/"
withLoadPath = "../../data/with_load/"
# path = "./jsons/tests/"
# path = "/tmp/delay-0.67/"

msgLenToPlot = [u'64']
# delayToPlot = [u'0.666666666667']
# delayToPlot = [u'2.0']
delayToPlot = [u'3.0']
frameLenToPlot = [u'07', u'14', u'28']
#frameLenToPlot = [u'07']

resultFileSuffix = "-10runsCleanOVSDB"

# path = "/tmp/"
resultsFile = "./diss-64_delay_3_Fl_071428-10runs-noLoadWithLoad.pdf"
# resultsFile = "./plot-msgLen"+ str(msgLenToPlot) +\
#               "-offset-delay" + str(delayToPlot) +\
#               "-frameLen" + str(frameLenToPlot) +\
#               "-intervals-noLoad" + resultFileSuffix + ".pdf"

def get_data(path, ovsLog=False):
    # collect sent information from json files
    x = []
    messageLengths = []
    offsets = []
    delays = []
    frameLengths = []
    timeIntervals = []
    numberOfRuns = []
    d = glob.glob(path + "sent*.json")
    d.sort()

    for i in d:
        x.append(json.load(open(i), object_pairs_hook=OrderedDict))
        # x.append(json.load(open(i)))
    # pprint(x)
    print "First extract all the keys from each json, and populate the key lists for data extraction."
    for file in x:
        for messageLength in file:
            if ovsLog is False and messageLength != u'ovs_log':
                # print messageLength
                if messageLength not in messageLengths:
                    print "Got messageLength: " + str(messageLength)
                    messageLengths.append(messageLength)
                for offset in file[messageLength]:
                    if offset not in offsets:
                        print "Got offset: " + str(offset)
                        offsets.append(offset)
                    for delay in file[messageLength][offset]:
                        if delay not in delays:
                            print "Got delay: " + str(delay)
                            delays.append(delay)
                        for frameLength in file[messageLength][offset][delay]:
                            if frameLength not in frameLengths:
                                print "Got frameLength: " + str(frameLength)
                                frameLengths.append(frameLength)
                            for interval in file[messageLength][offset][delay][frameLength]:
                                if interval not in timeIntervals:
                                    print "Got interval: " + str(interval)
                                    timeIntervals.append(interval)
                                for run in file[messageLength][offset][delay][frameLength][interval]:
                                    if run not in numberOfRuns:
                                        print "Got run: " + str(run)
                                        numberOfRuns.append(run)
    print "Now print the keys: messagesLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns"
    print messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns
    # print "x: "
    # pprint(x)
    # exit()

    sMessageDict = OrderedDict.fromkeys(messageLengths,
                                OrderedDict.fromkeys(offsets,
                                OrderedDict.fromkeys(delays,
                                OrderedDict.fromkeys(frameLengths,
                                OrderedDict.fromkeys(timeIntervals,
                                [])))))
    sFrameDict = OrderedDict.fromkeys(messageLengths,
                                OrderedDict.fromkeys(offsets,
                                OrderedDict.fromkeys(delays,
                                OrderedDict.fromkeys(frameLengths,
                                OrderedDict.fromkeys(timeIntervals,
                                [])))))
    sentValuesDict = {"messageDict": sMessageDict, "frameDict": sFrameDict}
    keyList = []
    print "First get the sent values from each json file into a keyList"
    for file in x:
        for messageLength in file:
            if messageLength == u'ovs_log':
                break
            print "messageLength: " + str(messageLength)
            if messageLength != u'ovs_log':
                for offset in file[messageLength]:
                    print "offset: " + str(offset)
                    for delay in file[messageLength][offset]:
                        print "delay: " + str(delay)
                        for frameLength in file[messageLength][offset][delay]:
                            print "frameLength: "+ str(frameLength)
                            for interval in file[messageLength][offset][delay][frameLength]:
                                print "interval: "
                                print interval
                                for run in file[messageLength][offset][delay][frameLength][interval]:
                                    print "here:"
                                    print messageLength, offset, delay, frameLength, interval
                                    print "run: "
                                    print run
                                    print file[messageLength][offset][delay][frameLength][interval][run][1]
                                    sentMessage = file[messageLength][offset][delay][frameLength][interval][run][1]
                                    keys = [messageLength, offset, delay, frameLength, interval, run, sentMessage]
        print "keys: " + str(keys)
        keyList.append(keys)
    print "keyList: "
    print keyList
    # exit()
    print "Now populate the sMessageDict with values from the keysList (from the json)"
    for messageLength in sMessageDict:
        print "messageLength: " + str(messageLength)
        offsetDict = OrderedDict.fromkeys(offsets)
        for offset in sMessageDict[messageLength]:
            print "offset: " + str(offset)
            delayDict = OrderedDict.fromkeys(delays)
            for delay in sMessageDict[messageLength][offset]:
                print "delay: " + str(delay)
                frameLengthDict = OrderedDict.fromkeys(frameLengths)
                for frameLength in sMessageDict[messageLength][offset][delay]:
                    print "frameLength: " + str(frameLength)
                    intervalDict = OrderedDict.fromkeys(timeIntervals, [])
                    for interval in sMessageDict[messageLength][offset][delay][frameLength]:
                        print "interval: " + str(interval)
                        # print sMessageDict[messageLength][offset][delay][frameLength][interval]
                        sentMessageList = []
                        for key in keyList:
                            if key[0] == messageLength and key[1] == offset and key[2] == delay and key[3] == frameLength and key[4] == interval and key[5] in numberOfRuns:
                                print "key: " + str(key)
                                if key[6] == "":
                                    sentMessageList.append(u'')
                                else:
                                    sentMessageList.append(key[6])
                        print "sentMessageList: "
                        print sentMessageList
                        print "total sentMessages: " + str(len(sentMessageList))
                        intervalDict[interval] = sentMessageList
                        print "intervaldict: "
                        print intervalDict
                    frameLengthDict[frameLength] = intervalDict
                    print "frameLengthDict: "
                    print frameLengthDict
                delayDict[delay] = frameLengthDict
                print "delaydict: "
                print delayDict
            offsetDict[offset] = delayDict
            print "offsetDict"
            print offsetDict
        sMessageDict[messageLength] = offsetDict
        print "sMessageDict"
        print sMessageDict
    # exit()

    # collect received information from json files
    print "Now get data for received files"
    x = []
    d = glob.glob(path + "received*.json")
    d.sort()
    for i in d:
        x.append(json.load(open(i), object_pairs_hook=OrderedDict))
    # pprint(x)
    rMessageDict = OrderedDict.fromkeys(messageLengths,
                                OrderedDict.fromkeys(offsets,
                                OrderedDict.fromkeys(delays,
                                OrderedDict.fromkeys(frameLengths,
                                OrderedDict.fromkeys(timeIntervals,
                                [])))))
    rFrameDict = OrderedDict.fromkeys(messageLengths,
                                OrderedDict.fromkeys(offsets,
                                OrderedDict.fromkeys(delays,
                                OrderedDict.fromkeys(frameLengths,
                                OrderedDict.fromkeys(timeIntervals,
                                [])))))
    receivedValuesDict = {"messageDict": rMessageDict, "frameDict": rFrameDict}
    keyList = []
    print "First get the received values from each json file into a keyList"
    for file in x:
        for messageLength in file:
            if messageLength == u'ovs_log':
                break
            print "messageLength: " + str(messageLength)
            if messageLength != u'ovs_log':
                for offset in file[messageLength]:
                    print "offset: " + str(offset)
                    for delay in file[messageLength][offset]:
                        print "delay: " + str(delay)
                        for frameLength in file[messageLength][offset][delay]:
                            print "frameLength: " + str(frameLength)
                            for interval in file[messageLength][offset][delay][frameLength]:
                                print "interval: "
                                print interval
                                for run in file[messageLength][offset][delay][frameLength][interval]:
                                    print "here:"
                                    print messageLength, offset, delay, frameLength, interval
                                    print "run: "
                                    print run
                                    print file[messageLength][offset][delay][frameLength][interval][run][1]
                                    receivedMessage = file[messageLength][offset][delay][frameLength][interval][run][1]
                                    keys = [messageLength, offset, delay, frameLength, interval, run, receivedMessage]
        print "keys: " + str(keys)
        keyList.append(keys)
    print "keyList: "
    print keyList
    print "Now populate the rMessageDict with values from the keysList (from the json)"
    for messageLength in rMessageDict:
        print "messageLength: " + str(messageLength)
        offsetDict = OrderedDict.fromkeys(offsets)
        for offset in rMessageDict[messageLength]:
            print "offset: " + str(offset)
            delayDict = OrderedDict.fromkeys(delays)
            for delay in rMessageDict[messageLength][offset]:
                print "delay: " + str(delay)
                frameLengthDict = OrderedDict.fromkeys(frameLengths)
                for frameLength in rMessageDict[messageLength][offset][delay]:
                    print "frameLength: " + str(frameLength)
                    intervalDict = OrderedDict.fromkeys(timeIntervals, [])
                    for interval in rMessageDict[messageLength][offset][delay][frameLength]:
                        print "interval: " + str(interval)
                        # print rMessageDict[messageLength][offset][delay][frameLength][interval]
                        receivedMessageList = []
                        for key in keyList:
                            if key[0] == messageLength and key[1] == offset and key[2] == delay and key[3] == frameLength and key[4] == interval and key[5] in numberOfRuns:
                                print "key: " + str(key)
                                if key[6] == "":
                                    receivedMessageList.append(u'')
                                else:
                                    receivedMessageList.append(key[6])
                        print "receivedMessageList: "
                        print receivedMessageList
                        print "total receivedMessages: " + str(len(receivedMessageList))
                        intervalDict[interval] = receivedMessageList
                        print "intervaldict: "
                        print intervalDict
                    frameLengthDict[frameLength] = intervalDict
                    print "frameLengthDict: "
                    print frameLengthDict
                delayDict[delay] = frameLengthDict
                print "delaydict: "
                print delayDict
            offsetDict[offset] = delayDict
            print "offsetDict"
            print offsetDict
        rMessageDict[messageLength] = offsetDict
        print "rMessageDict"
        print rMessageDict
    sentValuesDict["messageDict"] = sMessageDict
    receivedValuesDict["messageDict"] = rMessageDict
    # exit()
    return messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict

def filterData(messageLengths, offsets, delays,
               frameLengths, timeIntervals, numberOfRuns,
               sentValuesDict, receivedValuesDict):
    print "filterData()"
    print "filter data based on msgLenToPlot, delayToPlot, frameLenToPlot"
    print msgLenToPlot, delayToPlot, frameLenToPlot
    print "first remove from the dict"
    keys = ["messageDict", "frameDict"]
    for key in keys:
        for msgLen in messageLengths:
            if msgLen not in msgLenToPlot:
                del sentValuesDict[key][msgLen]
                del receivedValuesDict[key][msgLen]
            else:
                for offset in offsets:
                    for delay in delays:
                        if delay not in delayToPlot:
                            del sentValuesDict[key][msgLen][offset][delay]
                            del receivedValuesDict[key][msgLen][offset][delay]
                        else:
                            for frameLen in frameLengths:
                                if frameLen not in frameLenToPlot:
                                    del sentValuesDict[key][msgLen][offset][delay][frameLen]
                                    del receivedValuesDict[key][msgLen][offset][delay][frameLen]
    print "Now update the keys in the list: "
    messageLengths = msgLenToPlot
    delays = delayToPlot
    frameLengths = frameLenToPlot
    print "done filtering."
    # pprint(sentValuesDict)
    # pprint(receivedValuesDict)
    return messageLengths, offsets, delays,\
               frameLengths, timeIntervals, numberOfRuns,\
               sentValuesDict, receivedValuesDict

def getLevenshtein(messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentMessages, receivedMessages):
    print "getLevenshtein()"
    print delays
    print numberOfRuns
    #numberOfRuns = [u'1',u'2',u'3',u'4',u'5']
    print timeIntervals
    levenshteinDict = OrderedDict.fromkeys(messageLengths)
    for messageLength in messageLengths:
        offsetDict = OrderedDict.fromkeys(offsets)
        for offset in offsets:
            delayDict = OrderedDict.fromkeys(delays)
            for delay in delays:
                frameLengthDict = OrderedDict.fromkeys(frameLengths)
                for frameLength in frameLengths:
                    intervalDict = OrderedDict.fromkeys(timeIntervals, [])
                    for interval in timeIntervals:
                        lev = []
                        for i in range(len(numberOfRuns)):
                            lev.append(100*
                                Levenshtein.ratio(
                                    sentMessages[messageLength][offset][delay][frameLength][interval][i],
                                    receivedMessages[messageLength][offset][delay][frameLength][interval][i]
                                )
                            )
                        intervalDict[interval] = lev
                    frameLengthDict[frameLength] = intervalDict
                delayDict[delay] = frameLengthDict
            offsetDict[offset] = delayDict
        levenshteinDict[messageLength] = offsetDict
    print "levenshtein dict: "
    print levenshteinDict
    return levenshteinDict

def plot(noLoadData, withLoadData):
    print "plot()"
    # with was measured in inkscape
    width = 3.487 * 2
    height = 2.15512979
    plt.style.use('./dissertation.mplstyle')
    plt.figure(1, figsize=(width, height), frameon=False)
    fig = plt.figure(1, frameon=True)
    fig.subplots_adjust(bottom=0.2)
    # NO LOAD
    # if delayToPlot[0] == u'3.0':
    #     # width = width/2.0
    #     ax = plt.subplot(1, 2, 1)
    # else:
    #     ax = plt.subplot(1,2,1)
    ax = plt.subplot(1, 2, 1)
    ax.yaxis.grid()
    data = []
    y = noLoadData
    for messageLength in y:
        for offset in y[messageLength]:
            for delay in y[messageLength][offset]:
                for frameLength in y[messageLength][offset][delay]:
                    print "plot delay: "
                    print delay
                    for interval in y[messageLength][offset][delay][frameLength]:
                        data.append(y[messageLength][offset][delay][frameLength][interval])
    # medianpointprops = dict(marker='', linestyle='-', color='red')
    bp = plt.boxplot(data, patch_artist=True)
    colors = ['white', 'white', 'white']
    k = 0
    i = 0
    for patch in bp['boxes']:
        if k > 7 and k < 15:
            i = 1
        elif k > 15:
            i = 2
        patch.set_facecolor(colors[i])
        # plt.setp(bp['whiskers'], color='black')
        # plt.setp(bp['fliers'], color='blue')
        k += 1
    plt.ylabel('Accuracy (%)')
    c = 0
    ax.text(c+3.1, 110.0, u'FL=7')
    ax.text(c+11.1, 110.0, u'FL=14')
    ax.text(c+19.1,  110.0, u'FL=28')
    # ax.text(c+11.1, 125, u'No Load')
    offset = 8.5
    for i in range(1, 25):
        plt.plot([offset, offset], [-1, 100], color='#000000')
        offset += 8
    tickMarks = range(1, 25)
    x = range(30, 110, 10)
    y = x
    x.extend(y)
    x.extend(y)
    plt.xticks(tickMarks, tuple(x))
    # plt.tick_params(axis='both', which='major', labelsize=10)
    plt.xlabel("Time Interval (ms)\n(a) No Load")
    box = ax.get_position()
    ax.set_position([box.x0 * .5, box.y0, box.width * 1.22, box.height * 0.95])
    # ax.yaxis.grid(True, linestyle='-', which='major', color='grey')
    ax.set_axisbelow(True)
    # plt.title('No Load')
    # plt.tight_layout()
    plt.savefig(resultsFile)

    # WITH LOAD
    if delayToPlot[0] == u'3.0':
        return
    ax = plt.subplot(1,2,2)
    ax.yaxis.grid()
    data = []
    y = withLoadData
    for messageLength in y:
        for offset in y[messageLength]:
            for delay in y[messageLength][offset]:
                for frameLength in y[messageLength][offset][delay]:
                    print "plot delay: "
                    print delay
                    for interval in y[messageLength][offset][delay][frameLength]:
                        data.append(y[messageLength][offset][delay][frameLength][interval])
    # medianpointprops = dict(marker='', linestyle='-', color='red')
    bp = plt.boxplot(data, patch_artist=True)
    colors = ['white', 'white', 'white']
    k = 0
    i = 0
    for patch in bp['boxes']:
        if k > 7 and k < 15:
            i = 1
        elif k > 15:
            i = 2
        patch.set_facecolor(colors[i])
        # plt.setp(bp['whiskers'], color='black')
        # plt.setp(bp['fliers'], color='blue')
        k += 1
    plt.ylabel('Accuracy (%)')
    c = 0
    ax.text(c+3.1, 110.0, u'FL=7')
    ax.text(c+11.1, 110.0, u'FL=14')
    ax.text(c+19.1,  110.0, u'FL=28')
    # ax.text(c+11.1, 125, u'With Load')
    offset = 8.5
    for i in range(1, 25):
        plt.plot([offset, offset], [-1, 100], color='#000000')
        offset += 8
    tickMarks = range(1, 25)
    x = range(30, 110, 10)
    y = x
    x.extend(y)
    x.extend(y)
    plt.xticks(tickMarks, tuple(x))
    # plt.tick_params(axis='both', which='major', labelsize=10)
    plt.xlabel("Time Interval (ms)\n(b) With Load")
    box = ax.get_position()
    ax.set_position([box.x0 + 0.01, box.y0, box.width * 1.22, box.height * 0.95])
    # ax.yaxis.grid(True, linestyle='-', which='major', color='grey')
    ax.set_axisbelow(True)
    # plt.tight_layout()
    plt.savefig(resultsFile)

def main():
    messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict = get_data(noLoadPath)
    print "messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict"
    print messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict
    print "filter data..."
    messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict = filterData(messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict)
    noLoadlevenshteinDict = getLevenshtein(messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict["messageDict"], receivedValuesDict["messageDict"])

    if delayToPlot[0] == u'3.0':
        withLoadlevenshteinDict = {}
    else:
        messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict = get_data(withLoadPath)
        print "messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict"
        print messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict
        print "filter data..."
        messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict = filterData(messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict)
        withLoadlevenshteinDict = getLevenshtein(messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict["messageDict"], receivedValuesDict["messageDict"])
    plot(noLoadlevenshteinDict, withLoadlevenshteinDict)

main()
