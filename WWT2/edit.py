import csv
import sys

boxId = int(sys.argv[2])

newBoxId = str(sys.argv[2])
newBoxWeight = str(sys.argv[3])
newBoxPriority = str(sys.argv[4])
newBoxVolume = str(sys.argv[5])

if sys.argv[1] == "remove":
    boxData = []
    with open("/Users/noahc/Desktop/WWT/boxes.csv", "r") as csvFile:
        csvRaw = csv.reader(csvFile)
        for line in csvRaw:
            boxData.append(line)
    boxData = boxData[1:]

    newBoxData = []
    for line in boxData:
        if not int(line[0]) == boxId:
            newBoxData.append(line)
    
    dataString = "boxID,boxWeight,priority,boxVolume"
    for line in newBoxData:
        dataString += "\n" + line[0] + "," + line[1] + "," + line[2] + "," + line[3]

    with open("/Users/noahc/Desktop/WWT/boxes.csv", "w") as csvFile:
        csvFile.write(dataString)
elif sys.argv[1] == "write":
    boxData = []
    with open("/Users/noahc/Desktop/WWT/boxes.csv", "r") as csvFile:
        csvRaw = csv.reader(csvFile)
        for line in csvRaw:
            boxData.append(line)
    boxData = boxData[1:]

    found = False
    newBoxData = []
    for line in boxData:
        if not int(line[0]) == int(newBoxId):
            newBoxData.append(line)
        else:
            found = True
            newBoxData.append([newBoxId, newBoxWeight, newBoxPriority, newBoxVolume])

    if found == False:
        newBoxData.append([newBoxId, newBoxWeight, newBoxPriority, newBoxVolume])

    dataString = "boxID,boxWeight,priority,boxVolume"
    for line in newBoxData:
        dataString += "\n" + line[0] + "," + line[1] + "," + line[2] + "," + line[3]

    with open("/Users/noahc/Desktop/WWT/boxes.csv", "w") as csvFile:
        csvFile.write(dataString)