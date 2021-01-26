#!/usr/bin/python

import os

regexPattern = '[ \(\)\[\]\r\n]'
searchPatterns = []

def getPath():

    scriptPath = os.path.dirname(os.path.abspath(__file__))
    outputPath = os.path.join(scriptPath, "output")
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    return (scriptPath, outputPath)

def loadINI(scriptPath):

    try:
        # Python 2
        import ConfigParser
    except ImportError:
        # Python 3
        import configparser as ConfigParser

    config = ConfigParser.ConfigParser()
    config.read(os.path.join(scriptPath, "config.ini"))

    global searchPatterns
    targetColumns = []
    headers = []

    for section in config.sections():
        if section == "searchPatterns":
            searchPatterns = [item[1] for item in config.items(section)]
        elif section == "targetColumns":
            targetColumns = [item[1].split(',') for item in config.items(section)]
        elif section == "headers":
            headers = [item[1].split(',') for item in config.items(section)]
        else:
            continue

    return (targetColumns, headers)

def searchInFile():

    import sys

    if (len(sys.argv) < 2):
        return

    matchline = []
    with open(sys.argv[1], "r") as file:
        for pattern in searchPatterns:
            matchline.append([line[line.find(pattern):] for line in file if (-1 != line.find(pattern))])
            file.seek(0)

    return matchline

def debugMatchLine(outputPath, matchline):
    
    import re
    import csv

    output = []
    for index, pattern in enumerate(searchPatterns):
        if (0 == len(matchline[index])):
            continue
        result = re.split(regexPattern, matchline[index][0])
        output.append(result)
        continue

    with open(os.path.join(outputPath, "debug.csv"), "w") as file:
        write = csv.writer(file)
        write.writerows(output)

    return

def parseToCSV(targetColumns, headers, matchline):

    import re

    output = []
    for index, pattern in enumerate(searchPatterns):
        output.append([headers[index]])
        if (0 == len(matchline[index])):
            continue
        for line in matchline[index]:
            result = re.split(regexPattern, line)
            output[index].append([result[int(i)] for i in targetColumns[index]])

    return output

def writeToCSV(outputPath, output):

    import csv
    import time

    timestr = time.strftime("%Y%m%d_%H%M%S_")
    for index, pattern in enumerate(searchPatterns):
        with open(os.path.join(outputPath, timestr + str(index) + ".csv"), "w") as file:
            write = csv.writer(file)
            write.writerows(output[index])

    return

def main():

    (scriptPath, outputPath) = getPath()
    (targetColumns, headers) = loadINI(scriptPath)
    matchline = searchInFile()

    if __debug__:
        debugMatchLine(outputPath, matchline)

    output = parseToCSV(targetColumns, headers, matchline)
    writeToCSV(outputPath, output)

    return

if __name__ == "__main__":
    main()

