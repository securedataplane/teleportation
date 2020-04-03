#!/usr/bin/env python
import sys, getopt
import os
import re
import json
from pprint import pprint
# import plotly
#print plotly.__version__  # version >1.9.4 required
# import plotly.graph_objs as go
import numpy as np
import matplotlib.pyplot as plt

# with was measured in inkscape
width = 3.487*2
height = 2.15512979

resultKeys = ['10M', '20M', '30M', '40M', '50M', '60M', '70M']
#resultKeys = ['10M', '20M', '30M', '40M', '50M', '60M', '70M', '80M', '90M', '100M']
xAxisTimeLine = range(1, 800)
#  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
#12578 onos      20   0 3210988 122948  23324 S  99,7  3,1   0:02.00 java
cpuPattern = "\d+\s+onos\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\w+\s+\d+,\d+"
pattern = "\d+\s+onos\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\w+\s+\d+,\d+\s+\d+,\d+"
markers = ['None', 'None', 'None', 'None', 'None', 'o', 'v']
markers = ['1', '2', '3', '4', '.', 'x', '+']
markerColours = ['#097054', '#FFDE00', '#6599FF', '#FF9900', '#217C7E', '#9A3334', '#E86850']
markerColours = ['#627894', '#466289', '#6D8CA0', '#A0AEC1', '#BACFE4', '#B4D2E7', '#D4DDEF']
markerColours = ['#D4DDEF', '#B4D2E7', '#BACFE4', '#A0AEC1', '#6D8CA0', '#466289', '#627894']
colors = [u'#64b5cd', u'#4c72b0', u'#55a868', u'#c44e52', u'#8172b2', u'#ccb974', u'#64b5cd']
colors = ['white', 'white']
fontsize = 18

noLoadTopPath='../data/noLoad/top'
withLoadTopPath='../data/withLoad/top'

resultsFile='diss-cameraReady-cpu-memory-boxplot-10M-70M.pdf'
CpuResultFileName=resultsFile
MemoryResultFileName=CpuResultFileName

def getResultFiles(path):
    fileList = []
    for root, directories, filenames in os.walk(path, 'r'):
        for filename in filenames:
            fileList.append(os.path.join(root, filename))
    return fileList

def getDictWithCpuAndMem(fileList):
    tempDict = dict.fromkeys(resultKeys, None)
    for file in fileList:
        values = []
        if re.search('onosCpuMem', file):
            fileHandle = open(file, 'r')
            fileData = fileHandle.read()
            fileHandle.close()
            matches = re.findall(pattern, fileData)
            if re.search('-10M', file):
                if tempDict.get('10M') is None:
                    values.append(matches)
                    tempDict['10M'] = values
                else:
                    values = tempDict.get('10M')
                    values.append(matches)
                    tempDict['10M'] = values
            elif re.search('-20M', file):
                if tempDict.get('20M') is None:
                    values.append(matches)
                    tempDict['20M'] = values
                else:
                    values = tempDict.get('20M')
                    values.append(matches)
                    tempDict['20M'] = values
            elif re.search('-30M', file):
                if tempDict.get('30M') is None:
                    values.append(matches)
                    tempDict['30M'] = values
                else:
                    values = tempDict.get('30M')
                    values.append(matches)
                    tempDict['30M'] = values
            elif re.search('-40M', file):
                if tempDict.get('40M') is None:
                    values.append(matches)
                    tempDict['40M'] = values
                else:
                    values = tempDict.get('40M')
                    values.append(matches)
                    tempDict['40M'] = values
            elif re.search('-50M', file):
                if tempDict.get('50M') is None:
                    values.append(matches)
                    tempDict['50M'] = values
                else:
                    values = tempDict.get('50M')
                    values.append(matches)
                    tempDict['50M'] = values
            elif re.search('-60M', file):
                if tempDict.get('60M') is None:
                    values.append(matches)
                    tempDict['60M'] = values
                else:
                    values = tempDict.get('60M')
                    values.append(matches)
                    tempDict['60M'] = values
            elif re.search('-70M', file):
                if tempDict.get('70M') is None:
                    values.append(matches)
                    tempDict['70M'] = values
                else:
                    values = tempDict.get('70M')
                    values.append(matches)
                    tempDict['70M'] = values
            elif re.search('-80M', file):
                if tempDict.get('80M') is None:
                    values.append(matches)
                    tempDict['80M'] = values
                else:
                    values = tempDict.get('80M')
                    values.append(matches)
                    tempDict['80M'] = values
            elif re.search('-90M', file):
                if tempDict.get('90M') is None:
                    values.append(matches)
                    tempDict['90M'] = values
                else:
                    values = tempDict.get('90M')
                    values.append(matches)
                    tempDict['90M'] = values
            elif re.search('-100M', file):
                if tempDict.get('100M') is None:
                    values.append(matches)
                    tempDict['100M'] = values
                else:
                    values = tempDict.get('100M')
                    values.append(matches)
                    tempDict['100M'] = values
            elif re.search('ofcOnly', file):
                if tempDict.has_key('ofcOnly'):
                    values = tempDict['ofcOnly']
                    values.append(matches)
                    tempDict['ofcOnly'] = values
                else:
                    tempDict['ofcOnly'] = [matches]
    return tempDict

def parseCpu(d):
    tempDict = dict.fromkeys(resultKeys, None)
    if d.has_key('ofcOnly'):
        tempDict['ofcOnly'] = []
    for k in d.keys():
        valuesList = []
        valuesList = d.get(k)
        if valuesList == None:
            print('No values for ' + k + 'key')
            continue
        cpuList = []
        for l in valuesList:
            cpuTrialList = []
            for v in l:
                #for v in valuesList[0]:
                #Remove multiple whitespaces first
                subString = re.sub('\s+', ' ', str(v))
                #Then split the string based on a whitespace
                #The 9th position is the CPU and 10th is the Memory
                splitString = subString.split(' ')
                #print('cpu used:' + str(splitString[8]))
                #print('mem used:' + str(splitString[9]))
                #print subString
                cpuValue = str(splitString[8]).replace(',','.')
                #print cpuValue
                cpuTrialList.append(cpuValue)
            cpuList.append(cpuTrialList)
        tempDict[k] = cpuList
    return tempDict

def parseMem(d):
    tempDict = dict.fromkeys(resultKeys, None)
    if d.has_key('ofcOnly'):
        tempDict['ofcOnly'] = []
    for k in d.keys():
        valuesList = []
        valuesList = d.get(k)
        if valuesList == None:
            print('No values for ' + k + 'key')
            continue
        memList = []
        for l in valuesList:
            memTrialList = []
            for v in l:
                #Remove multiple whitespaces first
                subString = re.sub('\s+', ' ', str(v))
                #Then split the string based on a whitespace
                #The 9th position is the CPU and 10th is the Memory
                splitString = subString.split(' ')
                #print('cpu used:' + str(splitString[8]))
                #print('mem used:' + str(splitString[9]))
                #print subString
                memValue = str(splitString[9]).replace(',','.')
                # print memValue
                memTrialList.append(memValue)
            memList.append(memTrialList)
        tempDict[k] = memList
    return tempDict

def getAvgCpuResults(cpuResultsDict, withLoad=False):
    allCpuResults = dict.fromkeys(resultKeys, None)
    if cpuResultsDict.has_key('ofcOnly'):
        allCpuResults['ofcOnly'] = []
    for k in resultKeys:
        averageCpuResults = []
        cpuResults = cpuResultsDict[k]
        if cpuResults == None:
            print('No cpuResults for ' + k + 'key')
            continue
        count = len(cpuResults)
        print "count is:" + str(count)
        if withLoad is False:
            for i in range(70+60, 70+60+600):
                totalPerSecondCpu = 0
                for trial in range(0, 1):
                # for trial in range(0, count):
                    totalPerSecondCpu += float(cpuResults[trial][i])
                averagePerSecondCpu = totalPerSecondCpu / 1
                # averagePerSecondCpu = totalPerSecondCpu / count
                averageCpuResults.append(averagePerSecondCpu)
            allCpuResults[k] = averageCpuResults
        elif withLoad is True:
            for i in range(70+60+60, 70+60+600+60):
                totalPerSecondCpu = 0
                for trial in range(0, 1):
                # for trial in range(0, count):
                    totalPerSecondCpu += float(cpuResults[trial][i])
                averagePerSecondCpu = totalPerSecondCpu / 1
                # averagePerSecondCpu = totalPerSecondCpu / count
                averageCpuResults.append(averagePerSecondCpu)
            allCpuResults[k] = averageCpuResults
    return allCpuResults

def getAvgMemResults(memResultsDict, withLoad=False):
    allMemResults = dict.fromkeys(resultKeys, None)
    if memResultsDict.has_key('ofcOnly'):
        allMemResults['ofcOnly'] = []
    for k in resultKeys:
        averageMemResults = []
        memResults = memResultsDict[k]
        if memResults == None:
            print('No memResults for ' + k + 'key')
            continue
        count = len(memResults)
        if withLoad is False:
            for i in range(70+60, 70+60+600):
                # print i
                totalPerSecondMem = 0
                for trial in range(0, 1):
                # for trial in range(0, count):
                    totalPerSecondMem += float(memResults[trial][i])
                averagePerSecondMem = totalPerSecondMem / 1
                # averagePerSecondMem = totalPerSecondMem / count
                averageMemResults.append(averagePerSecondMem)
            allMemResults[k] = averageMemResults
        elif withLoad is True:
            for i in range(70+60+60, 70+60+600+60):
                totalPerSecondMem = 0
                for trial in range(0, 1):
                # for trial in range(0, count):
                    totalPerSecondMem += float(memResults[trial][i])
                averagePerSecondMem = totalPerSecondMem / 1
                # averagePerSecondMem = totalPerSecondMem / count
                averageMemResults.append(averagePerSecondMem)
            allMemResults[k] = averageMemResults
    return allMemResults

def cpuAndMemory():
    print('Get CPU data.')
    #no Load
    noLoadFileList = getResultFiles(noLoadTopPath)
    noLoadCpuMemDict = getDictWithCpuAndMem(noLoadFileList)
    cpuResultsDict = parseCpu(noLoadCpuMemDict)
    memResultsDict = parseMem(noLoadCpuMemDict)
    noLoadCpuResultsDict = getAvgCpuResults(cpuResultsDict)
    noLoadMemResultsDict = getAvgMemResults(memResultsDict)

    #with Load
    withLoadFileList = getResultFiles(withLoadTopPath)
    ofcOnlyFileList = getResultFiles('../data/onlyLoad')
    withLoadCpuMemDict = getDictWithCpuAndMem(withLoadFileList)
    ofcOnlyCpuMemDict = getDictWithCpuAndMem(ofcOnlyFileList)
    cpuResultsDict = parseCpu(withLoadCpuMemDict)
    memResultsDict = parseMem(withLoadCpuMemDict)
    withLoadCpuResultsDict = getAvgCpuResults(cpuResultsDict, withLoad=True)
    withLoadMemResultsDict = getAvgMemResults(memResultsDict, withLoad=True)

    cpu = []
    mem = []
    for key in resultKeys:
        cpu.append(noLoadCpuResultsDict[key])
    for key in resultKeys:
        cpu.append(withLoadCpuResultsDict[key])
    for key in resultKeys:
        mem.append(noLoadMemResultsDict[key])
    for key in resultKeys:
        mem.append(withLoadMemResultsDict[key])
    #################################################
    #### CPU stuff
    plt.style.use('./dissertation.mplstyle')
    fig = plt.figure(1, figsize=(width, height), frameon=True)
    ax = plt.subplot(1,2,1)
    bp = plt.boxplot(cpu, patch_artist=True)
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
    plt.ylabel("CPU usage (%)")
    c = 0
    ax.text(c+3, 111, u'No load', fontsize=6)
    ax.text(c+10, 111, u'With load', fontsize=6)
    offset = 7.5
    plt.plot([offset, offset], [20, 110], color='#000000')
    xmark=['10', '20', '30', '40', '50', '60', '70', '10', '20', '30', '40', '50', '60', '70']
    plt.xticks(range(1, 15), tuple(xmark))
    box=ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.15 , box.width * 1.0, box.height * 0.85])
    ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.5)
    ax.set_axisbelow(True)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.ylim((30, 110))
    plt.savefig(CpuResultFileName, format='pdf', bbox_inches='tight')
    #################################################
    #### Memory stuff
    fig = plt.figure(1, figsize=(width, height), frameon=True)
    ax = plt.subplot(1,2,2)
    bp = plt.boxplot(mem, patch_artist=True)
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
    plt.ylabel('Memory usage (MB)')
    c = 0
    ax.text(c+3, 15.01, u'No load', fontsize=6)
    ax.text(c+10, 15.01, u'With load', fontsize=6)
    offset = 7.5
    plt.plot([offset, offset], [12.5, 15.0], color='#000000')
    xmark=['10', '20', '30', '40', '50', '60', '70', '10', '20', '30', '40', '50', '60', '70']
    plt.xticks(range(1, 15), tuple(xmark))
    box=ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.15 , box.width * 1.0, box.height * 0.85])
    ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.5)
    ax.set_axisbelow(True)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.ylim((12.5, 15.0))
    plt.savefig(MemoryResultFileName, format='pdf', bbox_inches='tight')
    plt.close()

    # #OFCProbe only results
    # cpuResultsDict = parseCpu(ofcOnlyCpuMemDict)
    # list = []
    # index = 0
    # for l in cpuResultsDict['ofcOnly'][0]:
    #     index += 1
    #     if index > 99 and index < 700:
    #         list.append(l)
    #     if index > 700:
    #         break
    #
    # #OFCProbe only results using matplotlib
    # xAxis = range(0, 600)
    # xAxis = np.array(xAxis)
    # index=0
    # plt.plot(figsize=(12,7))
    # for key in resultKeys:
    #     plt.plot(xAxis, list, label='Tx at ' + key + 'bps', linestyle='',\
    #              marker=markers[index], markersize=7, color=markerColours[index])
    #     index += 1
    # # plt.legend(bbox_to_anchor=(1, 1), loc=2, shadow=True, fontsize='small', borderaxespad=1)
    # plt.ylabel('CPU usage (%)')
    # plt.xlabel('Time (s)')
    # plt.savefig('EuroSP-cpu-OfcOnly-Load.pdf', format='pdf', bbox_inches='tight')
    # plt.close()

if __name__ == "__main__":
    cpuAndMemory()
