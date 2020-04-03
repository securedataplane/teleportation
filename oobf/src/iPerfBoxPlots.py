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
labelKeys = ['10', '20', '30', '40', '50', '60', '70']
lines = ['solid', 'dashed', 'dashdot', 'dotted', ':', 'solid', 'dashed']
markers = ['None', 'None', 'None', 'None', 'None', 'o', 'v']
markers = ['1', '2', '3', '4', '.', 'x', '+']
markerColours = ['#097054', '#FFDE00', '#6599FF', '#FF9900', '#217C7E', '#9A3334', '#E86850']
markerColours = ['#627894', '#466289', '#6D8CA0', '#A0AEC1', '#BACFE4', '#B4D2E7', '#D4DDEF']
markerColours = ['#D4DDEF', '#B4D2E7', '#BACFE4', '#A0AEC1', '#6D8CA0', '#466289', '#627894']
colors = [u'#64b5cd', u'#4c72b0', u'#55a868', u'#c44e52', u'#8172b2', u'#ccb974', u'#64b5cd']
colors = ['white', 'white']
# colors = ['#5A5A5A', '#599487', '#CD6320', '#7EA1C5', '#7D7D7D', '#B1B1B1' ]
# markerColours = ['black', 'black', 'black', 'black', 'black', 'black', 'black']
fontsize = 18
xAxisTimeLine = range(1, 600)
incompleteResults = False

noLoadiPerfPath='../data/noLoad/iperf'
withLoadiPerfPath='../data/withLoad/iperf'

resultsFileName='diss-cameraReady-throughput-jitter-packetloss-boxPlot-10M-70M.pdf'
ThroughputResultFileName=resultsFileName
JitterResultFileName=ThroughputResultFileName
PacketLossResultFileName=ThroughputResultFileName

# Got this from
# https://stackoverflow.com/questions/11882393/matplotlib-disregard-outliers-when-plotting
def is_outlier(points, thresh=3.5):
    """
    Returns a boolean array with True if points are outliers and False
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor.
    """
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh

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
        print k
        for i in range(0, 1):
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
    [throughputDict, jitterDict, packetLossDict] = getAllTrialsPerformanceResultsAsDict(noLoadJsonDict, incompleteResults)
    # pprint(throughputDict)
    # The average is only over 1 trial. In this function, we discard the first 60s of measurements.
    [noLoadAverageThroughputResults, noLoadAverageJitterResults, noLoadAveragePacketLossResults] =\
        getAverageOverTrialsPerformanceAsDict(throughputDict, jitterDict, packetLossDict)
    #With load results
    incompleteResults = False
    [throughputDict, jitterDict, packetLossDict] = getAllTrialsPerformanceResultsAsDict(withLoadJsonDict, incompleteResults)
    [withLoadAverageThroughputResults, withLoadAverageJitterResults, withLoadAveragePacketLossResults] =\
        getAverageOverTrialsPerformanceAsDict(throughputDict, jitterDict, packetLossDict)

    print "boxplot the results"
    throughput=[]
    jitter=[]
    pktLoss=[]
    # For separate plots
    for key in resultKeys:
        throughput.append(noLoadAverageThroughputResults[key])
    for key in resultKeys:
        throughput.append(withLoadAverageThroughputResults[key])
    for key in resultKeys:
        x = np.array(noLoadAverageJitterResults[key])
        filteredData = x[~is_outlier(x)]
        jitter.append(filteredData)
    for key in resultKeys:
        x = np.array(withLoadAverageJitterResults[key])
        filteredData = x[~is_outlier(x)]
        jitter.append(filteredData)
    for key in resultKeys:
        pktLoss.append(noLoadAveragePacketLossResults[key])
    for key in resultKeys:
        pktLoss.append(withLoadAveragePacketLossResults[key])

    # Throughput stuff
    plt.style.use('./dissertation.mplstyle')
    plt.figure(1, figsize=(width, height), frameon=False)
    ax = plt.subplot(1,3,1)
    bp = plt.boxplot(throughput, patch_artist=True)
    k = 0
    for patch in bp['boxes']:
        i = k % 2
        patch.set_facecolor(colors[i])
        k += 1
    k = 0
    for patch in bp['boxes']:
        if k < 7:
            patch.set_facecolor(colors[0])
        if k > 6:
            patch.set_facecolor(colors[1])
        plt.setp(bp['whiskers'], color='black')
        plt.setp(bp['fliers'], color='black')
        k += 1
    plt.xlabel('Tx Throughput (Mbps)\n(a)')
    plt.ylabel('Rx Throughput (Mbps)')
    c = 0
    ax.text(c+3, 71.0, 'No load', fontsize=6)
    ax.text(c+10, 71.0, 'With load', fontsize=6)
    offset = 7.5
    plt.plot([offset, offset], [0, 70], color='#000000')
    xmark=['10', '20', '30', '40', '50', '60', '70', '10', '20', '30', '40', '50', '60', '70']
    plt.xticks(range(1, 15), tuple(xmark))
    box=ax.get_position()
    ax.set_position([box.x0-0.01, box.y0 + box.height * 0.15 , box.width * 1.0, box.height * 0.85])
    ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.5)
    ax.set_axisbelow(True)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.ylim((0, 70))
    plt.savefig(ThroughputResultFileName, format='pdf', bbox_inches='tight')

    ################################################
    ##### Jitter stuff
    fig = plt.figure(1, figsize=(width, height), frameon=True)
    ax = plt.subplot(1,3,2)
    # plt.tight_layout()
    bp = plt.boxplot(jitter, patch_artist=True)
    k = 0
    for patch in bp['boxes']:
        i = k % 2
        patch.set_facecolor(colors[i])
        k += 1
    k = 0
    for patch in bp['boxes']:
        if k < 7:
            patch.set_facecolor(colors[0])
        if k > 6:
            patch.set_facecolor(colors[1])
        plt.setp(bp['whiskers'], color='black')
        plt.setp(bp['fliers'], color='black')
        k += 1
    plt.xlabel('Tx Throughput (Mbps)\n(b)')
    plt.ylabel('Jitter (ms)')
    c = 0
    ax.text(c+3, .71, 'No load', fontsize=6)
    ax.text(c+10, .71, 'With load', fontsize=6)
    offset = 7.5
    plt.plot([offset, offset], [0.0, .7], color='#000000')
    xmark=['10', '20', '30', '40', '50', '60', '70', '10', '20', '30', '40', '50', '60', '70']
    plt.xticks(range(1, 15), tuple(xmark))
    box=ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.15 , box.width * 1.0, box.height * 0.85])
    ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.5)
    ax.set_axisbelow(True)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.ylim((0, .70))
    plt.savefig(JitterResultFileName, format='pdf', bbox_inches='tight')

    ################################################
    # Pkt Loss stuff
    fig = plt.figure(1, figsize=(width, height), frameon=True)
    ax = plt.subplot(1,3,3)
    bp = plt.boxplot(pktLoss, patch_artist=True)
    k = 0
    for patch in bp['boxes']:
        i = k % 2
        patch.set_facecolor(colors[i])
        k += 1
    k = 0
    for patch in bp['boxes']:
        if k < 7:
            patch.set_facecolor(colors[0])
        if k > 6:
            patch.set_facecolor(colors[1])
        plt.setp(bp['whiskers'], color='black')
        plt.setp(bp['fliers'], color='black')
        k += 1
    plt.xlabel('Tx Throughput (Mbps)\n(c)')
    plt.ylabel('Packet Loss (%)')
    c = 0
    ax.text(c+3, 71.0, 'No load', fontsize=6)
    ax.text(c+10, 71.0, 'With load', fontsize=6)
    offset = 7.5
    plt.plot([offset, offset], [0, 70], color='#000000')
    xmark=['10', '20', '30', '40', '50', '60', '70', '10', '20', '30', '40', '50', '60', '70']
    plt.xticks(range(1, 15), tuple(xmark))
    box=ax.get_position()
    ax.set_position([box.x0+0.01, box.y0 + box.height * 0.15 , box.width * 1.0, box.height * 0.85])
    ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.5)
    ax.set_axisbelow(True)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.ylim((0, 70))
    plt.savefig(PacketLossResultFileName, format='pdf', bbox_inches='tight')
    plt.close()

    print('Now delete the created json files.')
    cleanUpJsonFiles(noLoadiPerfPath)
    cleanUpJsonFiles(withLoadiPerfPath)

if __name__ == "__main__":
    udp()
