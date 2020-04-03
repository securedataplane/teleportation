#!/usr/bin/env python
import sys, getopt
import os
import re
import json
from pprint import pprint
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import itertools

# with was measured in inkscape
width = 3.487*2
height = 2.15512979

resultKeys = ['10M', '20M', '30M', '40M', '50M', '60M', '70M']
resultKeys = ['10M', '20M', '30M', '40M', '50M', '60M']
labelKeys = ['10', '20', '30', '40', '50', '60']
legendKeys = ['10Mbps', '20Mbps', '30Mbps', '40Mbps', '50Mbps', '60Mbps']
# resultKeys = ['10M', '20M', '30M', '40M', '50M', '60M', '70M', '80M', '90M', '100M']
lines = ['solid', 'dashed', 'dashdot', 'dotted', ':', 'solid', 'dashed']
markers = ['None', 'None', 'None', 'None', 'None', 'o', 'v']
markers = ['1', '2', '3', '4', '.', 'x', '+']
markerColours = ['#097054', '#FFDE00', '#6599FF', '#FF9900', '#217C7E', '#9A3334', '#E86850']
markerColours = ['#627894', '#466289', '#6D8CA0', '#A0AEC1', '#BACFE4', '#B4D2E7', '#D4DDEF']
markerColours = ['#D4DDEF', '#B4D2E7', '#BACFE4', '#A0AEC1', '#6D8CA0', '#466289', '#627894']
markerColours = [u'#64b5cd', u'#55a868', u'#c44e52', u'#8172b2', u'#ccb974', u'#4c72b0']
# Blues sequential
markerColours = [u'#d9e9f6', u'#bad6eb', u'#89bedc', u'#539ecd', u'#2b7bba', u'#0b559f']
markerColours = ['#B1B1B1', '#7D7D7D', '#5A5A5A', '#599487', '#CD6320', '#7EA1C5']
# markerColours = [u'#bad6eb', u'#539ecd', u'#0b559f']
# markerColours = ['black', 'black', 'black', 'black', 'black', 'black', 'black']
fontsize = 18
#resultKeys = ['10M', '20M', '30M', '40M', '50M', '60M', '70M', '80M', '90M', '100M']
xAxisTimeLine = range(1, 600)
incompleteResults = False

noLoadiPerfPath='../data/noLoad/iperf'
withLoadiPerfPath='../data/withLoad/iperf'
resultsFile='diss-cameraReady-throughput-scatter-10M-70M.pdf'
noLoadThroughputResultFileName=resultsFile

withLoadThroughputResultFileName=noLoadThroughputResultFileName

def getResultFiles(path):
    fileList = []
    for root, directories, filenames in os.walk(path, 'r'):
        for filename in filenames:
            fileList.append(os.path.join(root, filename))
    return fileList

def parseResultFilesAsJson(fileList):
    tempDict = dict.fromkeys(resultKeys, None)
    for file in fileList:
        values = []
        #Select only the client files as they have the JSON results.
        #Skip the first 3 lines and the last line from the original
        #file and save a .json version for parsing.
        if re.search('client', file):
            fileHandle = open(file, 'r')
            fileData = fileHandle.readlines()[3:]
            lastElementIndex = len(fileData) - 1
            fileData.pop(lastElementIndex)
            #print('Found a client result file.')
            fileHandle.close()

            jsonFile = open(file + '.json', 'wb')
            for line in fileData:
                jsonFile.write(line)
            jsonFile.close()

            with open(file + '.json', 'r') as jsonFile:
                jsonData = jsonFile.read()
            jsonData = jsonData.replace('-nan', '0')
            jsonFile.close()

            with open(file + '.json', 'w') as jsonFile:
                jsonFile.write(jsonData)
            jsonFile.close()

            jsonData = json.loads(open(file + '.json').read())
            #pprint(jsonData)
            #return
            #pprint(jsonData)
            #Now return a dictionary of JSON results.
            if re.search('client-10M', file):
                if tempDict.get('10M') is None:
                    values.append(jsonData)
                    tempDict['10M'] = values
                else:
                    values = tempDict.get('10M')
                    values.append(jsonData)
                    tempDict['10M'] = values
            elif re.search('client-20M', file):
                if tempDict.get('20M') is None:
                    values.append(jsonData)
                    tempDict['20M'] = values
                else:
                    values = tempDict.get('20M')
                    values.append(jsonData)
                    tempDict['20M'] = values
            elif re.search('client-30M', file):
                if tempDict.get('30M') is None:
                    values.append(jsonData)
                    tempDict['30M'] = values
                else:
                    values = tempDict.get('30M')
                    values.append(jsonData)
                    tempDict['30M'] = values
            elif re.search('client-40M', file):
                if tempDict.get('40M') is None:
                    values.append(jsonData)
                    tempDict['40M'] = values
                else:
                    values = tempDict.get('40M')
                    values.append(jsonData)
                    tempDict['40M'] = values
            elif re.search('client-50M', file):
                if tempDict.get('50M') is None:
                    values.append(jsonData)
                    tempDict['50M'] = values
                else:
                    values = tempDict.get('50M')
                    values.append(jsonData)
                    tempDict['50M'] = values
            elif re.search('client-60M', file):
                if tempDict.get('60M') is None:
                    values.append(jsonData)
                    tempDict['60M'] = values
                else:
                    values = tempDict.get('60M')
                    values.append(jsonData)
                    tempDict['60M'] = values
            elif re.search('client-70M', file):
                # if re.search('70M-5', file):
                #     continue
                # else:
                if tempDict.get('70M') is None:
                    values.append(jsonData)
                    tempDict['70M'] = values
                else:
                    values = tempDict.get('70M')
                    values.append(jsonData)
                    tempDict['70M'] = values
            elif re.search('client-80M', file):
                if tempDict.get('80M') is None:
                    values.append(jsonData)
                    tempDict['80M'] = values
                else:
                    values = tempDict.get('80M')
                    values.append(jsonData)
                    tempDict['80M'] = values
            elif re.search('client-90M', file):
                if tempDict.get('90M') is None:
                    values.append(jsonData)
                    tempDict['90M'] = values
                else:
                    values = tempDict.get('90M')
                    values.append(jsonData)
                    tempDict['90M'] = values
            elif re.search('client-100M', file):
                if tempDict.get('100M') is None:
                    values.append(jsonData)
                    tempDict['100M'] = values
                else:
                    values = tempDict.get('100M')
                    values.append(jsonData)
                    tempDict['100M'] = values
    return tempDict

def getAllTrialsPerformanceResultsAsDict(jsonDict, incompleteResults):
    throughputDict = dict.fromkeys(resultKeys, None)
    jitterDict = dict.fromkeys(resultKeys, None)
    packetLossDict = dict.fromkeys(resultKeys, None)
    for k in resultKeys:
        #print k
        respectiveThroughputResults = []  # Has throughput for respective nM
        respectiveJitterResults = []
        respectivePacketLossResults = []
        # if incompleteResults == True and ( k == "60M" or k == "70M" or k == "80M" or k == "90M" or k == "100M" ):
        #     print('In incomplete results:60,70 ... 100M')
        #     for i in [0]:
        #         trialThroughputResults = []  # Has throughputs for a given trial
        #         trialJitterResults = []
        #         trialPacketLossResults = []
        #         for interval in jsonDict[k][i]["intervals"]:
        #             trialThroughputResults.append(interval["sum"]["bits_per_second"] / 1000000)
        #             trialJitterResults.append(interval["sum"]["jitter_ms"])
        #             trialPacketLossResults.append(interval["sum"]["lost_percent"])
        #         respectiveThroughputResults.append(trialThroughputResults)
        #         respectiveJitterResults.append(trialJitterResults)
        #         respectivePacketLossResults.append(trialPacketLossResults)
        #     throughputDict[k] = respectiveThroughputResults
        #     jitterDict[k] = respectiveJitterResults
        #     packetLossDict[k] = respectivePacketLossResults
        # elif incompleteResults == False and k == "70M":
        #     for i in range(0, 4):
        #         trialThroughputResults = []  # Has throughputs for a given trial
        #         trialJitterResults = []
        #         trialPacketLossResults = []
        #         for interval in jsonDict[k][i]["intervals"]:
        #             trialThroughputResults.append(interval["sum"]["bits_per_second"] / 1000000)
        #             trialJitterResults.append(interval["sum"]["jitter_ms"])
        #             trialPacketLossResults.append(interval["sum"]["lost_percent"])
        #         respectiveThroughputResults.append(trialThroughputResults)
        #         respectiveJitterResults.append(trialJitterResults)
        #         respectivePacketLossResults.append(trialPacketLossResults)
        #     throughputDict[k] = respectiveThroughputResults
        #     jitterDict[k] = respectiveJitterResults
        #     packetLossDict[k] = respectivePacketLossResults
        # elif k == "80M" or k == "90M" or k == "100M":
        #     for i in [0]:
        #         trialThroughputResults = []  # Has throughputs for a given trial
        #         trialJitterResults = []
        #         trialPacketLossResults = []
        #         for interval in noLoadJsonDict[k][i]["intervals"]:
        #             trialThroughputResults.append(interval["sum"]["bits_per_second"] / 1000000)
        #             trialJitterResults.append(interval["sum"]["jitter_ms"])
        #             trialPacketLossResults.append(interval["sum"]["lost_percent"])
        #         respectiveThroughputResults.append(trialThroughputResults)
        #         respectiveJitterResults.append(trialJitterResults)
        #         respectivePacketLossResults.append(trialPacketLossResults)
        #     throughputDict[k] = respectiveThroughputResults
        #     jitterDict[k] = respectiveJitterResults
        #     packetLossDict[k] = respectivePacketLossResults
        #else:
        print k
        for i in range(0, 1):
        # for i in range(0, 10):
            print i
            trialThroughputResults = [] #Has throughputs for a given trial
            trialJitterResults = []
            trialPacketLossResults = []
            for interval in jsonDict[k][i]["intervals"]:
                trialThroughputResults.append(interval["sum"]["bits_per_second"]/1000000)
                trialJitterResults.append(interval["sum"]["jitter_ms"])
                trialPacketLossResults.append(interval["sum"]["lost_percent"])
            respectiveThroughputResults.append(trialThroughputResults)
            respectiveJitterResults.append(trialJitterResults)
            respectivePacketLossResults.append(trialPacketLossResults)
        throughputDict[k] = respectiveThroughputResults
        jitterDict[k] = respectiveJitterResults
        packetLossDict[k] = respectivePacketLossResults
    return [throughputDict, jitterDict, packetLossDict]

def getAverageOverTrialsPerformanceAsDict(throughputDict, jitterDict, packetLossDict):
    allThroughputResults = dict.fromkeys(resultKeys, None)
    allJitterResults = dict.fromkeys(resultKeys, None)
    allPacketLossResults = dict.fromkeys(resultKeys, None)
    for k in resultKeys:
        averageThroughputResults = []
        averageJitterResults = []
        averagePacketLossResults = []
        throughputResults = throughputDict[k]
        jitterResults = jitterDict[k]
        packetLossResults = packetLossDict[k]
        count = len(throughputResults)
        # discard the first 60s of traffic.
        for i in range(60, 660):
            totalPerSecondThroughput = 0
            totalPerSecondJitter = 0
            totalPerSecondPacketLoss = 0
            for trial in range(0, count):
                totalPerSecondThroughput += throughputResults[trial][i]
                totalPerSecondJitter += jitterResults[trial][i]
                totalPerSecondPacketLoss += packetLossResults[trial][i]
            averagePerSecondThroughput = totalPerSecondThroughput/count
            averagePerSecondJitter = totalPerSecondJitter/count
            averagePerSecondPacketLoss = totalPerSecondPacketLoss/count
            averageThroughputResults.append(averagePerSecondThroughput)
            averageJitterResults.append(averagePerSecondJitter)
            averagePacketLossResults.append(averagePerSecondPacketLoss)
        allThroughputResults[k] = averageThroughputResults
        allJitterResults[k] = averageJitterResults
        allPacketLossResults[k] = averagePacketLossResults
    return [allThroughputResults, allJitterResults, allPacketLossResults]

def cleanUpJsonFiles(path):
    fileList = getResultFiles(path)
    for file in fileList:
        if re.search('.json', file):
            if os.path.exists(file):
                try:
                    print('Deleting file:' + str(file))
                    os.remove(file)
                except OSError, e:
                    print("Error: %s - %s." % (e.filename, e.strerror))

def udp():
    #UDP stuff here
    print('Now delete the created json files.')
    # #Get the result files
    cleanUpJsonFiles(noLoadiPerfPath)
    cleanUpJsonFiles(withLoadiPerfPath)
    # Get the result files
    noLoadFileList = getResultFiles(noLoadiPerfPath)
    withLoadFileList = getResultFiles(withLoadiPerfPath)

    #Pattern matching through a list of files
    noLoadJsonDict = parseResultFilesAsJson(noLoadFileList)
    withLoadJsonDict = parseResultFilesAsJson(withLoadFileList)

    #No Load results
    incompleteResults = False
    allThroughputResults = []
    allJitterResults = []
    allPacketLossResults = []
    [throughputDict, jitterDict, packetLossDict] = getAllTrialsPerformanceResultsAsDict(noLoadJsonDict, incompleteResults)
    # pprint(throughputDict)
    # The average is only over 1 trial. In this function, we discard the first 60s of measurements.
    [averageThroughputResults, averageJitterResults, averagePacketLossResults] = getAverageOverTrialsPerformanceAsDict(throughputDict, jitterDict, packetLossDict)

    xAxis = range(0, 600)
    xAxis = np.array(xAxis)
    index=0
    plt.style.use('./dissertation.mplstyle')
    plt.figure(1, figsize=(width, height), frameon=False)
    ax = plt.subplot(1,2,1)
    for key, label in zip(resultKeys, labelKeys):
        plt.plot(xAxis, averageThroughputResults[key], label='Tx at ' + key + 'bps', color=markerColours[index])
        index += 1
    handles, labels = ax.get_legend_handles_labels()
    # Need to relabel the legend label. No need of the Tx at.
    labels = legendKeys
    #### Generate the legend 
    plt.legend(handles, labels, loc=3, ncol=6, bbox_to_anchor=(0,1,2,.1), mode="expand",borderaxespad=1)
    plt.ylabel('Rx Throughput (Mbps)')
    plt.xlabel('Time (s)\n(a) No Load')
    locs, labels = plt.yticks()
    locs = np.arange(10, 80, 10)
    plt.yticks(locs)
    plt.savefig(noLoadThroughputResultFileName, format='pdf', bbox_inches='tight')

    #With load results
    incompleteResults = False
    allThroughputResults = []
    allJitterResults = []
    allPacketLossResults = []
    [throughputDict, jitterDict, packetLossDict] = getAllTrialsPerformanceResultsAsDict(withLoadJsonDict, incompleteResults)
    [averageThroughputResults, averageJitterResults, averagePacketLossResults] =\
        getAverageOverTrialsPerformanceAsDict(throughputDict, jitterDict, packetLossDict)

    xAxis = range(0, 600)
    xAxis = np.array(xAxis)
    index=0
    ax = plt.subplot(1,2,2)
    for key, label in zip(resultKeys, labelKeys):
        plt.plot(xAxis, averageThroughputResults[key], label='Tx at ' + key + 'bps', color=markerColours[index])
        index += 1
    plt.ylabel('Rx Throughput (Mbps)')
    plt.xlabel('Time (s)\n(b) With Load')
    locs, labels = plt.yticks()
    locs = np.arange(10, 80, 10)
    plt.yticks(locs)
    plt.savefig(withLoadThroughputResultFileName, format='pdf', bbox_inches='tight')
    plt.close()

    print('Now delete the created json files.')
    cleanUpJsonFiles(noLoadiPerfPath)
    cleanUpJsonFiles(withLoadiPerfPath)

if __name__ == "__main__":
    udp()
