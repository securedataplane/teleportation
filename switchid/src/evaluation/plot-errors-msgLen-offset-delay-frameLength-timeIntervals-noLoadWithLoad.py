#!/usr/bin/env python
#Author: Robert Kroesche, Kashyap Thimmaraju
#Email: rkroesche@sec.t-labs.tu-berlin.de, kash@fgsect.de

import re
import json
import glob
import itertools
from collections import OrderedDict
import matplotlib.pyplot as plt
from pprint import pprint
import Levenshtein

noLoadPath = "../../data/no_load/"
withLoadPath = "../../data/with_load/"
# path = "./jsons/tests/"

msgLenToPlot = [u'64']
# delayToPlot = [u'2.0']
delayToPlot = [u'3.0']
# delayToPlot = [u'0.666666666667']
frameLenToPlot = [u'07', u'14', u'28']
resultFileSuffix = "-10runsCleanOVSDB-fixed"

msbResultsFile = "./diss-plot-msbErrors-msgLen"+ "64_delay_3_Fl_071428-10runs-noLoadWithLoad.pdf"
eomResultsFile = "./diss-plot-eomErrors-msgLen"+ "64_delay_3_Fl_071428-10runs-noLoadWithLoad.pdf"
cfResultsFile = "./diss-plot-cfErrors-msgLen"+ "64_delay_2_Fl_071428-10runs-noLoadWithLoad.pdf"

# with was measured in inkscape
width = 3.487 * 2
height = 2.15512979
plt.style.use('./dissertation.mplstyle')

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
    # #pprint(x)
    print "First extract all the keys from each json, and populate the key lists for data extraction."
    for file in x:
        for messageLength in file:
            if ovsLog is False and messageLength != u'ovs_log':
                # #print messageLength
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
    print "Now #print the keys: messagesLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns"
    #print messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns
    # print "x: "
    # #pprint(x)
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
                                #print interval
                                for run in file[messageLength][offset][delay][frameLength][interval]:
                                    print "here:"
                                    #print messageLength, offset, delay, frameLength, interval
                                    print "run: "
                                    #print run
                                    #print file[messageLength][offset][delay][frameLength][interval][run][1]
                                    sentMessage = file[messageLength][offset][delay][frameLength][interval][run][1]
                                    sentFrame = file[messageLength][offset][delay][frameLength][interval][run][0]
                                    keys = [messageLength, offset, delay, frameLength, interval, run, sentMessage, sentFrame]
        print "keys: " + str(keys)
        keyList.append(keys)
    print "keyList: "
    #print keyList
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
                        # #print sMessageDict[messageLength][offset][delay][frameLength][interval]
                        sentMessageList = []
                        for key in keyList:
                            if key[0] == messageLength and key[1] == offset and key[2] == delay and key[3] == frameLength and key[4] == interval and key[5] in numberOfRuns:
                                print "key: " + str(key)
                                if key[6] == "":
                                    sentMessageList.append(u'')
                                else:
                                    sentMessageList.append(key[6])
                        print "sentMessageList: "
                        #print sentMessageList
                        intervalDict[interval] = sentMessageList
                        print "intervaldict: "
                        #print intervalDict
                    frameLengthDict[frameLength] = intervalDict
                    print "frameLengthDict: "
                    #print frameLengthDict
                delayDict[delay] = frameLengthDict
                print "delaydict: "
                #print delayDict
            offsetDict[offset] = delayDict
            print "offsetDict"
            #print offsetDict
        sMessageDict[messageLength] = offsetDict
        print "sMessageDict"
        #print sMessageDict
    print "Now populate the sFrameDict with values from the keysList (from the json)"
    for messageLength in sFrameDict:
        print "messageLength: " + str(messageLength)
        offsetDict = OrderedDict.fromkeys(offsets)
        for offset in sFrameDict[messageLength]:
            print "offset: " + str(offset)
            delayDict = OrderedDict.fromkeys(delays)
            for delay in sFrameDict[messageLength][offset]:
                print "delay: " + str(delay)
                frameLengthDict = OrderedDict.fromkeys(frameLengths)
                for frameLength in sFrameDict[messageLength][offset][delay]:
                    print "frameLength: " + str(frameLength)
                    intervalDict = OrderedDict.fromkeys(timeIntervals, [])
                    for interval in sFrameDict[messageLength][offset][delay][frameLength]:
                        print "interval: " + str(interval)
                        # #print sMessageDict[messageLength][offset][delay][frameLength][interval]
                        sentFrameList = []
                        for key in keyList:
                            if key[0] == messageLength and key[1] == offset and key[2] == delay and key[3] == frameLength and key[4] == interval and key[5] in numberOfRuns:
                                print "key: " + str(key)
                                sentFrameList.append(key[7])
                        print "sentFrameList: "
                        #print sentFrameList
                        intervalDict[interval] = sentFrameList
                        print "intervaldict: "
                        #print intervalDict
                    frameLengthDict[frameLength] = intervalDict
                    print "frameLengthDict: "
                    #print frameLengthDict
                delayDict[delay] = frameLengthDict
                print "delaydict: "
                #print delayDict
            offsetDict[offset] = delayDict
            print "offsetDict"
            #print offsetDict
        sFrameDict[messageLength] = offsetDict
        print "sFrameDict"
        #print sFrameDict
    # exit()

    # collect received information from json files
    print "Now get data for received files"
    x = []
    d = glob.glob(path + "received*.json")
    d.sort()
    for i in d:
        x.append(json.load(open(i), object_pairs_hook=OrderedDict))
    # #pprint(x)
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
                                #print interval
                                for run in file[messageLength][offset][delay][frameLength][interval]:
                                    print "here:"
                                    #print messageLength, offset, delay, frameLength, interval
                                    print "run: "
                                    #print run
                                    #print file[messageLength][offset][delay][frameLength][interval][run][1]
                                    receivedMessage = file[messageLength][offset][delay][frameLength][interval][run][1]
                                    receivedFrame = file[messageLength][offset][delay][frameLength][interval][run][0]
                                    keys = [messageLength, offset, delay, frameLength, interval, run, receivedMessage, receivedFrame]
        print "keys: " + str(keys)
        keyList.append(keys)
    print "keyList: "
    #print keyList
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
                        # #print rMessageDict[messageLength][offset][delay][frameLength][interval]
                        receivedMessageList = []
                        for key in keyList:
                            if key[0] == messageLength and key[1] == offset and key[2] == delay and key[3] == frameLength and key[4] == interval and key[5] in numberOfRuns:
                                print "key: " + str(key)
                                if key[6] == "":
                                    receivedMessageList.append(u'')
                                else:
                                    receivedMessageList.append(key[6])
                        print "receivedMessageList: "
                        #print receivedMessageList
                        intervalDict[interval] = receivedMessageList
                        print "intervaldict: "
                        #print intervalDict
                    frameLengthDict[frameLength] = intervalDict
                    print "frameLengthDict: "
                    #print frameLengthDict
                delayDict[delay] = frameLengthDict
                print "delaydict: "
                #print delayDict
            offsetDict[offset] = delayDict
            print "offsetDict"
            #print offsetDict
        rMessageDict[messageLength] = offsetDict
        print "rMessageDict"
        #print rMessageDict
    print "Now populate the rFrameDict with values from the keysList (from the json)"
    for messageLength in rFrameDict:
        print "messageLength: " + str(messageLength)
        offsetDict = OrderedDict.fromkeys(offsets)
        for offset in rFrameDict[messageLength]:
            print "offset: " + str(offset)
            delayDict = OrderedDict.fromkeys(delays)
            for delay in rFrameDict[messageLength][offset]:
                print "delay: " + str(delay)
                frameLengthDict = OrderedDict.fromkeys(frameLengths)
                for frameLength in rFrameDict[messageLength][offset][delay]:
                    print "frameLength: " + str(frameLength)
                    intervalDict = OrderedDict.fromkeys(timeIntervals, [])
                    for interval in rFrameDict[messageLength][offset][delay][frameLength]:
                        print "interval: " + str(interval)
                        # #print rMessageDict[messageLength][offset][delay][frameLength][interval]
                        receivedFrameList = []
                        for key in keyList:
                            if key[0] == messageLength and key[1] == offset and key[2] == delay and key[3] == frameLength and key[4] == interval and key[5] in numberOfRuns:
                                print "key: " + str(key)
                                receivedFrameList.append(key[7])
                        print "receivedMessageList: "
                        #print receivedFrameList
                        intervalDict[interval] = receivedFrameList
                        print "intervaldict: "
                        #print intervalDict
                    frameLengthDict[frameLength] = intervalDict
                    print "frameLengthDict: "
                    #print frameLengthDict
                delayDict[delay] = frameLengthDict
                print "delaydict: "
                #print delayDict
            offsetDict[offset] = delayDict
            print "offsetDict"
            #print offsetDict
        rFrameDict[messageLength] = offsetDict
        print "rFrameDict"
        #print rFrameDict
    sentValuesDict["messageDict"] = sMessageDict
    receivedValuesDict["messageDict"] = rMessageDict
    sentValuesDict["frameDict"] = sFrameDict
    receivedValuesDict["frameDict"] = rFrameDict
    return messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict

def filterData(messageLengths, offsets, delays,
                   frameLengths, timeIntervals, numberOfRuns,
                   sentValuesDict, receivedValuesDict):
    print "filterData()"
    print "filter data based on msgLenToPlot, delayToPlot, frameLenToPlot"
    #print msgLenToPlot, delayToPlot, frameLenToPlot
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
    # #pprint(sentValuesDict)
    # #pprint(receivedValuesDict)
    return messageLengths, offsets, delays, \
           frameLengths, timeIntervals, numberOfRuns, \
           sentValuesDict, receivedValuesDict

def getMSB(messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentFrames, receivedFrames):
    print "getMSB()"
    msbDict = OrderedDict.fromkeys(messageLengths)

    globalMSB = 0
    for messageLength in messageLengths:
        offsetDict = OrderedDict.fromkeys(offsets)
        for offset in offsets:
            delayDict = OrderedDict.fromkeys(delays)
            for delay in delays:
                frameLengthDict = OrderedDict.fromkeys(frameLengths)
                for frameLength in frameLengths:
                    intervalDict = OrderedDict.fromkeys(timeIntervals, [])
                    for interval in timeIntervals:
                        # localMSB = 0
                        # frames = 0
                        msbList = []
                        for run in range(len(receivedFrames[messageLength][offset][delay][frameLength][interval])):
                            localMSB = 0
                            frames = 0
                            for bitValues in receivedFrames[messageLength][offset][delay][frameLength][interval][run]:
                                if bitValues == u'':
                                    localMSB += 1
                                    globalMSB += 1
                                else:
                                    frames += 1
                            msbList.append(float(localMSB)/(float(localMSB) + float(frames)) * 100)
                        # print "localMSB for: "
                        # #print messageLength, offset, delay, frameLength, interval
                        # print "is: " + str(localMSB)
                        intervalDict[interval] = msbList
                    frameLengthDict[frameLength] = intervalDict
                delayDict[delay] = frameLengthDict
            offsetDict[offset] = delayDict
        msbDict[messageLength] = offsetDict
    print "msbDict: "
    #pprint(msbDict)
    print "globalMSB is: " + str(globalMSB)
    return msbDict, globalMSB

def getEOM(messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentFrames, receivedFrames):
    print "getErrors()"
    eomDict = OrderedDict.fromkeys(messageLengths)
    bfDict = OrderedDict.fromkeys(messageLengths)

    globalEOM = 0
    for messageLength in messageLengths:
        offsetDict = OrderedDict.fromkeys(offsets)
        for offset in offsets:
            delayDict = OrderedDict.fromkeys(delays)
            for delay in delays:
                frameLengthDict = OrderedDict.fromkeys(frameLengths)
                for frameLength in frameLengths:
                    intervalDict = OrderedDict.fromkeys(timeIntervals, [])
                    for interval in timeIntervals:
                        localEOM = 0
                        shortFrames = []
                        for run in range(len(receivedFrames[messageLength][offset][delay][frameLength][interval])):
                            correctFrames = 0
                            if len(receivedFrames[messageLength][offset][delay][frameLength][interval][run])\
                                < len(sentFrames[messageLength][offset][delay][frameLength][interval][run]):
                                print "received frames less than sent, got: " +\
                                      str(len(receivedFrames[messageLength][offset][delay][frameLength][interval][run]))
                                print "sent frames: " + \
                                  str(len(sentFrames[messageLength][offset][delay][frameLength][interval][run]))
                                shortFrames.append(len(receivedFrames[messageLength][offset][delay][frameLength][interval][run]))
                                for bitValues in receivedFrames[messageLength][offset][delay][frameLength][interval][run]:
                                    if bitValues != u'':
                                        correctFrames += 1
                                localEOM += 1
                                globalEOM += 1
                        print "localEOM for: "
                        #print messageLength, offset, delay, frameLength, interval
                        print "is: " + str(localEOM)
                        intervalDict[interval] = [localEOM, shortFrames]
                    frameLengthDict[frameLength] = intervalDict
                delayDict[delay] = frameLengthDict
            offsetDict[offset] = delayDict
        eomDict[messageLength] = offsetDict
    print "eomDict: "
    #pprint(eomDict)
    print "globalEOM is: " + str(globalEOM)
    return eomDict, globalEOM

def getBF(messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentFrames, receivedFrames):
    print "getBF()"
    bfDict = OrderedDict.fromkeys(messageLengths)

    globalBF = 0
    globalMissEOM = 0
    for messageLength in messageLengths:
        offsetDict = OrderedDict.fromkeys(offsets)
        for offset in offsets:
            delayDict = OrderedDict.fromkeys(delays)
            for delay in delays:
                frameLengthDict = OrderedDict.fromkeys(frameLengths)
                for frameLength in frameLengths:
                    intervalDict = OrderedDict.fromkeys(timeIntervals, [])
                    for interval in timeIntervals:
                        localBF = 0
                        localReceivedFrames = 0
                        localCorrectFrames = 0
                        localMissEOM = 0
                        for run in range(len(receivedFrames[messageLength][offset][delay][frameLength][interval])):
                            for receiverFrameIndex in range(len(receivedFrames[messageLength][offset][delay][frameLength][interval][run])):
                                if receiverFrameIndex + 1 > len(sentFrames[messageLength][offset][delay][frameLength][interval][run]):
                                    print "Receiver missed EOM frame for: "
                                    #print messageLength, offset, delay, frameLength, interval, run
                                    globalMissEOM += 1
                                    break
                                if receivedFrames[messageLength][offset][delay][frameLength][interval][run][receiverFrameIndex] == u'':
                                    continue
                                else:
                                    localBF += Levenshtein.hamming(
                                        sentFrames[messageLength][offset][delay][frameLength][interval][run][receiverFrameIndex],
                                        receivedFrames[messageLength][offset][delay][frameLength][interval][run][receiverFrameIndex]
                                    )
                                    globalBF += Levenshtein.hamming(
                                        sentFrames[messageLength][offset][delay][frameLength][interval][run][receiverFrameIndex],
                                        receivedFrames[messageLength][offset][delay][frameLength][interval][run][receiverFrameIndex]
                                    )
                                    localReceivedFrames += 1
                                    if Levenshtein.hamming(
                                            sentFrames[messageLength][offset][delay][frameLength][interval][run][receiverFrameIndex],
                                            receivedFrames[messageLength][offset][delay][frameLength][interval][run][receiverFrameIndex]
                                    ) == 0:
                                        localCorrectFrames += 1
                        print "localBF for: "
                        #print messageLength, offset, delay, frameLength, interval
                        print "is: " + str(localBF)
                        intervalDict[interval] = [localBF, localReceivedFrames, localCorrectFrames]
                    frameLengthDict[frameLength] = intervalDict
                delayDict[delay] = frameLengthDict
            offsetDict[offset] = delayDict
        bfDict[messageLength] = offsetDict
    print "bfDict: "
    #pprint(bfDict)
    print "globalBF is: " + str(globalBF)
    print "globalMissEOM is: " + str(globalMissEOM)
    return bfDict, globalBF

def plotMSB(noLoadData, withLoadData):
    print "plotMSB()"
    totalFrames = {u'07': 64, u'14': 32, u'28': 16}
    plt.figure(1, figsize=(width, height), frameon=False)
    fig = plt.figure(1, frameon=True)
    fig.subplots_adjust(bottom=0.2)
    ax = plt.subplot(1,2,1)
    ax.yaxis.grid()
    data = []
    y = noLoadData
    for messageLength in y:
        for offset in y[messageLength]:
            for delay in y[messageLength][offset]:
                for frameLength in y[messageLength][offset][delay]:
                    for interval in y[messageLength][offset][delay][frameLength]:
                        data.append(y[messageLength][offset][delay][frameLength][interval])
                        # data.append([float(y[messageLength][offset][delay][frameLength][interval][0])/(y[messageLength][offset][delay][frameLength][interval][0] + y[messageLength][offset][delay][frameLength][interval][1]) * 100])
    # medianpointprops = dict(marker='', linestyle='-', color='red')
    bp = plt.boxplot(data, patch_artist=True)
    # colors = ['#3D9970', '#FF9136', '#FFC51B']
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
    plt.ylabel('Miss start bit errors (%)')
    c = 0
    ax.text(c+3, 110.0, u'FL=7')
    ax.text(c+11, 110.0, u'FL=14')
    ax.text(c+19, 110.0, u'FL=28')
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
    #ax.set_ylim([0, 10])
    plt.xlabel("Time Interval (ms)\n(a) Miss start bit errors without load")
    box = ax.get_position()
    ax.set_position([box.x0 * .5, box.y0, box.width * 1.22, box.height * 0.95])
    # ax.yaxis.grid(True, linestyle='-', which='major', color='grey')
    ax.set_axisbelow(True)
    plt.savefig(msbResultsFile)

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
                    for interval in y[messageLength][offset][delay][frameLength]:
                        data.append(y[messageLength][offset][delay][frameLength][interval])
    # medianpointprops = dict(marker='', linestyle='-', color='red')
    bp = plt.boxplot(data, patch_artist=True)
    # colors = ['#3D9970', '#FF9136', '#FFC51B']
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
    plt.ylabel('Miss start bit errors (%)')
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
    plt.savefig(msbResultsFile)

def plotEOM(noLoadData, withLoadData, numberOfRuns):
    print "plotEOM()"
    totalFrames = {u'07': 64, u'14': 32, u'28': 16}
    plt.figure(1, figsize=(width, height), frameon=False)
    fig = plt.figure(1, frameon=True)
    fig.subplots_adjust(bottom=0.2)
    ax = plt.subplot(1,2,1)
    ax.yaxis.grid()
    data = []
    y = noLoadData
    for messageLength in y:
        for offset in y[messageLength]:
            for delay in y[messageLength][offset]:
                for frameLength in y[messageLength][offset][delay]:
                    for interval in y[messageLength][offset][delay][frameLength]:
                        data.append([float(y[messageLength][offset][delay][frameLength][interval][0])/(len(numberOfRuns)) * 100])
    # medianpointprops = dict(marker='', linestyle='-', color='red')
    bp = plt.boxplot(data, patch_artist=True)
    # colors = ['#3D9970', '#FF9136', '#FFC51B']
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
    plt.ylabel('End of message errors (%)')
    c = 0
    ax.text(c+3, 110.0, u'FL=7')
    ax.text(c+11, 110.0, u'FL=14')
    ax.text(c+19, 110.0, u'FL=28')
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
    # ax.set_ylim([0, 26])
    plt.xlabel("Time Interval (ms)\n(a) End of message errors without load")
    box = ax.get_position()
    ax.set_position([box.x0 * .5, box.y0, box.width * 1.22, box.height * 0.95])
    # ax.yaxis.grid(True, linestyle='-', which='major', color='grey')
    ax.set_axisbelow(True)
    plt.savefig(eomResultsFile)

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
                    for interval in y[messageLength][offset][delay][frameLength]:
                        data.append([float(y[messageLength][offset][delay][frameLength][interval][0])/(len(numberOfRuns)) * 100])
    # medianpointprops = dict(marker='', linestyle='-', color='red')
    bp = plt.boxplot(data, patch_artist=True)
    # colors = ['#3D9970', '#FF9136', '#FFC51B']
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
    plt.ylabel('End of message errors (%)')
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
    plt.savefig(eomResultsFile)


def plotCF(x, y, labels, numberOfRuns):
    print "plotBF()"
    totalFrames = {u'07': 64, u'14': 32, u'28': 16}
    fig = plt.figure(1, frameon=True)
    fig.subplots_adjust(bottom=0.2)
    ax = plt.subplot(111)
    ax.yaxis.grid()
    data = []
    for messageLength in y:
        for offset in y[messageLength]:
            for delay in y[messageLength][offset]:
                for frameLength in y[messageLength][offset][delay]:
                    for interval in y[messageLength][offset][delay][frameLength]:
                        if y[messageLength][offset][delay][frameLength][interval][1] == 0:
                            data.append([0])
                        else:
                            data.append([(float(y[messageLength][offset][delay][frameLength][interval][2])/float(y[messageLength][offset][delay][frameLength][interval][1])) * 100])
                            # #print (float(y[messageLength][offset][delay][frameLength][interval][0])/float(y[messageLength][offset][delay][frameLength][interval][1]))/float(frameLength)
    medianpointprops = dict(marker='', linestyle='-', color='red')
    bp = plt.boxplot(data, sym='+', vert=1, whis=1.5, patch_artist=True, medianprops=medianpointprops)
    # colors = ['#3D9970', '#FF9136', '#FFC51B']
    colors = ['white', 'white', 'white']
    k = 0
    i = 0
    for patch in bp['boxes']:
        if k > 7 and k < 15:
            i = 1
        elif k > 15:
            i = 2
        patch.set_facecolor(colors[i])
        plt.setp(bp['whiskers'], color='black')
        plt.setp(bp['fliers'], color='blue')
        k += 1
    plt.ylabel('Correct frames received (%)')
    c = 0
    ax.text(c+3, 110.0, u'FL=7')
    ax.text(c+11, 110.0, u'FL=14')
    ax.text(c+19, 110.0, u'FL=28')
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
    plt.tick_params(axis='both', which='major', labelsize=5)
    # ax.set_ylim([0, 26])
    plt.xlabel("Time Interval [ms]")
    box = ax.get_position()
    ax.set_position([box.x0 * 0.9, box.y0 + box.height * 0.20 , box.width * 1.0, box.height * 0.80])
    ax.yaxis.grid(True, linestyle='-', which='major', color='grey')
    ax.set_axisbelow(True)
    plt.savefig(cfResultsFile)
    print "boxplot data: "
    #pprint(data)

def main():
    messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict = get_data(noLoadPath)
    # print "messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict"
    # #print messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict
    print "filter data..."
    messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict = filterData(
        messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict)
    noLoadmsbDict, globalMSB = getMSB(messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict["frameDict"], receivedValuesDict["frameDict"])
    # noLoadeomDict, globalEOM = getEOM(messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict["frameDict"], receivedValuesDict["frameDict"])
    # bfDict, globalBF = getBF(messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict["frameDict"], receivedValuesDict["frameDict"])
    # print "global errors msb, eom, bf: "
    # #print globalMSB, globalEOM, globalBF

    if delayToPlot[0] == u'3.0':
        withLoadmsbDict = {}
        withLoadeomDict = {}
    else:
        messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict = get_data(withLoadPath)
        print "messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict"
        # print messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict
        # print "\n\n\n" + str(numberOfRuns) + "\n\n\n"
        print "filter data..."
        messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict = filterData(
            messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict, receivedValuesDict)
        withLoadmsbDict, globalMSB = getMSB(messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict["frameDict"], receivedValuesDict["frameDict"])
        # withLoadeomDict, globalEOM = getEOM(messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict["frameDict"], receivedValuesDict["frameDict"])
        # bfDict, globalBF = getBF(messageLengths, offsets, delays, frameLengths, timeIntervals, numberOfRuns, sentValuesDict["frameDict"], receivedValuesDict["frameDict"])
        # print "global errors msb, eom, bf: "
        # #print globalMSB, globalEOM, globalBF

    plotMSB(noLoadmsbDict, withLoadmsbDict)
    # plotEOM(noLoadeomDict, withLoadeomDict, numberOfRuns)
    # plotCF(timeIntervals, bfDict, frameLengths, numberOfRuns)
main()
